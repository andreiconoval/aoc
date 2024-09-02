import numpy as np
from collections import deque
import generic_dmf_algorithm

class AhujaOrlinShortestPathAlgorithm(generic_dmf_algorithm.GenericDMFAlgorithm):
    """Alg Ahuja-Orlin etichete de distanta O(n*sqr(m))"""
    def __init__(self, num_nodes, source, sink):
        super().__init__(num_nodes, source, sink)
        self.exact_distance_labels = [-1] * num_nodes
        self.exact_distance_labels[-1] = 0

    def calculate_exact_distances_BFS(self, capacity_matrix):
        visited = [False] * self.num_nodes
        queue = deque([self.sink_node])
        visited[self.sink_node] = True

        current_node = self.sink_node
        self.exact_distance_labels[0] = self.num_nodes + 1

        while not visited[self.source_node] and queue:
            for i in range(self.num_nodes - 2, -1, -1):
                if not visited[i] and capacity_matrix[i][current_node] > 0:
                    visited[i] = True
                    queue.append(i)
                    self.exact_distance_labels[i] = self.exact_distance_labels[current_node] + 1
            queue.popleft()
            if queue:
                current_node = queue[0]

        print(self.exact_distance_labels)

    def calculate_dx_by_min_dy(self, residual_network, x):
        min_val = self.num_nodes + 1
        for i in range(self.num_nodes):
            if residual_network[x][i] > 0 and self.exact_distance_labels[i] + 1 < min_val:
                min_val = self.exact_distance_labels[i] + 1

        self.exact_distance_labels[x] = min_val

    def calculate_shortest_path_on_residual_network(self, residual_network, capacity_matrix):
        x = self.source_node
        while self.exact_distance_labels[self.source_node] < self.num_nodes:
            y = 0
            while y < self.num_nodes:
                if (residual_network[x][y] > 0 and
                    self.exact_distance_labels[x] == self.exact_distance_labels[y] + 1):
                    self.predecessor_nodes[y] = x
                    x = y
                    if x == self.sink_node:
                        residual_network = self.update_residual_network(residual_network)

                        for i in range(self.num_nodes):
                            print(residual_network[i])

                        x = self.source_node
                        self.predecessor_nodes = [-1] * self.num_nodes
                    y = -1
                y += 1
            if y == self.num_nodes:
                self.calculate_dx_by_min_dy(residual_network, x)
                print(self.exact_distance_labels)

                if x != self.source_node:
                    x = self.predecessor_nodes[x]

    def execute_ahuja_orlin_shortest_path(self, capacity_matrix):
        flow_matrix = np.zeros((self.num_nodes, self.num_nodes), dtype=int)
        residual_network = self.calculate_initial_residual_network(self.num_nodes, flow_matrix, capacity_matrix)
        for i in range(self.num_nodes):
            print(residual_network[i])

        self.calculate_exact_distances_BFS(capacity_matrix)
        self.calculate_shortest_path_on_residual_network(residual_network, capacity_matrix)

        for i in range(self.num_nodes):
            print(residual_network[i])

        max_flow_matrix = self.calculate_max_flow(flow_matrix, capacity_matrix, residual_network)
        self.display_max_flow_and_capacity(max_flow_matrix, capacity_matrix)
