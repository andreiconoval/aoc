import numpy as np
from collections import deque
import generic_dmf_algorithm

class ShortestPathAlgorithm(generic_dmf_algorithm.GenericFlowAlgorithm):
    def __init__(self, node_count, source, sink):
        # Initialize the algorithm with the number of nodes, source, and sink
        super().__init__(node_count, source, sink)
        self.exact_distance_labels = [-1] * node_count
        self.exact_distance_labels[sink] = 0  # Distance from sink to itself is 0

    def calculate_exact_distances_BFS(self, capacity_matrix):
        # Use BFS to calculate the exact distance labels for each node from the sink
        visited = [False] * self.node_count
        queue = deque([self.sink])
        visited[self.sink] = True

        self.exact_distance_labels[self.source] = self.node_count + 1

        while not visited[self.source] and queue:
            current_node = queue.popleft()

            for neighbor in range(self.node_count - 2, -1, -1):
                if not visited[neighbor] and capacity_matrix[neighbor][current_node] > 0:
                    visited[neighbor] = True
                    queue.append(neighbor)
                    self.exact_distance_labels[neighbor] = self.exact_distance_labels[current_node] + 1

        print(self.exact_distance_labels)

    def update_distance_label_by_min_neighbor(self, residual_network, node):
        # Update the distance label for a node based on its minimum neighbor's distance label
        min_distance = self.node_count + 1
        for neighbor in range(self.node_count):
            if residual_network[node][neighbor] > 0 and self.exact_distance_labels[neighbor] + 1 < min_distance:
                min_distance = self.exact_distance_labels[neighbor] + 1

        self.exact_distance_labels[node] = min_distance

    def find_shortest_path_in_residual_network(self, residual_network, capacity_matrix):
        # Find the shortest path in the residual network and update the residual capacities
        current_node = self.source
        while self.exact_distance_labels[self.source] < self.node_count:
            for neighbor in range(self.node_count):
                if (residual_network[current_node][neighbor] > 0 and 
                    self.exact_distance_labels[current_node] == self.exact_distance_labels[neighbor] + 1):
                    self.predecessors[neighbor] = current_node
                    current_node = neighbor

                    if current_node == self.sink:
                        residual_network = self.update_residual_network(residual_network)
                        self.display_network(residual_network)
                        current_node = self.source
                        self.predecessors = [-1] * self.node_count
                    break
            else:
                self.update_distance_label_by_min_neighbor(residual_network, current_node)
                print(self.exact_distance_labels)

                if current_node != self.source:
                    current_node = self.predecessors[current_node]

    def run_ahuja_orlin_shortest_path_algorithm(self, capacity_matrix):
        # Execute the Ahuja-Orlin shortest path algorithm for maximum flow
        flow_matrix = np.zeros((self.node_count, self.node_count), dtype=int)
        residual_network = self.initialize_residual_network(flow_matrix, capacity_matrix)
        self.display_network(residual_network)

        self.calculate_exact_distances_BFS(capacity_matrix)
        self.find_shortest_path_in_residual_network(residual_network, capacity_matrix)

        self.display_network(residual_network)

        max_flow = self.calculate_max_flow(flow_matrix, capacity_matrix, residual_network)
        self.display_flow_and_capacity(max_flow, capacity_matrix)

    def display_network(self, network):
        # Display the network matrix row by row
        for row in network:
            print(row)
