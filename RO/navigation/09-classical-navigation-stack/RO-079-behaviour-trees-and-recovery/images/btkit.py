"""Our Python version of Nav2's default behaviour tree, navigate_to_pose_w_replanning_and_recovery.xml (navigation2,
branch main, read 2026-10-12), ticked every 10 ms (bt_loop_duration) in the room of RO-058. It is NOT Nav2 running.
- The control nodes copy the code: Sequence, Fallback, ReactiveSequence, ReactiveFallback and Inverter from
  BehaviorTree.CPP (src/controls/*.cpp, src/control_node.cpp), PipelineSequence, RecoveryNode, RoundRobin and
  RateController from nav2_behavior_tree/plugins.
- The servers are simple stand-ins: the planner is A* on 0.1 m cells (a cell is blocked when the robot's disk there
  would overlap an obstacle); FollowPath is a path follower at up to 0.5 m/s and 1.0 rad/s with Nav2's goal checker
  (0.25 m, then 0.25 rad) and progress checker (0.5 m in 10 s); Spin, Wait and BackUp use the behaviour server's
  bring-up values; clearing a costmap erases its marks, and the next scan marks again whatever is still there, before
  the next plan.
- Each action returns RUNNING on the tick it is sent, as BtActionNode does, and its result on a later tick.
No output when run on its own; run with any argument for the self-check."""
import heapq
import math

import bandkit as bk
import numpy as np

IDLE, RUNNING, SUCCESS, FAILURE = "IDLE", "RUNNING", "SUCCESS", "FAILURE"
DT = 0.01                                   # bt_loop_duration 10 ms


# ---------------------------------------------------------------- the tree engine (BehaviorTree.CPP v4 rules)
class Node:
    def __init__(self, name, children=(), label=None):
        self.name, self.children, self.status = name, list(children), IDLE
        self.label = label or name

    def execute_tick(self, bb):
        s = self.tick(bb)
        self.status = s
        bb["log"].append((self.label, s, getattr(self, "uid", None)))
        return s

    def halt(self):
        self.reset_children()

    def halt_node(self):
        self.halt()

    def reset_status(self):
        self.status = IDLE

    def reset_children(self):                    # ControlNode::resetChildren
        for c in self.children:
            if c.status == RUNNING:
                c.halt_node()
            c.reset_status()

    def halt_child(self, i):                     # ControlNode::haltChild
        c = self.children[i]
        if c.status == RUNNING:
            c.halt_node()
        c.reset_status()

    def walk(self, depth=0):
        yield self, depth
        for c in self.children:
            yield from c.walk(depth + 1)


class Sequence(Node):
    def __init__(self, *a, **k):
        super().__init__(*a, **k)
        self.idx = 0

    def tick(self, bb):
        while self.idx < len(self.children):
            s = self.children[self.idx].execute_tick(bb)
            if s == RUNNING:
                return RUNNING
            if s == FAILURE:
                self.reset_children()
                self.idx = 0
                return FAILURE
            self.idx += 1
        self.reset_children()
        self.idx = 0
        return SUCCESS

    def halt(self):
        self.idx = 0
        super().halt()


class Fallback(Node):
    def __init__(self, *a, **k):
        super().__init__(*a, **k)
        self.idx = 0

    def tick(self, bb):
        while self.idx < len(self.children):
            s = self.children[self.idx].execute_tick(bb)
            if s == RUNNING:
                return RUNNING
            if s == SUCCESS:
                self.reset_children()
                self.idx = 0
                return SUCCESS
            self.idx += 1
        self.reset_children()
        self.idx = 0
        return FAILURE

    def halt(self):
        self.idx = 0
        super().halt()


class ReactiveSequence(Node):
    def tick(self, bb):
        for i, c in enumerate(self.children):
            s = c.execute_tick(bb)
            if s == RUNNING:
                for j in range(len(self.children)):
                    if j != i:
                        self.halt_child(j)
                return RUNNING
            if s == FAILURE:
                self.reset_children()
                return FAILURE
        self.reset_children()
        return SUCCESS


class ReactiveFallback(Node):
    def tick(self, bb):
        for i, c in enumerate(self.children):
            s = c.execute_tick(bb)
            if s == RUNNING:
                for j in range(len(self.children)):
                    if j != i:
                        self.halt_child(j)
                return RUNNING
            if s == SUCCESS:
                self.reset_children()
                return SUCCESS
        self.reset_children()
        return FAILURE


class Inverter(Node):
    def tick(self, bb):
        s = self.children[0].execute_tick(bb)
        if s == RUNNING:
            return RUNNING
        self.children[0].reset_status()
        return FAILURE if s == SUCCESS else SUCCESS


class PipelineSequence(Node):                        # nav2_behavior_tree/plugins/control/pipeline_sequence.cpp
    def __init__(self, *a, **k):
        super().__init__(*a, **k)
        self.last = 0

    def tick(self, bb):
        for i, c in enumerate(self.children):
            s = c.execute_tick(bb)
            if s == FAILURE:
                for j in range(len(self.children)):
                    self.halt_child(j)
                self.last = 0
                return FAILURE
            if s == RUNNING and i >= self.last:
                self.last = i
                return RUNNING
        for j in range(len(self.children)):
            self.halt_child(j)
        self.last = 0
        return SUCCESS

    def halt(self):
        super().halt()
        self.last = 0


class RecoveryNode(Node):                            # .../control/recovery_node.cpp
    def __init__(self, name, children, retries, label=None):
        super().__init__(name, children, label)
        self.retries, self.count, self.idx = retries, 0, 0

    def tick(self, bb):
        while self.idx < 2 and self.count <= self.retries:
            s = self.children[self.idx].execute_tick(bb)
            if self.idx == 0:
                if s == SUCCESS:
                    self.halt_child(1)
                    self.halt()
                    return SUCCESS
                if s == RUNNING:
                    return RUNNING
                if self.count < self.retries:
                    self.halt_child(0)
                    self.idx = 1
                else:
                    self.halt()
                    return FAILURE
            else:
                if s == RUNNING:
                    return RUNNING
                if s == SUCCESS:
                    self.halt_child(1)
                    self.count += 1
                    self.idx = 0
                else:
                    self.halt()
                    return FAILURE
        self.halt()
        return FAILURE

    def halt(self):
        super().halt()
        self.count, self.idx = 0, 0


class RoundRobin(Node):                              # .../control/round_robin_node.cpp, wrap_around true
    def __init__(self, *a, **k):
        super().__init__(*a, **k)
        self.idx, self.failed = 0, 0

    def tick(self, bb):
        n = len(self.children)
        while self.failed < n:
            s = self.children[self.idx].execute_tick(bb)
            if s != RUNNING:
                self.idx = (self.idx + 1) % n
            if s == SUCCESS:
                self.failed = 0
                for j in range(n):
                    self.halt_child(j)
                return SUCCESS
            if s == FAILURE:
                self.failed += 1
            if s == RUNNING:
                return RUNNING
        self.halt()
        return FAILURE

    def halt(self):
        super().halt()
        self.idx, self.failed = 0, 0


class RateController(Node):                          # .../decorator/rate_controller.cpp
    def __init__(self, name, children, hz, label=None):
        super().__init__(name, children, label)
        self.period, self.start, self.first = 1.0 / hz, 0.0, False

    def tick(self, bb):
        if self.status in (IDLE,):
            self.start, self.first = bb["t"], True
        child = self.children[0]
        if self.first or child.status == RUNNING or bb["t"] - self.start >= self.period - 1e-9:
            self.first = False
            s = child.execute_tick(bb)
            if s == SUCCESS:
                self.start = bb["t"]
            return s
        return RUNNING


class Leaf(Node):
    def __init__(self, name, fn, label=None):
        super().__init__(name, (), label)
        self.fn = fn

    def tick(self, bb):
        return self.fn(bb)


class Action(Node):
    """BtActionNode: on the first tick send the goal and return RUNNING; later ticks return the server's result."""

    def __init__(self, name, server, label=None):
        super().__init__(name, (), label)
        self.server, self.active = server, False

    def tick(self, bb):
        self.bb = bb
        if not self.active:
            self.active = True
            self.server.start(bb)
            return RUNNING
        s = self.server.update(bb)
        if s != RUNNING:
            self.active = False
        return s

    def halt(self):                                  # cancel the goal
        if self.active:
            self.server.cancel(self.bb)
            self.bb["halted"].append((self.bb["t"], self.label))
        self.active = False


def stop(bb):                                        # a cancelled server stops the robot
    bb["cmd"] = (0.0, 0.0)


# ---------------------------------------------------------------- the room, the planner and the servers
START = np.array([2.0, 1.0, math.radians(30)])
GOAL = np.array([3.6, 3.5, math.radians(90)])
CELL = 0.1
CLEAR = 0.25                                # the planner prefers cells whose disk keeps this gap, m


def obstacles(world):
    obs = bk.obstacles(None)
    if world.get("person") is not None:
        p = world["person"]
        obs.append(lambda x, y, p=p: np.hypot(x - p[0], y - p[1]) - bk.PERSON_R)
    if world.get("trolley") is not None:
        R = world["trolley"]
        obs.append(lambda x, y, R=R: bk.poly_dist(x, y, R))
    return obs


def gap(x, y, world):
    return np.min([o(np.asarray(x, float), np.asarray(y, float)) for o in obstacles(world)], axis=0) - bk.R_BODY


def astar(a, b, world):
    """A* on 0.1 m cells, 8 neighbours, no corner cutting; a cell is blocked when the robot's disk centred there
    would overlap an obstacle, and a step into a cell whose disk is less than 0.25 m from an obstacle costs up to 3
    times its length. Returns (path, code): code 'GOAL_OCCUPIED', 'NO_VALID_PATH' or None."""
    nx, ny = int(round(bk.ROOM_W / CELL)), int(round(bk.ROOM_H / CELL))
    cx, cy = np.meshgrid((np.arange(nx) + 0.5) * CELL, (np.arange(ny) + 0.5) * CELL, indexing="ij")
    G = gap(cx, cy, world)
    blocked = G < 0
    pen = 1.0 + 2.0 * np.clip((CLEAR - G) / CLEAR, 0, 1)      # extra cost near obstacles, like an inflation layer
    s = (int(math.floor(a[0] / CELL + 1e-9)), int(math.floor(a[1] / CELL + 1e-9)))
    t = (int(math.floor(b[0] / CELL + 1e-9)), int(math.floor(b[1] / CELL + 1e-9)))
    if blocked[t]:
        return None, "GOAL_OCCUPIED"
    blocked[s] = False
    free = lambda c: 0 <= c[0] < nx and 0 <= c[1] < ny and not blocked[c]
    d2 = math.sqrt(2) * CELL
    h = lambda c: d2 * min(abs(c[0] - t[0]), abs(c[1] - t[1])) + CELL * abs(abs(c[0] - t[0]) - abs(c[1] - t[1]))
    g, came, openl, closed = {s: 0.0}, {}, [(h(s), h(s), s)], set()
    while openl:
        _, _, c = heapq.heappop(openl)
        if c in closed:
            continue
        if c == t:
            break
        closed.add(c)
        for dx in (-1, 0, 1):
            for dy in (-1, 0, 1):
                n = (c[0] + dx, c[1] + dy)
                if (dx, dy) == (0, 0) or not free(n):
                    continue
                if dx and dy and not (free((c[0] + dx, c[1])) and free((c[0], c[1] + dy))):
                    continue
                gn = g[c] + (d2 if dx and dy else CELL) * pen[n]
                if gn < g.get(n, np.inf) - 1e-12:
                    g[n], came[n] = gn, c
                    heapq.heappush(openl, (gn + h(n), h(n), n))
    if t not in g:
        return None, "NO_VALID_PATH"
    path = [t]
    while path[-1] != s:
        path.append(came[path[-1]])
    pts = np.array([((i + 0.5) * CELL, (j + 0.5) * CELL) for i, j in path[::-1]])
    pts[0], pts[-1] = a[:2], b[:2]
    return pts, None


def path_valid(path, world, from_xy):
    """ValidatePath on the remaining path (TruncatePathLocal): for a round robot, nav2_planner's IsPathValid rejects
    a pose whose cell is lethal or inscribed, that is, where the robot's disk would overlap an obstacle."""
    k = int(np.argmin(np.hypot(*(path - from_xy).T)))
    return bool(np.all(gap(path[k:, 0], path[k:, 1], world) >= 0))


def remaining_length(path, xy):
    k = int(np.argmin(np.hypot(*(path - xy).T)))
    return float(np.sum(np.hypot(*np.diff(path[k:], axis=0).T)))


class Planner:
    """planner_server's ComputePathToPose: the result arrives on the tick after the request."""

    def start(self, bb):
        self.t0 = bb["t"]

    def update(self, bb):
        path, code = astar(bb["robot"], bb["goal"], bb["world"])
        bb["planned"].append((bb["t"], code))
        if path is None:                         # on_aborted: the path output is emptied
            bb["compute_path_error_code"], bb["path"] = code, None
            return FAILURE
        bb["compute_path_error_code"] = None
        bb["path"] = path
        return SUCCESS

    def cancel(self, bb):                        # ComputePathToPoseAction::halt empties the path
        bb["path"] = None


class Controller:
    """controller_server's FollowPath at 20 Hz with a simple path follower (look 0.4 m ahead; turn on the spot when
    the heading is more than 0.6 rad off; at most 0.5 m/s and 1.0 rad/s), the stateful goal checker (within 0.25 m,
    then within 0.25 rad) and the progress checker (0.5 m in 10 s)."""

    def start(self, bb):
        self.last_ctrl = -1.0
        self.xy_reached = False
        self.prog_t, self.prog_xy = bb["t"], bb["robot"][:2].copy()
        self.path = bb["path"]
        bb["follow_path_error_code"] = None

    def update(self, bb):
        r = bb["robot"]
        if bb["path"] is not None:               # FollowPathAction takes a new path, never an empty one
            self.path = bb["path"]
        if bb["t"] - self.last_ctrl < 0.05 - 1e-9:
            return RUNNING
        self.last_ctrl = bb["t"]
        g = bb["goal"]
        d = float(np.hypot(*(g[:2] - r[:2])))
        if d < 0.25:
            self.xy_reached = True
        yaw_err = float(bk.wrap(g[2] - r[2]))
        if self.xy_reached and abs(yaw_err) < 0.25:
            bb["cmd"] = (0.0, 0.0)
            return SUCCESS
        bb["checkers"] = dict(prog_t=self.prog_t, prog_xy=self.prog_xy.copy(), xy_reached=self.xy_reached)
        if np.hypot(*(r[:2] - self.prog_xy)) > 0.5:
            self.prog_t, self.prog_xy = bb["t"], r[:2].copy()
            bb["checkers"] = dict(prog_t=self.prog_t, prog_xy=self.prog_xy.copy(), xy_reached=self.xy_reached)
        elif bb["t"] - self.prog_t > 10.0:
            bb["follow_path_error_code"] = "FAILED_TO_MAKE_PROGRESS"
            bb["cmd"] = (0.0, 0.0)
            return FAILURE
        if self.xy_reached:
            bb["cmd"] = (0.0, float(np.clip(2.0 * yaw_err, -1.0, 1.0)))
            return RUNNING
        P = self.path
        k = int(np.argmin(np.hypot(*(P - r[:2]).T)))
        s = np.concatenate([[0], np.cumsum(np.hypot(*np.diff(P[k:], axis=0).T))])
        j = k + int(np.searchsorted(s, 0.4))
        q = P[min(j, len(P) - 1)]
        e = float(bk.wrap(math.atan2(q[1] - r[1], q[0] - r[0]) - r[2]))
        if abs(e) > 0.6:
            bb["cmd"] = (0.0, float(np.sign(e)))
        else:
            bb["cmd"] = (0.5, float(np.clip(2.0 * e, -1.0, 1.0)))
        return RUNNING

    cancel = staticmethod(stop)


class Spin:
    """nav2_behaviors::Spin, spin_dist 1.57 rad, at 10 Hz: speed sqrt(2 x 3.2 x remaining), between 0.4 and 1.0 rad/s;
    it fails after its time_allowance, 10 s."""

    def __init__(self, dist=1.57):
        self.dist = dist

    def start(self, bb):
        self.turned, self.last, self.yaw, self.t0 = 0.0, bb["t"] - 1.0, float(bb["robot"][2]), bb["t"]

    def update(self, bb):
        if bb["t"] - self.last < 0.1 - 1e-9:
            return RUNNING
        self.last = bb["t"]
        if bb["t"] - self.t0 > 10.0:             # time_allowance 10 s
            bb["cmd"] = (0.0, 0.0)
            return FAILURE
        y = float(bb["robot"][2])
        self.turned += abs(float(bk.wrap(y - self.yaw)))
        self.yaw = y
        rem = self.dist - self.turned
        if rem <= 0:
            bb["cmd"] = (0.0, 0.0)
            return SUCCESS
        w = min(max(0.4, math.sqrt(2 * 3.2 * rem)), 1.0)
        bb["cmd"] = (0.0, w)
        return RUNNING

    cancel = staticmethod(stop)


class Wait:
    def __init__(self, duration=5.0):
        self.duration = duration

    def start(self, bb):
        self.t0 = bb["t"]
        bb["cmd"] = (0.0, 0.0)

    def update(self, bb):
        return SUCCESS if bb["t"] - self.t0 >= self.duration - 1e-9 else RUNNING

    cancel = staticmethod(stop)


class BackUp:
    """nav2_behaviors::BackUp, backup_dist 0.30 m at backup_speed 0.15 m/s, at 10 Hz. Before each step it checks
    the poses ahead (simulate_ahead_time 2.0 s, at most the distance left) and fails if the disk would hit something."""

    def start(self, bb):
        self.x0, self.last, self.t0 = bb["robot"][:2].copy(), bb["t"] - 1.0, bb["t"]

    def update(self, bb):
        if bb["t"] - self.last < 0.1 - 1e-9:
            return RUNNING
        self.last = bb["t"]
        if bb["t"] - self.t0 > 10.0:             # time_allowance 10 s
            bb["cmd"] = (0.0, 0.0)
            return FAILURE
        r = bb["robot"]
        left = 0.30 - float(np.hypot(*(r[:2] - self.x0)))
        if left <= 0:
            bb["cmd"] = (0.0, 0.0)
            return SUCCESS
        s = np.arange(1, 21) * 0.015
        s = s[s < left]
        if np.any(gap(r[0] - s * math.cos(r[2]), r[1] - s * math.sin(r[2]), bb["world"]) < 0):
            bb["cmd"] = (0.0, 0.0)
            bb["backup_error_code"] = "COLLISION_AHEAD"
            return FAILURE
        bb["cmd"] = (-0.15, 0.0)
        return RUNNING

    cancel = staticmethod(stop)


def clear_costmap(which):
    def fn(bb):
        bb["cleared"].append((bb["t"], which))
        return SUCCESS
    return fn


def would_planner_help(bb):
    return SUCCESS if bb.get("compute_path_error_code") in ("NO_VALID_PATH", "TIMEOUT", "UNKNOWN") else FAILURE


def would_controller_help(bb):
    return SUCCESS if bb.get("follow_path_error_code") in (
        "UNKNOWN", "PATIENCE_EXCEEDED", "FAILED_TO_MAKE_PROGRESS", "NO_VALID_CONTROL") else FAILURE


def is_goal_nearby(bb):
    P = bb.get("path")
    if P is None:
        return FAILURE
    return SUCCESS if remaining_length(P, bb["robot"][:2]) < 4.0 else FAILURE


def validate_path(bb):
    P = bb.get("path")
    return SUCCESS if P is not None and path_valid(P, bb["world"], bb["robot"][:2]) else FAILURE


def default_tree():
    """navigate_to_pose_w_replanning_and_recovery.xml (main). The five selector nodes are one node here; the
    BackupWithReset subtree is its BackUp (the robot has not backed up before)."""
    succeed = lambda bb: SUCCESS
    fail = lambda bb: FAILURE
    compute = RecoveryNode("RecoveryNode", [
        Fallback("Fallback", [
            ReactiveSequence("ReactiveSequence", [
                Inverter("Inverter", [Leaf("GlobalUpdatedGoal", fail)]),
                Leaf("IsGoalNearby", is_goal_nearby),
                Leaf("TruncatePathLocal", succeed),
                Leaf("ValidatePath", validate_path)], label="CheckIfNewPathNeeded"),
            Action("ComputePathToPose", Planner())], label="FallbackComputePathToPose"),
        Sequence("Sequence", [Leaf("WouldAPlannerRecoveryHelp", would_planner_help),
                              Leaf("ClearEntireCostmap", clear_costmap("global"), label="ClearGlobalCostmap-Context")],
                 label="ContextualPlannerRecovery")], retries=1, label="ComputePathToPose (retry 1)")
    follow = RecoveryNode("RecoveryNode", [
        Action("FollowPath", Controller()),
        Sequence("Sequence", [Leaf("WouldAControllerRecoveryHelp", would_controller_help),
                              Leaf("ClearEntireCostmap", clear_costmap("local"), label="ClearLocalCostmap-Context")],
                 label="ContextualControllerRecovery")], retries=1, label="FollowPath (retry 1)")
    navigation = PipelineSequence("PipelineSequence", [
        Leaf("Selectors", succeed, label="5 selectors"),
        RateController("RateController", [compute], hz=1.0, label="RateController 1 Hz"),
        follow], label="NavigateWithReplanning")
    recovery = Sequence("Sequence", [
        Fallback("Fallback", [Leaf("WouldAControllerRecoveryHelp", would_controller_help, label="WouldAControllerRecoveryHelp "),
                              Leaf("WouldAPlannerRecoveryHelp", would_planner_help, label="WouldAPlannerRecoveryHelp ")],
                 label="Fallback (can a recovery help?)"),
        ReactiveFallback("ReactiveFallback", [
            Leaf("GoalUpdated", fail),
            RoundRobin("RoundRobin", [
                Sequence("Sequence", [Leaf("ClearEntireCostmap", clear_costmap("local"), label="ClearLocalCostmap-Subtree"),
                                      Leaf("ClearEntireCostmap", clear_costmap("global"), label="ClearGlobalCostmap-Subtree")],
                         label="ClearingActions"),
                Action("Spin", Spin(1.57), label="Spin 1.57 rad"),
                Action("Wait", Wait(5.0), label="Wait 5 s"),
                Action("BackUp", BackUp(), label="BackUp 0.30 m")], label="RecoveryActions")],
            label="RecoveryFallback")], label="Recovery")
    return RecoveryNode("RecoveryNode", [navigation, recovery], retries=6, label="NavigateRecovery (retry 6)")


def mini_tree(kind="sequence"):
    """The core of the default tree with nothing else: [Path valid? or ComputePathToPose], then FollowPath, under a
    plain Sequence (BehaviorTree.CPP: continues from the running child) or a PipelineSequence (re-ticks the
    children before it)."""
    first = Fallback("Fallback", [Leaf("ValidatePath", validate_path, label="Path valid?"),
                                  Action("ComputePathToPose", Planner())], label="Fallback")
    kids = [first, Action("FollowPath", Controller())]
    return Sequence("Sequence", kids, label="Sequence") if kind == "sequence" else \
        PipelineSequence("PipelineSequence", kids, label="PipelineSequence")


# ---------------------------------------------------------------- one run
GAP_PERSON = np.array([3.05, 3.5])                 # left of the door, in the gap between the table corner and the wall
TROLLEY = np.array([(5.35, 2.65), (5.75, 2.65), (5.75, 3.3), (5.35, 3.3)])   # between the table and the cabinet


def run(t_end=40.0, person=None, t_in=None, t_out=None, trolley=False, goal=GOAL, start=START, keep=1, goals=None,
        stuck_at=None, pause=0.2, tree_fn=None):
    """Tick the tree every 10 ms; the robot follows the last command, its turn rate changing at once (as RO-058's
    robot's does) and its forward speed by at most 0.5 m/s^2 (backing up starts at once). goals: several goal poses
    in turn, as the waypoint follower sends them (a new NavigateToPose goal each, 0.2 s pause after each success,
    the next goal after a failure: stop_on_failure false). stuck_at: from this time the base does not move (a wheel
    caught). Returns the per-tick records and each goal's result."""
    goals = [goal] if goals is None else goals
    bb = dict(t=0.0, robot=np.array(start, float), path=None, cmd=(0.0, 0.0),
              world=dict(person=None, trolley=TROLLEY if trolley else None), planned=[], cleared=[], halted=[], log=[])
    v = 0.0
    out, results = [], []
    k = 0
    for gi, g in enumerate(goals):
        tree = (tree_fn or default_tree)()
        for i, (n, _) in enumerate(tree.walk()):
            n.uid = i
        bb.update(goal=np.array(g, float), path=None, compute_path_error_code=None, follow_path_error_code=None)
        status, t_goal, pause_left = RUNNING, bb["t"], None
        while bb["t"] <= t_end + 1e-9:
            here = person is not None and t_in is not None and \
                t_in - 1e-9 <= bb["t"] < (t_out if t_out else 1e9) - 1e-9
            bb["world"]["person"] = person if here else None
            bb["log"] = []
            if pause_left is None:
                status = tree.execute_tick(bb)
                if status != RUNNING:
                    results.append(dict(goal=gi, status=status, t0=t_goal, t=bb["t"]))
                    bb["cmd"] = (0.0, 0.0)
                    pause_left = round(pause / DT) if status == SUCCESS and gi < len(goals) - 1 else 0
            if k % keep == 0 or status != RUNNING:
                out.append(dict(t=round(bb["t"], 2), robot=bb["robot"].copy(), path=bb["path"], goal=gi,
                                status={n.uid: n.status for n, _ in tree.walk()}, log=list(bb["log"]), cmd=bb["cmd"],
                                person=bb["world"]["person"], tree_status=status, checkers=bb.get("checkers")))
            if pause_left == 0:
                break
            # the base executes the last command for 10 ms
            cv, cw = bb["cmd"]
            v = float(np.clip(cv, v - 0.5 * DT, v + 0.5 * DT)) if cv >= 0 and v >= 0 else cv
            if stuck_at is not None and bb["t"] >= stuck_at - 1e-9:
                v, cw = 0.0, 0.0
            r = bb["robot"]
            r[0] += v * math.cos(r[2]) * DT
            r[1] += v * math.sin(r[2]) * DT
            r[2] = float(bk.wrap(r[2] + cw * DT))
            bb["t"] = round(bb["t"] + DT, 10)
            k += 1
            if pause_left:
                pause_left -= 1
                if pause_left == 0:
                    break
        else:
            break
    last = results[-1]["status"] if results else RUNNING
    return dict(records=out, tree=tree, planned=bb["planned"], cleared=bb["cleared"], halted=bb["halted"],
                status=last, t=bb["t"], results=results)


# ---------------------------------------------------------------- the Note's runs
WAYPOINTS = [(6.0, 2.0, math.radians(90)), (4.6, 3.5, math.radians(180)), (1.5, 2.0, math.radians(180))]
T_PERSON, T_LEAVES, STUCK_AT = 2.4, 8.0, 2.0


def results():
    """Every run of the Note, cached: the clear room; RO-058's person at 2.4 s; the blocked door (person in the gap
    at 2.4 s, trolley, the person leaves at 8.0 s); the person stays; a wheel stuck from 2.0 s; three waypoints with
    the person and the trolley there from the start; the two small trees of Section 4 on the person run."""
    import hashlib
    import pickle
    from pathlib import Path
    here = Path(__file__).parent        # cached by this file's and bandkit's text, so a code change reruns
    key = hashlib.sha1((here / "btkit.py").read_bytes() + (here / "bandkit.py").read_bytes()).hexdigest()[:12]
    f = Path(f"/tmp/ro079_cache/bt_{key}.pkl")
    if f.exists():
        return pickle.load(open(f, "rb"))
    R = dict(clear=run(t_end=60), person=run(person=bk.PERSON, t_in=T_PERSON, t_end=60),
             blocked=run(person=GAP_PERSON, t_in=T_PERSON, t_out=T_LEAVES, trolley=True, t_end=60),
             stays=run(person=GAP_PERSON, t_in=T_PERSON, trolley=True, t_end=60),
             stuck=run(stuck_at=STUCK_AT, t_end=25),
             waypoints=run(person=GAP_PERSON, t_in=0.0, trolley=True, goals=WAYPOINTS, t_end=120),
             mini_seq=run(person=bk.PERSON, t_in=T_PERSON, t_end=3.1, tree_fn=lambda: mini_tree("sequence")),
             mini_pipe=run(person=bk.PERSON, t_in=T_PERSON, t_end=3.1, tree_fn=lambda: mini_tree("pipeline")))
    for r in R.values():
        r.pop("tree")
    f.parent.mkdir(exist_ok=True)
    pickle.dump(R, open(f, "wb"))
    return R


if __name__ == "__main__":
    import sys
    if len(sys.argv) > 1:
        # the four control rules on tiny trees
        bb = dict(t=0.0, log=[])
        ok, no = (lambda b: SUCCESS), (lambda b: FAILURE)
        assert Fallback("f", [Leaf("a", no), Leaf("b", ok)]).execute_tick(bb) == SUCCESS
        assert Sequence("s", [Leaf("a", ok), Leaf("b", no)]).execute_tick(bb) == FAILURE
        rr = RoundRobin("r", [Leaf("a", ok), Leaf("b", ok)])
        rr.execute_tick(bb)
        rr.reset_status()
        assert rr.idx == 1                      # the next recovery is the next child
        p, c = astar(START, GOAL, dict(person=None, trolley=None))
        assert c is None and len(p) > 10
        print("self-check passed")
