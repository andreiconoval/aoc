import numpy as np
from heapq import heappush, heappop
import alg_generic_cu_preflux

class DistanceComparator:
    def __init__(self, distances):
        self.distances = distances

    def __call__(self, node):
        return -self.distances[node]  # Max heap, so negate the distance

class PreflowWithHighestLabelAlgorithm(alg_generic_cu_preflux.GenericPreflowAlgorithm):
    def __init__(self, num_nodes, source, sink):
        super().__init__(num_nodes, source, sink)
        self.active_nodes_heap = []

    def calculate_residual_network_with_highest_label_preflow(self, flow_matrix, capacity_matrix, residual_network):
        for i in range(self.num_nodes):
            if residual_network[self.source_node][i] > 0:
                flow_matrix[self.source_node][i] = capacity_matrix[self.source_node][i]
                residual_network[i][self.source_node] = residual_network[self.source_node][i]
                residual_network[self.source_node][i] = 0

        self.exact_distance_labels[self.source_node] = self.num_nodes

        self.initialize_node_excesses(flow_matrix)

        # Using a max-heap (priority queue)
        distance_comparator = DistanceComparator(self.exact_distance_labels)
        self.active_nodes_heap = []

        for i in range(self.num_nodes):
            if residual_network[i][self.source_node] > 0 and i != self.sink_node:
                heappush(self.active_nodes_heap, (distance_comparator(i), i))

        while self.active_nodes_heap:
            _, current_node = heappop(self.active_nodes_heap)
            y = 0

            while self.node_excesses[current_node] > 0 and y < self.num_nodes:
                if (residual_network[current_node][y] > 0 and 
                        self.exact_distance_labels[current_node] == self.exact_distance_labels[y] + 1):
                    min_flow = min(self.node_excesses[current_node], residual_network[current_node][y])

                    self.node_excesses[current_node] -= min_flow
                    self.node_excesses[y] += min_flow
                    residual_network[current_node][y] -= min_flow
                    residual_network[y][current_node] += min_flow

                    if y not in [self.source_node, self.sink_node] and not any(y == item[1] for item in self.active_nodes_heap):
                        heappush(self.active_nodes_heap, (distance_comparator(y), y))

                    y = -1  # Reset to restart the loop
                y += 1

            if self.node_excesses[current_node] > 0:
                self.calculate_dx_by_min_dy(residual_network, current_node)
                print(self.exact_distance_labels)

                if current_node not in [self.source_node, self.sink_node] and not any(current_node == item[1] for item in self.active_nodes_heap):
                    heappush(self.active_nodes_heap, (distance_comparator(current_node), current_node))

        return residual_network

    def execute_highest_label_preflow_algorithm(self, capacity_matrix):
        flow_matrix = np.zeros((self.num_nodes, self.num_nodes), dtype=int)
        residual_network = self.calculate_initial_residual_network(self.num_nodes, flow_matrix, capacity_matrix)

        for row in residual_network:
            print(row)

        self.calculate_exact_distances_BFS(capacity_matrix)
        residual_network = self.calculate_residual_network_with_highest_label_preflow(flow_matrix, capacity_matrix, residual_network)

        for row in residual_network:
            print(row)

        max_flow_matrix = self.calculate_max_flow(flow_matrix, capacity_matrix, residual_network)
        self.display_max_flow_and_capacity(max_flow_matrix, capacity_matrix)
