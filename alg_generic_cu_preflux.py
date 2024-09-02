import numpy as np
import random
import alg_ahuja_orlin_shortest_path

class GenericPreflowAlgorithm(alg_ahuja_orlin_shortest_path.AhujaOrlinShortestPathAlgorithm):
    def __init__(self, num_nodes, source, sink):
        super().__init__(num_nodes, source, sink)
        self.node_excesses = []

    def calculate_node_excess(self, flow_matrix, node):
        excess = 0
        for i in range(self.num_nodes):
            excess += flow_matrix[i][node] - flow_matrix[node][i]  # total inflow - total outflow for the node
        return excess

    def initialize_node_excesses(self, flow_matrix):
        self.node_excesses = [self.calculate_node_excess(flow_matrix, i) for i in range(self.num_nodes)]
        print(self.node_excesses)

    def get_active_nodes(self):
        return [i for i in range(self.num_nodes) if i != self.source_node and i != self.sink_node and self.node_excesses[i] > 0]

    def calculate_residual_network_with_preflows(self, flow_matrix, capacity_matrix, residual_network):
        for i in range(self.num_nodes):
            if residual_network[self.source_node][i] > 0:
                flow_matrix[self.source_node][i] = capacity_matrix[self.source_node][i]
                residual_network[i][self.source_node] = residual_network[self.source_node][i]
                residual_network[self.source_node][i] = 0

        self.exact_distance_labels[self.source_node] = self.num_nodes

        self.initialize_node_excesses(flow_matrix)
        active_nodes = self.get_active_nodes()

        while active_nodes:
            random_index = random.randint(0, len(active_nodes) - 1)
            current_node = active_nodes[random_index]
            print(f"randomElement: {current_node}")

            y = 0

            while y < self.num_nodes:
                if (residual_network[current_node][y] > 0 and
                        self.exact_distance_labels[current_node] == self.exact_distance_labels[y] + 1):
                    min_flow = min(self.node_excesses[current_node], residual_network[current_node][y])

                    self.node_excesses[current_node] -= min_flow
                    self.node_excesses[y] += min_flow
                    residual_network[current_node][y] -= min_flow
                    residual_network[y][current_node] += min_flow

                    break
                y += 1

            if y == self.num_nodes:
                self.calculate_dx_by_min_dy(residual_network, current_node)
                print(self.exact_distance_labels)

            active_nodes = self.get_active_nodes()

        return residual_network

    def execute_generic_preflow_algorithm(self, capacity_matrix):
        flow_matrix = np.zeros((self.num_nodes, self.num_nodes), dtype=int)
        residual_network = self.calculate_initial_residual_network(self.num_nodes, flow_matrix, capacity_matrix)
        for row in residual_network:
            print(row)

        self.calculate_exact_distances_BFS(capacity_matrix)

        residual_network = self.calculate_residual_network_with_preflows(flow_matrix, capacity_matrix, residual_network)

        for row in residual_network:
            print(row)

        max_flow_matrix = self.calculate_max_flow(flow_matrix, capacity_matrix, residual_network)
        self.display_max_flow_and_capacity(max_flow_matrix, capacity_matrix)
