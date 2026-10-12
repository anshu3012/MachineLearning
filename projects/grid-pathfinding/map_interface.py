"""The one interface every map gives the search algorithms and the drawing code.

A map is a graph: places (nodes) joined by moves (edges) that cost metres. The algorithms in algorithms.py and the
drawing code only call the methods below, so they never know whether the map is a warehouse grid, a street graph or
a grid made from streets. A new kind of map is a new subclass that fills these in."""
import math

import networkx as nx


class Map:
    name = ""          # short name, used for file names
    label = ""         # what the drawing writes on the map, e.g. "Warehouse floor" or "Chicago"
    start = None       # the node a search starts from
    goal = None        # the node it must reach
    goals = ()         # the goals of the multi-goal search (e.g. charging docks or train stations)

    def nodes(self):
        """Every node of the map."""
        raise NotImplementedError

    def neighbours(self, node):
        """The nodes one move away from node."""
        raise NotImplementedError

    def cost(self, a, b):
        """The length of the move from a to its neighbour b, in metres."""
        raise NotImplementedError

    def xy(self, node):
        """Where the node is drawn: (x, y) in metres, x to the east (right), y to the north (up)."""
        raise NotImplementedError

    def heuristic(self, a, b):
        """The straight-line distance from a to b in metres. No route is shorter, so A* may use it as its guess."""
        return math.dist(self.xy(a), self.xy(b))

    def edge_xy(self, a, b):
        """The points of the drawn line from a to b (a curved street has more than two)."""
        return [self.xy(a), self.xy(b)]

    def route_length(self, route):
        """Total cost along a route given as a list of nodes."""
        return sum(self.cost(a, b) for a, b in zip(route, route[1:]))

    def to_networkx(self):
        """The same map as a networkx graph with edge weight "length", for checking our answers."""
        G = nx.Graph()
        for a in self.nodes():
            for b in self.neighbours(a):
                G.add_edge(a, b, length=self.cost(a, b))
        return G
