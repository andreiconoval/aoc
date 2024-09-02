from collections import deque
import numpy as np
import alg_generic_cu_preflux

class PreflowFIFOAlgorithm(alg_generic_cu_preflux.GenericPreflowAlgorithm):
    """Alg cu preflux FIFO O(n*n*n)"""
    def __init__(self, num_nodes, source, sink):
        super().__init__(num_nodes, source, sink)
        self.active_nodes_queue = deque()

    def calculate_residual_network_with_preflow_FIFO(self, flow_matrix, capacity_matrix, residual_network):
        for i in range(self.num_nodes):
            if residual_network[self.source_node][i] > 0:
                flow_matrix[self.source_node][i] = capacity_matrix[self.source_node][i]
                residual_network[i][self.source_node] = residual_network[self.source_node][i]
                residual_network[self.source_node][i] = 0

                if i != self.sink_node:
                    self.active_nodes_queue.append(i)

        self.exact_distance_labels[self.source_node] = self.num_nodes

        self.initialize_node_excesses(flow_matrix)

        while self.active_nodes_queue:
            current_node = self.active_nodes_queue.popleft()
            y = 0

            while self.node_excesses[current_node] > 0 and y < self.num_nodes:
                if (residual_network[current_node][y] > 0 and 
                        self.exact_distance_labels[current_node] == self.exact_distance_labels[y] + 1):
                    min_flow = min(self.node_excesses[current_node], residual_network[current_node][y])

                    self.node_excesses[current_node] -= min_flow
                    self.node_excesses[y] += min_flow
                    residual_network[current_node][y] -= min_flow
                    residual_network[y][current_node] += min_flow

                    if y not in self.active_nodes_queue and y != self.source_node and y != self.sink_node:
                        self.active_nodes_queue.append(y)

                    y = -1  # Reset to restart the loop
                y += 1

            if self.node_excesses[current_node] > 0:
                self.calculate_dx_by_min_dy(residual_network, current_node)
                print(self.exact_distance_labels)
                self.active_nodes_queue.append(current_node)

        return residual_network

    def execute_preflow_FIFO_algorithm(self, capacity_matrix):
        flow_matrix = np.zeros((self.num_nodes, self.num_nodes), dtype=int)
        residual_network = self.calculate_initial_residual_network(self.num_nodes, flow_matrix, capacity_matrix)
        for row in residual_network:
            print(row)

        self.calculate_exact_distances_BFS(capacity_matrix)
        residual_network = self.calculate_residual_network_with_preflow_FIFO(flow_matrix, capacity_matrix, residual_network)

        for row in residual_network:
            print(row)

        max_flow_matrix = self.calculate_max_flow(flow_matrix, capacity_matrix, residual_network)
        self.display_max_flow_and_capacity(max_flow_matrix, capacity_matrix)
