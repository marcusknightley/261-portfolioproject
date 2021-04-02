# Course: CS261 - Data Structures
# Author: Marcus Knightley
# Assignment: 6, Part 2
# Description: Create a directed graph with methods to perform BFS and DFS searches

import heapq
from collections import deque


class DirectedGraph:
    """
    Class to implement directed weighted graph
    - duplicate edges not allowed
    - loops not allowed
    - only positive edge weights
    - vertex names are integers
    """

    def __init__(self, start_edges=None):
        """
        Store graph info as adjacency matrix
        DO NOT CHANGE THIS METHOD IN ANY WAY
        """
        self.v_count = 0
        self.adj_matrix = []

        # populate graph with initial vertices and edges (if provided)
        # before using, implement add_vertex() and add_edge() methods
        if start_edges is not None:
            v_count = 0
            for u, v, _ in start_edges:
                v_count = max(v_count, u, v)
            for _ in range(v_count + 1):
                self.add_vertex()
            for u, v, weight in start_edges:
                self.add_edge(u, v, weight)

    def __str__(self):
        """
        Return content of the graph in human-readable form
        DO NOT CHANGE THIS METHOD IN ANY WAY
        """
        if self.v_count == 0:
            return 'EMPTY GRAPH\n'
        out = '   |'
        out += ' '.join(['{:2}'.format(i) for i in range(self.v_count)]) + '\n'
        out += '-' * (self.v_count * 3 + 3) + '\n'
        for i in range(self.v_count):
            row = self.adj_matrix[i]
            out += '{:2} |'.format(i)
            out += ' '.join(['{:2}'.format(w) for w in row]) + '\n'
        out = f"GRAPH ({self.v_count} vertices):\n{out}"
        return out

    # ------------------------------------------------------------------ #

    def add_vertex(self) -> int:
        """
        add a vertex to the graph
        """
        self.adj_matrix.append([])
        count = self.v_count
        if count == 0:
            self.adj_matrix[count].append(0)
            self.v_count += 1
            return self.v_count
        for i in range(0,count):
            self.adj_matrix[i].append(0)
        for k in range(count+1):
            self.adj_matrix[count].append(0)
        self.v_count += 1
        return self.v_count


    def add_edge(self, src: int, dst: int, weight=1) -> None:
        """
        Add an edge between two vertices with the given weight
        """
        if 0 > src or src > (len(self.adj_matrix)-1) or dst < 0 or dst > (len(self.adj_matrix)-1):
            return
        elif weight < 1:
            return
        elif src == dst:
            return

        self.adj_matrix[src][dst] = weight

    def remove_edge(self, src: int, dst: int) -> None:
        """
        If there is an edge between the two vertices, remove the edge
        """
        if src < 0 or dst < 0 or src > (self.v_count-1) or dst > (self.v_count-1):
            return
        elif self.adj_matrix[src][dst] == 0:
            return
        else:
            self.adj_matrix[src][dst] = 0

    def get_vertices(self) -> []:
        """
        Return a list of the vertices
        """
        v_list = []
        for i in range(len(self.adj_matrix)):
            v_list.append(i)
        return v_list


    def get_edges(self) -> []:
        """
        return a list of tuples containing the vertices and their edge if there is an edge between the vertices
        """
        return_list = []
        for i in range(len(self.adj_matrix)):  # loop the matrix to visit each vertex
            for k in range(len(self.adj_matrix[i])):
                # check if there's an edge
                value = self.adj_matrix[i][k]
                if value != 0:
                    # if true, add a tuple into the return list
                    return_list.append((i, k, value))
        return return_list


    def is_valid_path(self, path: []) -> bool:
        """
        Check if a given path is valid in the matrix
        """
        if len(path) == 0:  # return true if the path is empty
            return True
        start_v = path[0]  # assign the first index value
        count = 1 # start the counter at 1
        for i in range(1,len(path)):  # loop through the indeces of the path
            path_index = path[i]
            # if the there is an edge between the two vertices, move the starting vertex to the path_index value and increment the count
            if self.adj_matrix[start_v][path_index] != 0:
                start_v = path_index
                count += 1
        if count == len(path):  # if the count covers the length of the path, then return true otherwise false
            return True
        else:
            return False


    def dfs(self, v_start, v_end=None) -> []:
        """
        Start a DFS search and return a list of visited
        """
        return_list = []
        # if the starting vertex is outside the vertex matrix, return the empty list
        if v_start < 0 or v_start >= len(self.adj_matrix):
            return return_list
        return_list.append(v_start)
        if v_start == v_end:
            return return_list
        # call the helper recursive function to check the neighbouring vertices of the given function
        self.dfs_trav(v_start,v_end,return_list)
        return return_list

    def dfs_trav(self,v_start,v_end,return_list):
        """Helper method to dfs search"""
        for i in range(self.v_count):
            if self.adj_matrix[v_start][i] != 0 and i not in return_list:
                return_list.append(i)
                if i == v_end:
                    return return_list
                self.dfs_trav(i,v_end,return_list)
        return return_list


    def bfs(self, v_start, v_end=None) -> []:
        """
         Perform a bfs search and return a list of vertices in the order they are visited
        """
        return_list = []
        if v_start < 0 or v_start >= len(self.adj_matrix):
            return return_list
        return_list.append(v_start)
        if v_start == v_end:
            return return_list
        vertex_list = deque()
        self.bfs_trav(v_start,v_end,return_list,vertex_list)
        return return_list

    def bfs_trav(self,v_start,v_end,return_list,vertex_list):
        """recursive funtion to help with the bfs"""
        for i in range(self.v_count):
            if self.adj_matrix[v_start][i] != 0 and i not in return_list:
                return_list.append(i)
                if i == v_end: # exit the method if the current vertex is equal to the end vertex
                    return return_list
                vertex_list.append(i)  # if there's an edge and the vertex is not in the list, add it
        if len(vertex_list) > 0: # if the vertex list is not empty, pop the next value and call the function recursively
            next_index = vertex_list.popleft()
            self.bfs_trav(next_index, v_end, return_list, vertex_list)
        else:
            return return_list


    def has_cycle(self):
        """
        Check if the graph has any cycles, if yes, return true
        """
        # initialise a visit list to track vertices visited
        # initialise a return list to feed vertices into the recursion call
        visited_list = [False] * self.v_count
        return_list = [False] * self.v_count
        # check for each vertex of the graph if it is visited
        for vertex in range(self.v_count):
            if visited_list[vertex] is False:
                # if false, check check for each indices of the vertex
                if self.rec_cycle(vertex,visited_list,return_list) is True:
                    return True
        return False

    def rec_cycle(self, vertex, visited_list, return_list):
        """recursively check the indices of a vertex to detec a cycle"""
        visited_list[vertex] = True
        return_list[vertex] = True
        for node in range(len(self.adj_matrix[vertex])):
            if self.adj_matrix[vertex][node] != 0:
                if visited_list[node] is False:
                    if self.rec_cycle(node, visited_list, return_list) is True:
                        return True
                elif return_list[node] is True:
                    return True
        return_list[vertex] = False
        return False


    def dijkstra(self, src: int) -> []:
        """
        Find the shortest path from source vertex to each vertex is the graph
        """
        dist = [float('inf')] * self.v_count  # assign all values of the distance list to infinity
        dist[src] = 0  # then assign 0 to the starting index
        sp_list = [False] * self.v_count  # initialise the shortes path list with False values
        # loop through the vertices to check the minimum values of each index
        for node in range(self.v_count):
            # get the index with the minimum value
            first_v = self.min_dist(dist,sp_list)
            sp_list[first_v] = True  # mark the index as visited in the shortest path list

            for k in range(self.v_count):
                # check if the path value of the index in the given vertex, check if the current path value plus the new path value is less than the existing distance value
                # also check if the vertex is not already in the shortest path list
                if self.adj_matrix[first_v][k] > 0 and dist[k] > (dist[first_v] + self.adj_matrix[first_v][k]) and sp_list[k] is False:
                    # if true, assign the new path value to the given index for the vertex
                    dist[k] = dist[first_v] + self.adj_matrix[first_v][k]

        return dist

    def min_dist(self,dist,sp_list):
        """Helper method to find the index with the minimum distance from an index that is not in the shortest path list"""
        min_value = float('inf')  # assign the infinity value to be the biggest possible value
        min_index = 0
        for vertex in range(self.v_count):
            if dist[vertex] < min_value and sp_list[vertex] is False:
                min_value = dist[vertex] # if the min_value is greater than the actual distance value, assign the actual distance value to min_value
                min_index = vertex
        return min_index

