import numpy as np
from collections import deque
import alg_ahuja_orlin_shortest_path

class AhujaOrlinLayeredNetworksAlgorithm(alg_ahuja_orlin_shortest_path.AhujaOrlinShortestPathAlgorithm):
    """Alg Ahuja-Orlin retele stratificate O(n*sqr(m))"""
    def __init__(self, num_nodes, source, sink):
        super().__init__(num_nodes, source, sink)
        self.layered_network_flags = [0] * num_nodes

    def initialize_layered_network_flags(self):
        self.layered_network_flags = [0] * self.num_nodes

    def calculate_layered_network_on_residual(self, residual_network, capacity_matrix):
        x = self.source_node
        while self.exact_distance_labels[self.source_node] < self.num_nodes:
            if self.layered_network_flags[self.source_node] == 0:
                y = 0
                admissible_arc_exists = False
                while y < self.num_nodes:
                    if (residual_network[x][y] > 0 and
                        self.exact_distance_labels[x] == self.exact_distance_labels[y] + 1 and
                        self.layered_network_flags[y] == 0):
                        
                        admissible_arc_exists = True
                        self.predecessor_nodes[y] = x
                        x = y
                        if x == self.sink_node:
                            residual_network = self.update_residual_network(residual_network)

                            for i in range(self.num_nodes):
                                print(residual_network[i])

                            x = self.source_node
                            self.predecessor_nodes = [-1] * self.num_nodes
                        break
                    y += 1
                if not admissible_arc_exists:
                    self.layered_network_flags[x] = 1
                    if x != self.source_node:
                        x = self.predecessor_nodes[x]
            else:
                self.calculate_exact_distances_BFS(residual_network)
                print(self.exact_distance_labels)
                self.initialize_layered_network_flags()

        return residual_network

    def execute_ahuja_orlin_layered_networks(self, capacity_matrix):
        flow_matrix = np.zeros((self.num_nodes, self.num_nodes), dtype=int)
        residual_network = self.calculate_initial_residual_network(self.num_nodes, flow_matrix, capacity_matrix)
        for i in range(self.num_nodes):
            print(residual_network[i])

        # Initialize exact distance labels and layered network flags
        self.calculate_exact_distances_BFS(capacity_matrix)
        self.initialize_layered_network_flags()

        # Apply layered networks algorithm
        residual_network = self.calculate_layered_network_on_residual(residual_network, capacity_matrix)

        # Display the residual network
        for i in range(self.num_nodes):
            print(residual_network[i])

        max_flow_matrix = self.calculate_max_flow(flow_matrix, capacity_matrix, residual_network)
        self.display_max_flow_and_capacity(max_flow_matrix, capacity_matrix)
