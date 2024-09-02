import numpy as np
from copy import deepcopy
import generic_dmf_algorithm

class BitScalingAlgorithm(generic_dmf_algorithm.GenericFlowAlgorithm):
    def __init__(self, node_count, source, sink, capacity_matrix):
        # Initialize with the number of nodes, source, sink, and initial capacity matrix
        super().__init__(node_count, source, sink)
        self.max_capacity = []
        self.capacity_matrix_stack = []
        self.current_step = 0
        self.capacity_matrix_stack.append(capacity_matrix)

    def calculate_max_capacity(self, capacity_matrix):
        # Calculate the maximum capacity in the capacity matrix
        max_capacity = np.max(capacity_matrix)
        self.max_capacity.append(max_capacity)

    def initialize_capacity_matrices(self, capacity_matrix):
        print(f"Maximum capacity: {self.max_capacity} for step k={self.current_step}")
        old_capacity_matrix = capacity_matrix  # Assume this is a list of lists

        while self.max_capacity[-1] > 1:
            new_capacity_matrix = [
                [old_capacity_matrix[i][j] // 2 for j in range(self.node_count)]
                for i in range(self.node_count)
            ]
            self.current_step += 1
            print(f"For k={self.current_step}, new capacity matrix:\n{new_capacity_matrix}")
            self.capacity_matrix_stack.append(new_capacity_matrix)

            self.calculate_max_capacity(new_capacity_matrix)
            print(f"Maximum capacity: {self.max_capacity[-1]} for step k={self.current_step}")
            old_capacity_matrix = new_capacity_matrix

    def run_bit_scaling_algorithm(self, initial_capacity_matrix):
        # Calculate the initial maximum capacity and initialize the capacity matrices
        self.calculate_max_capacity(initial_capacity_matrix)
        self.initialize_capacity_matrices(initial_capacity_matrix)

        # Initialize the flow matrix for the first step
        flow_matrix = np.zeros((self.node_count, self.node_count), dtype=int)
        print("Initial flow matrix:\n", flow_matrix)

        # Process each step from the highest bit level down to the original capacity matrix
        while self.current_step >= 0:
            current_capacity_matrix = self.capacity_matrix_stack[-1]
            residual_network = deepcopy(current_capacity_matrix)

            # Calculate the residual network corresponding to the maximum flow
            residual_network = self.calculate_max_flow_residual_network(residual_network)
            print(f"Current capacity matrix:\n{self.capacity_matrix_stack[-1]}")
            print(f"Residual network:\n{residual_network}")

            # Calculate the maximum flow and display it
            max_flow = self.calculate_max_flow(flow_matrix, current_capacity_matrix, residual_network)
            print(f"Flow matrix:\n{max_flow}")
            self.display_flow_and_capacity(max_flow, current_capacity_matrix)

            self.capacity_matrix_stack.pop()
            self.current_step -= 1

            # Prepare the flow matrix for the next iteration
            if self.capacity_matrix_stack:
                print(f"Next capacity matrix:\n{self.capacity_matrix_stack[-1]}")
                flow_matrix = 2 * max_flow

    def display_flow_and_capacity(self, flow_matrix, capacity_matrix):
        # Display the flow matrix and the capacity matrix
        for i in range(self.node_count):
            for j in range(self.node_count):
                if capacity_matrix[i][j] > 0:
                    print(f"({i+1},{j+1}): flow = {flow_matrix[i][j]}, capacity = {capacity_matrix[i][j]}")

