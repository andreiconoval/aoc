import numpy as np
from copy import deepcopy
import generic_dmf_algorithm 

class BitScalingAlgorithm(generic_dmf_algorithm.GenericDMFAlgorithm):
    """Alg Gabow de scalare pe biti O(sqr(2)*logC)"""
    def __init__(self, num_nodes, source, sink, capacity_matrix):
        super().__init__(num_nodes, source, sink)
        self.max_capacity_list = []
        self.capacity_matrix_stack = []
        self.current_index = 0
        self.capacity_matrix_stack.append(capacity_matrix)

    def calculate_max_capacity(self, capacity_matrix):
        max_capacity = 0
        for i in range(self.num_nodes):
            max_from_current_row = np.max(capacity_matrix[i])
            if max_capacity < max_from_current_row:
                max_capacity = max_from_current_row
        self.max_capacity_list.append(max_capacity)

    def initialize_capacity_matrix(self, capacity_matrix):
        print(f"Max capacity: {self.max_capacity_list[-1]} for step k={self.current_index}")
        old_capacity_matrix = deepcopy(capacity_matrix)
        while self.max_capacity_list[-1] > 1:
            new_capacity_matrix = np.zeros((self.num_nodes, self.num_nodes), dtype=int)
            for i in range(self.num_nodes):
                for j in range(self.num_nodes):
                    if old_capacity_matrix[i][j] > 0:
                        new_capacity_matrix[i][j] = old_capacity_matrix[i][j] // 2
            self.current_index += 1
            print(f"For k={self.current_index} the new capacity matrix is {new_capacity_matrix}")
            self.capacity_matrix_stack.append(new_capacity_matrix)

            self.calculate_max_capacity(new_capacity_matrix)
            print(f"Max capacity: {self.max_capacity_list[-1]} for step k={self.current_index}")
            old_capacity_matrix = deepcopy(new_capacity_matrix)

    def clone_array(self, array):
        return deepcopy(array)

    def execute_bit_scaling_algorithm(self, capacity_matrix):
        self.calculate_max_capacity(capacity_matrix)
        self.initialize_capacity_matrix(capacity_matrix)

        f_k_plus_1 = np.zeros((self.num_nodes, self.num_nodes), dtype=int)
        print(f_k_plus_1)

        while self.current_index >= 0:
            current_capacity_matrix = self.capacity_matrix_stack[-1]
            new_residual_network = self.clone_array(current_capacity_matrix)

            new_residual_network = self.calculate_residual_network_for_max_flow(new_residual_network)
            print(f"Capacity matrix={self.capacity_matrix_stack[-1]}")
            print(f"Residual network={new_residual_network}")

            # Calculate max flow and display
            max_flow_matrix = self.calculate_max_flow(f_k_plus_1, current_capacity_matrix, new_residual_network)
            print(f"Flow matrix={max_flow_matrix}")
            self.display_max_flow_and_capacity(max_flow_matrix, current_capacity_matrix)

            self.capacity_matrix_stack.pop()

            self.current_index -= 1
            if self.capacity_matrix_stack:
                print(f"Capacity matrix={self.capacity_matrix_stack[-1]}")
                for i in range(self.num_nodes):
                    for j in range(self.num_nodes):
                        f_k_plus_1[i][j] = 2 * max_flow_matrix[i][j]
