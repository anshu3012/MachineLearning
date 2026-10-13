"""A tiny physics simulator for this Note (no output when imported; run it to check itself).

A box of 1 kg (a 0.2 m cube, seen from the side, so x along the floor and z up) falls from 0.1 m with a sideways
speed of 2.0 m/s onto a floor with a coefficient of friction of 0.4 (RO-053's cup on the table), slides and stops.
Each step does what MuJoCo's mj_step does, in the same order (MuJoCo docs, Simulation): find the contact, add up
the forces, get the acceleration (Newton's second law), then advance with semi-implicit Euler: the new velocity
first, then the new position from the new velocity.

Contact: soft, a spring and damper on the depth the box's bottom has sunk into the floor, set from MuJoCo's default
contact time constant 0.02 s and damping ratio 1 (solref "0.02 1"): stiffness 1 / 0.02^2 = 2500 N/m per kg and
damping 2 / 0.02 = 100 N s/m per kg (MuJoCo's formula with impedance 1; its default solimp gives 0.9 to 0.95).
Or hard: in a step that would end inside the floor, an impulse that stops the fall at once, and the box is placed
on the floor, so it never enters it.
Friction: Coulomb, applied as an impulse capped at 0.4 times the normal impulse of the step (stick if that is
enough to stop the sliding, otherwise slip)."""
import math

import numpy as np

G, M, MU = 9.81, 1.0, 0.4
TAU, ZETA = 0.02, 1.0
K = M / (TAU ** 2 * ZETA ** 2)           # 2500 N/m
B = 2 * M / TAU                          # 100 N s/m
H0, VX0, SIZE = 0.1, 2.0, 0.2           # drop height of the bottom, sideways speed, box side (m, m/s, m)
DTS = (0.002, 0.015, 0.03)               # stable (MuJoCo's default step), jittery, unstable


def reference():
    """The exact answer with a hard floor: fall, an impact that stops the fall and takes mu times the vertical
    speed off the sideways speed, then a slide braked at mu g."""
    t_land = math.sqrt(2 * H0 / G)
    vz = G * t_land
    x_land = VX0 * t_land
    vx_after = VX0 - MU * vz
    t_slide = vx_after / (MU * G)
    d_slide = vx_after ** 2 / (2 * MU * G)
    return dict(t_land=t_land, vz_land=vz, x_land=x_land, vx_after=vx_after, t_slide=t_slide, d_slide=d_slide,
                x_stop=x_land + d_slide, t_stop=t_land + t_slide)


def friction(vx, N_imp, push_imp=0.0):
    """Coulomb friction as an impulse over one step: N_imp is the normal impulse (N s), push_imp any sideways push
    impulse. Returns the new sideways speed and the friction impulse used."""
    v_try = vx + push_imp / M
    cap = MU * N_imp
    if abs(M * v_try) <= cap:                      # friction can stop it: sticks
        return 0.0, -M * v_try
    f = -math.copysign(cap, v_try)
    return v_try + f / M, f


def simulate(dt, T=1.0, contact="soft", x0=0.0, z0=H0, vx0=VX0, vz0=0.0, push=None, stop_far=50.0):
    """Semi-implicit Euler with a soft or hard floor. push(t) is a sideways force in N. Returns an array of rows
    (t, x, z, vx, vz, normal force N, friction force N, depth m)."""
    x, z, vx, vz, t = x0, z0, vx0, vz0, 0.0
    rows = [(t, x, z, vx, vz, 0.0, 0.0, max(0.0, -z))]
    n = int(round(T / dt))
    for _ in range(n):
        F = push(t) if push else 0.0
        if contact == "soft":
            depth = -z                                  # 1 find the contact
            N = max(0.0, K * depth - B * vz) if depth > 0 else 0.0   # 2 forces
            vz = vz + dt * (-G + N / M)                 # 3 new velocity
            vx, f_imp = friction(vx, N * dt, F * dt)
        else:
            vz = vz - G * dt
            N_imp = 0.0
            hit = z + vz * dt < 0                       # the step would end inside the floor
            if hit:
                N_imp = -M * vz                         # the impulse that stops the fall at once
                vz = 0.0
            N = N_imp / dt
            vx, f_imp = friction(vx, N_imp, F * dt)
        x, z = x + vx * dt, z + vz * dt                 # 4 new position, from the new velocity
        if contact == "hard" and hit:
            z = 0.0                                     # placed on the floor, never inside it
        t = round(t + dt, 12)
        rows.append((t, x, z, vx, vz, N, f_imp / dt, max(0.0, -z)))
        if abs(z) > stop_far:
            break
    return np.array(rows)


def free_fall(dt, steps, method):
    """Free fall from H0 with no floor: 'semi' (semi-implicit Euler) or 'explicit' (position from the old
    velocity). Returns rows (t, z, vz)."""
    z, vz, out = H0, 0.0, [(0.0, H0, 0.0)]
    for k in range(1, steps + 1):
        if method == "semi":
            vz = vz - G * dt
            z = z + vz * dt
        else:
            z = z + vz * dt
            vz = vz - G * dt
        out.append((k * dt, z, vz))
    return np.array(out)


def step_factor(dt):
    """How much one semi-implicit Euler step multiplies the box's sinking speed by the damper alone: 1 - b dt / m."""
    return 1 - B * dt / M


def push_test(dt=0.002, T=3.0, rate=2.0):
    """The box at rest on the soft floor (settled first), pushed sideways with a force growing at `rate` N/s."""
    z_rest = -M * G / K
    return simulate(dt, T=T, contact="soft", z0=z_rest, vx0=0.0, push=lambda t: rate * t)


if __name__ == "__main__":
    ref = reference()
    assert abs(ref["x_stop"] - 0.5497) < 1e-3 and abs(ref["t_stop"] - 0.5097) < 1e-3
    r = simulate(0.002)
    assert abs(r[-1, 1] - ref["x_stop"]) < 0.005
    h = simulate(0.002, contact="hard")
    assert abs(h[-1, 1] - ref["x_stop"]) < 0.01 and h[:, 2].min() >= -1e-12
    assert step_factor(0.03) == -2.0 and abs(step_factor(0.015) + 0.5) < 1e-12
    print("simkit self-check passed")
