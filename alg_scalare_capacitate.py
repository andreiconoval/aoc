import numpy as np
import generic_dmf_algorithm

class CapacityScalingAlgorithm(generic_dmf_algorithm.GenericFlowAlgorithm):
    def __init__(self, node_count, source, sink, flow_matrix, capacity_matrix):
        # Initialize with the number of nodes, source, sink, flow matrix, and capacity matrix
        super().__init__(node_count, source, sink)
        self.residual_network = self.initialize_residual_network(flow_matrix, capacity_matrix)
        self.calculate_max_capacity(capacity_matrix)
        self.calculate_initial_r_bar()

    def calculate_max_capacity(self, capacity_matrix):
        # Calculate the maximum capacity in the capacity matrix
        self.max_capacity = np.max(capacity_matrix)

    def calculate_initial_r_bar(self):
        # Calculate the initial value of r_bar, the largest power of 2 less than or equal to max capacity
        self.r_bar = 1
        while self.r_bar < self.max_capacity:
            self.r_bar *= 2
        if self.r_bar > self.max_capacity:
            self.r_bar //= 2

    def calculate_r_bar_residual_network(self, residual_network):
        # Create a residual network considering only capacities >= r_bar
        r_bar_residual_network = np.zeros((self.node_count, self.node_count), dtype=int)
        for i in range(self.node_count):
            for j in range(self.node_count):
                if residual_network[i][j] >= self.r_bar:
                    r_bar_residual_network[i][j] = residual_network[i][j]
        return r_bar_residual_network

    def update_residual_network(self, r_bar_residual_network):
        # Update the residual network with the r_bar residual network values
        for i in range(self.node_count):
            for j in range(self.node_count):
                if r_bar_residual_network[i][j] != 0:
                    self.residual_network[i][j] = r_bar_residual_network[i][j]

    def calculate_residual_network_corresponding_to_max_flow(self):
        # Iteratively calculate the residual network corresponding to the maximum flow
        while self.r_bar >= 1:
            r_bar_residual_network = self.calculate_r_bar_residual_network(self.residual_network)
            r_bar_residual_network = self.calculate_max_flow_residual_network(r_bar_residual_network)
            print("r_bar residual network:")
            print(r_bar_residual_network)
            self.update_residual_network(r_bar_residual_network)
            print("Updated residual network:")
            print(self.residual_network)
            self.r_bar //= 2
        return r_bar_residual_network

    def run_capacity_scaling_algorithm(self, flow_matrix, capacity_matrix):
        # Display initial states
        print("Initial residual network:")
        print(self.residual_network)
        print("Maximum capacity C:", self.max_capacity)
        print("Initial r_bar:", self.r_bar)

        # Calculate the residual network using the capacity scaling algorithm
        final_residual_network = self.calculate_residual_network_corresponding_to_max_flow()
        print("Final r_bar residual network after algorithm:")
        for i in range(self.node_count):
            for j in range(self.node_count):
                print(final_residual_network[i][j], end=" ")
            print()

        # Calculate and display the maximum flow
        max_flow = self.calculate_max_flow(flow_matrix, capacity_matrix, final_residual_network)
        self.display_flow_and_capacity(max_flow, capacity_matrix)

    def display_flow_and_capacity(self, flow_matrix, capacity_matrix):
        # Display the flow matrix and the capacity matrix
        for i in range(self.node_count):
            for j in range(self.node_count):
                if capacity_matrix[i][j] > 0:
                    print(f"({i+1},{j+1}): flow = {flow_matrix[i][j]}, capacity = {capacity_matrix[i][j]}")
