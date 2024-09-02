import numpy as np
import generic_dmf_algorithm 

class CapacityScalingAlgorithm(generic_dmf_algorithm.GenericDMFAlgorithm):
    """Alg de scalare de excess O(sqr(n)*logC+n*m)"""
    def __init__(self, num_nodes, source, sink, flow_matrix, capacity_matrix):
        super().__init__(num_nodes, source, sink)
        self.residual_network = self.calculate_initial_residual_network(self.num_nodes, flow_matrix, capacity_matrix)
        self.calculate_max_capacity(capacity_matrix)
        self.calculate_scaled_capacity()

    def calculate_max_capacity(self, capacity_matrix):
        self.max_capacity = 0
        for i in range(self.num_nodes):
            max_from_current_row = np.max(capacity_matrix[i])
            if self.max_capacity < max_from_current_row:
                self.max_capacity = max_from_current_row

    def calculate_scaled_capacity(self):
        self.scaled_capacity = 1
        while self.scaled_capacity < self.max_capacity:
            self.scaled_capacity *= 2
        if self.scaled_capacity > self.max_capacity:
            self.scaled_capacity //= 2

    def calculate_scaled_residual_network(self, residual_network):
        scaled_residual_network = np.zeros((self.num_nodes, self.num_nodes), dtype=int)
        for i in range(self.num_nodes):
            for j in range(self.num_nodes):
                if residual_network[i][j] >= self.scaled_capacity:
                    scaled_residual_network[i][j] = residual_network[i][j]
        return scaled_residual_network

    def update_residual_network(self, scaled_residual_network):
        for i in range(self.num_nodes):
            for j in range(self.num_nodes):
                if scaled_residual_network[i][j] != 0:
                    self.residual_network[i][j] = scaled_residual_network[i][j]

    def calculate_max_flow_scaled_residual_network(self):
        scaled_residual_network = np.zeros((self.num_nodes, self.num_nodes), dtype=int)
        while self.scaled_capacity >= 1:
            scaled_residual_network = self.calculate_residual_network_for_max_flow(
                self.calculate_scaled_residual_network(self.residual_network)
            )
            print("Scaled residual network:")
            print(scaled_residual_network)
            self.update_residual_network(scaled_residual_network)
            print(self.residual_network)
            self.scaled_capacity //= 2
        return scaled_residual_network

    def execute_capacity_scaling_algorithm(self, flow_matrix, capacity_matrix):
        print("Initial residual network:")
        print(self.residual_network)
        print("Maximum capacity:", self.max_capacity)
        print("Scaled capacity:", self.scaled_capacity)

        print("Scaled residual network AFTER algorithm:")
        residual_network = self.calculate_max_flow_scaled_residual_network()
        for i in range(self.num_nodes):
            for j in range(self.num_nodes):
                print(residual_network[i][j], end=" ")
            print()

        # Calculate max flow and display
        max_flow_matrix = self.calculate_max_flow(flow_matrix, capacity_matrix, residual_network)
        self.display_max_flow_and_capacity(max_flow_matrix, capacity_matrix)
