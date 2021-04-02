# Course: CS261 - Data Structures
# Author: Marcus Knightley
# Assignment: 6, Part 1
# Description: Create an undirected Graph with methods to perform BFS and DFS searches

import heapq
from collections import deque


class UndirectedGraph:
    """
    Class to implement undirected graph
    - duplicate edges not allowed
    - loops not allowed
    - no edge weights
    - vertex names are strings
    """

    def __init__(self, start_edges=None):
        """
        Store graph info as adjacency list
        DO NOT CHANGE THIS METHOD IN ANY WAY
        """
        self.adj_list = dict()

        # populate graph with initial vertices and edges (if provided)
        # before using, implement add_vertex() and add_edge() methods
        if start_edges is not None:
            for u, v in start_edges:
                self.add_edge(u, v)

    def __str__(self):
        """
        Return content of the graph in human-readable form
        DO NOT CHANGE THIS METHOD IN ANY WAY
        """
        out = [f'{v}: {self.adj_list[v]}' for v in self.adj_list]
        out = '\n  '.join(out)
        if len(out) < 70:
            out = out.replace('\n  ', ', ')
            return f'GRAPH: {{{out}}}'
        return f'GRAPH: {{\n  {out}}}'

    # ------------------------------------------------------------------ #

    def add_vertex(self, v: str) -> None:
        """
        Add new vertex to the graph
        """
        # if c is already in the graph, do nothing
        if v in self.adj_list:
            return
        # otherwise, add the vertex with an empty list
        else:
            self.adj_list[v] = []

    def add_edge(self, u: str, v: str) -> None:
        """
        Add edge to the graph
        """
        # check if v or u is not already in the graph
        if u == v:
            return
        if v not in self.adj_list or u not in self.adj_list:
            # if true, add whichever is missing
            if v != u:
                self.add_vertex(u)
                self.add_vertex(v)
        # if the u and v keys are the same, do nothing

        # v and u already have an edge, do nothing
        elif v in self.adj_list[u] and u in self.adj_list[v]:
            return
        # add an edge between the vertices
        self.adj_list[u].append(v)
        self.adj_list[v].append(u)

    def remove_edge(self, v: str, u: str) -> None:
        """
        Remove edge from the graph
        """
        if v not in self.adj_list or u not in self.adj_list:
            return
        # if the vertices have an edge between them, then remove the edge
        elif v in self.adj_list[u] and u in self.adj_list[v]:
            self.adj_list[u].remove(v)
            self.adj_list[v].remove(u)
        # otherwise, do nothing
        else:
            return

    def remove_vertex(self, v: str) -> None:
        """
        Remove vertex and all connected edges
        """
        # check if the vertex exists in the graph, if not, do nothing
        if v not in self.adj_list:
            return
        else:
            # otherwise first, remove the vertex's edges, then remove the vertex from the graph
            for i in self.adj_list[v]:
                self.adj_list[i].remove(v)
            del self.adj_list[v]

    def get_vertices(self) -> []:
        """
        Return list of vertices in the graph (any order)
        """
        vertex_list = []  # initialise the vertex list
        # return the empty list if the graph is empty
        if len(self.adj_list) == 0:
            return vertex_list
        for k in self.adj_list:
            vertex_list.append(k)
        return vertex_list

    def get_edges(self) -> []:
        """
        Return list of edges in the graph (any order)
        """
        edge_list = []  # initialise the edge list
        # return the empty list if the graph is empty
        if len(self.adj_list) == 0:
            return edge_list

        # initialise an empty tumple to hold each edge
        edge_tuple = ()
        for i in self.adj_list:
            for k in self.adj_list[i]:
                edge_tuple = (i, k)
                rev_tuple = (k, i)  # create a reverse reverse direction of the same edge
                if rev_tuple not in edge_list:  # check if the same edge isnt already in the list
                    edge_list.append(edge_tuple)
        return edge_list

    def is_valid_path(self, path: []) -> bool:
        """
        Return true if provided path is valid, False otherwise
        """
        len_path = len(path)
        if len_path == 0:
            return True
        elif path[0] not in self.adj_list:
            return False
        elif len_path == 1:
            return True
        counter = 0
        k = 0
        while k < len_path - 1:
            if path[k + 1] in self.adj_list[path[k]]:
                counter += 1
            k += 1
        if counter == len_path - 1:
            return True
        else:
            return False

    def dfs(self, v_start, v_end=None) -> []:
        """
        Return list of vertices visited during DFS search
        Vertices are picked in alphabetical order
        """
        return_list = []
        if v_start not in self.adj_list:
            return []
        return_list.append(v_start)
        if v_start == v_end:
            return return_list
        sorted_list = sorted(self.adj_list[v_start])
        vertex_list = deque(sorted_list)
        while vertex_list:
            first_val = vertex_list.popleft()
            if first_val not in return_list:
                return_list.append(first_val)
                if first_val == v_end:
                    return return_list
                sorted_list = sorted(self.adj_list[first_val])
                for i in range(len(sorted_list)-1,-1,-1):
                    vertex_list.appendleft(sorted_list[i])

        return return_list


    def bfs(self, v_start, v_end=None) -> []:
        """
        Return list of vertices visited during BFS search
        Vertices are picked in alphabetical order
        """
        return_list = []
        if v_start not in self.adj_list:
            return []
        return_list.append(v_start)
        if v_start == v_end:
            return return_list

        sorted_list = sorted(self.adj_list[v_start])
        vertex_list = deque(sorted_list)
        while vertex_list:
            first_val = vertex_list.popleft()
            if first_val not in return_list:
                return_list.append(first_val)
                if first_val == v_end:
                    return return_list
                sorted_list = sorted(self.adj_list[first_val])
                vertex_list.extend(sorted_list)
        return return_list

    def count_connected_components(self):
        """
        Return number of connected componets in the graph
        """
        visit_dict = {} # initiate to store the visited vertices
        connected = [] # create a list each connected components
        for i in self.adj_list: # initiate all the initial value of the visit list to False
            visit_dict[i] = False
        for node in self.adj_list: # loop the graph list to check eac vertex and find and connected connected components to the list
            if visit_dict[node] is False:
                temp = []
                connected.append(self.count_helper(temp, node, visit_dict))
        return len(connected)  # return the length of the connected list

    def count_helper(self, temp, vertex, visit_dict):
        """Helper method to store the connected components into the connected list"""
        # add the vertex to the visit list
        visit_dict[vertex] = True
        # store the vertex to temp list
        temp.append(vertex)
        # repeat for all vertices adjacent to this vertex
        for i in self.adj_list[vertex]:
            if visit_dict[i] is False:
                temp = self.count_helper(temp, i, visit_dict)
        return temp

    def has_cycle(self):
        """
        Return True if graph contains a cycle, False otherwise
        """
        visit_dict = {} # initialise a dict to store mark vertices as true or false
        for node in self.adj_list: # assign a bool False to all vertices
            visit_dict[node] = False
        for node in self.adj_list:  # check all the vertices of the graph to detect a cycle
            if visit_dict[node] is False:
                if self.cycle_helper(node,visit_dict,prev_node=None) is True:
                    return True
        return False

    def cycle_helper(self,vertex,visit_dict,prev_node):
        """Helper method to find if subgraphs have any cycles"""
        visit_dict[vertex] = True
        for i in self.adj_list[vertex]:
            if visit_dict[i] is False:
                if self.cycle_helper(i,visit_dict,vertex):
                    return True
            elif prev_node != i:
                return True

