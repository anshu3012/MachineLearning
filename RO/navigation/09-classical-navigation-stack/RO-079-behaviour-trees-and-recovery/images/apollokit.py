"""Our one-dimensional model of Apollo's stop-sign scenario (ApolloAuto/apollo, branch master, read 2026-10-12). It
is NOT Apollo running. The rules that switch scenarios and stages are copied from the code:
- planning runs every 0.1 s (planning_gflags.cc: planning_loop_rate 10);
- ScenarioManager::Update keeps a scenario while it is PROCESSING; otherwise it takes the first scenario in the
  configured list (planner_config.pb.txt) whose IsTransferable() is true, else LANE_FOLLOW;
- STOP_SIGN_UNPROTECTED is transferable when the car's front is 0 to 4.0 m before the stop line
  (scenario_conf.pb.txt: start_stop_sign_scenario_distance 4.0);
- PRE_STOP ends when the car has stopped (speed at most 0.2 m/s, vehicle_param.pb.txt) at most 2.0 m before the
  line (max_valid_stop_distance), or has passed it by more than 0.3 m; meanwhile it adds every vehicle within
  5.0 m of its own stop line on the crossing lanes to a watch list;
- STOP ends after at least 1.0 s (stop_duration_sec) once the watch list is empty, a watched vehicle leaving it
  when it is more than 10.0 m from its stop line; or after 8.0 s (stop_timeout_sec) with at most one vehicle left;
- CREEP moves up to a stop fence 4.0 m past the line; it ends when the front is more than 2.0 m past the line, or
  after 10.0 s (creep_timeout_sec), and no moving obstacle can reach the path within 6.0 s (min_boundary_t), for
  5 cycles in a row;
- INTERSECTION_CRUISE ends when the car's rear is 20.0 m past the line (no junction outline in our map); the
  scenario is then DONE and the manager returns to LANE_FOLLOW.
Our own choices: the car (length 4.933 m, Apollo's Lincoln MKZ) comes at 8 m/s, brakes at 1.5 m/s^2 for the stop
fence that the stop-sign traffic rule puts 1.0 m before the line (stop_sign default_conf: stop_distance 1.0),
creeps at 1.0 m/s, and speeds up at 1.5 m/s^2; the crossing car waits at its line, leaves at 9.5 s and speeds up
at 2.0 m/s^2. No output when run on its own; run with any argument for the self-check."""
import math

DT = 0.1
L_EGO, W_EGO = 4.933, 2.11
V0, A_BRAKE, A_GO, V_CREEP = 8.0, 1.5, 1.5, 1.0
S0 = -40.0                                   # the car's front at t = 0, m (the stop line is at 0)
FENCE = -1.0                                 # stop fence: 1.0 m before the line
CREEP_TARGET, CREEP_FINISH = 4.0, 2.0        # past the line (end_s + 4.0, then minus 2.0)
CROSS_LINE, CROSS_FRONT0, T_GO, A_CROSS = 4.5, 5.5, 9.5, 2.0   # crossing car: x of its line, of its front at rest
CROSS_Y = 6.25                               # its lane centre


def cross_x(t):
    """The crossing car's front x (it drives towards -x)."""
    return CROSS_FRONT0 - (0.5 * A_CROSS * (t - T_GO) ** 2 if t > T_GO else 0.0)


def simulate(t_end=30.0):
    s, v, t = S0, V0, 0.0
    scenario, stage = "LANE_FOLLOW", None
    watch, stop_t0, creep_t0, clear, done_t = set(), None, None, 0, None
    out = []
    while t <= t_end + 1e-9:
        note = ""
        # the scenario manager (ScenarioManager::Update), then the current stage (Scenario::Process)
        if scenario == "LANE_FOLLOW" and done_t is None and 0.0 < -s <= 4.0:
            scenario, stage, note = "STOP_SIGN_UNPROTECTED", "PRE_STOP", "front 4.0 m or less before the line"
        if stage == "PRE_STOP":
            if s > 0.3 or (v <= 0.2 and -s <= 2.0):
                stage, stop_t0, note = "STOP", t, f"stopped {-s:.2f} m before the line, at {v:.2f} m/s"
            else:
                cx = cross_x(t)
                if cx - CROSS_LINE <= 5.0 and cx - CROSS_LINE >= -L_EGO:
                    watch.add("crossing car")
        elif stage == "STOP":
            wait = t - stop_t0
            gone = abs(cross_x(t) + L_EGO / 2 - CROSS_LINE) > 10.0       # its centre to its stop line
            if gone:
                watch.discard("crossing car")
            if wait >= 1.0 - 1e-9 and (not watch or (wait > 8.0 and len(watch) <= 1)):
                stage, creep_t0, note = "CREEP", t, f"waited {wait:.1f} s, watch list empty"
        elif stage == "CREEP":
            fx = cross_x(t)                      # moving and over the strip the car will drive through
            moving_near = T_GO <= t and fx < 1.75 + W_EGO / 2 and fx + L_EGO > 1.75 - W_EGO / 2
            if s > CREEP_FINISH or t - creep_t0 >= 10.0:
                clear = 0 if moving_near else clear + 1
                if clear >= 5:
                    stage, note = "INTERSECTION_CRUISE", "past the creep point, 5 clear cycles"
        elif stage == "INTERSECTION_CRUISE":
            if s - L_EGO >= 20.0:
                scenario, stage, done_t, note = "LANE_FOLLOW", None, t, "rear 20 m past the line: scenario done"
        # our speed model
        if stage in ("PRE_STOP", "STOP") or (scenario == "LANE_FOLLOW" and done_t is None):
            d = FENCE - s                        # brake for the fence once 1.5 m/s^2 is needed, then exactly
            need = v * v / (2 * d) if d > 1e-6 else math.inf
            a = -need if need >= A_BRAKE - 1e-9 else 0.0
            if stage == "STOP" or d <= 1e-6:
                a, v = 0.0, 0.0
        elif stage == "CREEP":
            a = A_GO if v < V_CREEP and s < CREEP_TARGET - 0.5 else (-A_BRAKE if s >= CREEP_TARGET - 0.5 else 0.0)
            if v >= V_CREEP and a > 0:
                a = 0.0
        else:
            a = A_GO if v < V0 else 0.0
        out.append(dict(t=round(t, 2), s=s, v=v, scenario=scenario, stage=stage, watch=sorted(watch),
                        cross=cross_x(t), note=note, stop_wait=None if stop_t0 is None else t - stop_t0,
                        creep_wait=None if creep_t0 is None else t - creep_t0, clear=clear))
        v2 = max(0.0, v + a * DT)
        s += 0.5 * (v + v2) * DT
        v = min(v2, V_CREEP if stage == "CREEP" else V0)
        t = round(t + DT, 10)
    return out


def events(out):
    """(time, scenario, stage, why) at every change."""
    ev, prev = [], None
    for r in out:
        key = (r["scenario"], r["stage"])
        if key != prev:
            ev.append((r["t"], r["scenario"], r["stage"], r["note"]))
            prev = key
    return ev


if __name__ == "__main__":
    import sys
    if len(sys.argv) > 1:
        out = simulate()
        for e in events(out):
            print(e)
        stopped = [r for r in out if r["stage"] == "STOP"]
        assert stopped and abs(stopped[0]["s"] - FENCE) < 0.3
        print("self-check passed")
