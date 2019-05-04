"""
A weighted graph implemented as a dictionary of key = vertex, value = dictionary.
    Inner dictionary: key = vertex has edge to. Value is weight of edge.
    Method for storing edges: Adjacency list
"""
import math
from operator import itemgetter


class Graph:
    """
    The graph has pathﬁnding capabilities. It is able to ﬁnd the minimum weight path between two vertices.
    It also can report if it is bipartite using a graph coloring algorithm.
    An edge connects two vertices, u and v, and speciﬁes a weight on that connection, w.
    Edges are undirected and, therefore, symmetric; (u,v,w) means the same thing as (v,u,w).
    """

    def __init__(self, n):
        """
        Constructor
        :param n: Number of vertices
        """
        self.order = n
        self.size = 0
        # You may put any required initialization code here
        self.graph = {}
        # Make inner dict for each vertex
        for i in range(self.order):
            self.graph[i] = {}

    def insert_edge(self, u, v, w):
        """
        Function to create a new edge in the graph
        :param u: Start vertex
        :param v: End vertex
        :param w: Weight
        """
        # Vertex not in graph
        if u >= self.order or v >= self.order:
            raise IndexError
        # Weighted graph so need to insert in dict of u and v
        if v in self.graph[u]:
            # Set new weight
            self.graph[u][v] = w
            self.graph[v][u] = w
        else:
            # Add vertex and weight
            self.graph[u][v] = w
            self.graph[v][u] = w
            self.size += 1

    def degree(self, v):
        """
        Get the degree of vertex
        :param v: Vertex to get
        :return: Degree of v
        """
        # Vertex not in graph
        if v >= self.order:
            raise IndexError
        # Number of degrees is number of values for v
        return len(self.graph[v])

    def are_connected(self, u, v):
        """
        See if two vertices are connected
        :param u: Start vertex
        :param v: End vertex
        :return: True if connected, False otherwise
        """
        # Vertex not in graph
        if u >= self.order or v >= self.order:
            raise IndexError
        # Will return True if v is a key in the inner dict
        return v in self.graph[u]

    def is_path_valid(self, path):
        """
        See if path valid
        :param path: List of vertices in order of path
        :return: True if valid, False otherwise
        """
        for i in range(len(path) - 1):
            # If not connected, not a path, return False
            if not self.are_connected(path[i], path[i + 1]):
                return False
        return True

    def edge_weight(self, u, v):
        """
        Get the weight of an edge between vertices
        :param u: Start vertex
        :param v: End vertex
        :return: Weight if connected, inf if not
        """
        # Vertex not in graph
        if u >= self.order or v >= self.order:
            raise IndexError
        if v in self.graph[u]:
            # Weight of connected vertices
            return self.graph[u][v]
        else:
            # Vertices not connected
            return math.inf

    def path_weight(self, path):
        """
        Get total weight of path
        :param path: List of vertices in path order
        :return: Total weight of path
        """
        weight = 0
        for i in range(len(path) - 1):
            # Add up weights of edges
            weight += self.edge_weight(path[i], path[i + 1])
        return weight

    def does_path_exist(self, u, v):
        """
        Check if there is a path between two vertices
        :param u: Start vertex
        :param v: End vertex
        :return: True if path exists, False otherwise
        """
        # Vertex not in graph
        if u >= self.order or v >= self.order:
            raise IndexError
        # Keep track of which vertices have edges to from u
        q = [u]
        # Keep track of which vertices visited
        visited = set()
        visited.add(u)
        # While vertices to visit
        while q:
            vertex = q.pop(0)
            # Found path
            if vertex == v:
                return True
            # Update q and visited
            for x in self.graph[vertex]:
                if x not in visited:
                    q.append(x)
                    visited.add(x)
        return False

    def find_min_weight_path(self, u, v):
        """
        Find minimum weight path if exists
        :param u: Start vertex
        :param v: End vertex
        :return: The minimum weight path if exists, raise IndexError if doesn't
        """
        dist = {}
        prior = {}
        nodes = set(i for i in range(self.order))
        # Initialize distances
        for i in range(self.order):
            dist[i] = math.inf

        dist[u] = 0
        prior[u] = u
        visited = set()
        # While haven't visited every node in self.order
        while visited != nodes:
            others = []
            # Keep track of possible paths
            for other in nodes - visited:
                others.append((other, dist[other]))
            x = sorted(others, key=itemgetter(1))[0][0]
            for y, dis in self.graph[x].items():
                # Update distances and priors for the vertices
                if dist[x] + dis < dist[y]:
                    dist[y] = dist[x] + dis
                    prior[y] = x
            # Update visited
            visited.add(x)
        # Raise ValueError if no path exists
        if v not in prior:
            raise ValueError

        # Create return list of minimum weight path
        path = []
        node = v
        while node != u:
            path.append(node)
            node = prior[node]
        path.append(u)
        path.reverse()
        return path

    def is_bipartite(self):
        """
        Determine if graph is bipartite
        :return: True if bipartite, False otherwise
        """
        # Create color array to store colors assigned to vertices
        # Value -1 means no color assigned to vertex
        # Value 1 means first color, 0 means second color
        color = {}
        for i in range(self.order):
            color[i] = -1
        q = []
        q.append(1)
        # Create FIFO queue of vertex and enqueue source vertex for BFS traversal
        while q:
            u = q.pop()
            # Return false if there is a self loop
            for k in self.graph[u]:
                if k == u:
                    return False
            # An edge from u to v exists and destination v is not colored
            for v in range(self.order):
                for x in self.graph[v]:
                    if x == u and color[v] == -1:
                        # Assign alternate color to adjacent v of u
                        color[v] = 1 - color[u]
                        q.append(v)
                    # Edge from u to v exists and destination v is colored w/ same color as u
                    elif x == u and color[v] == color[u]:
                        return False
        # All adjacent vertices can be colored w alternate color
        return True
