import numpy as np
import alg_ahuja_orlin_shortest_path

class StratifiedNetworkAlgorithm(alg_ahuja_orlin_shortest_path.ShortestPathAlgorithm):
    def __init__(self, node_count, source, sink):
        # Initialize with the number of nodes, source, and sink
        super().__init__(node_count, source, sink)
        self.visited_flags = [0] * node_count

    def reset_visited_flags(self):
        # Reset the visited flags for all nodes
        self.visited_flags = [0] * self.node_count

    def calculate_stratified_networks(self, residual_network, capacity_matrix):
        current_node = self.source
        while self.exact_distance_labels[self.source] < self.node_count:
            if self.visited_flags[self.source] == 0:
                admissible_arc_found = False
                for neighbor in range(self.node_count):
                    if (residual_network[current_node][neighbor] > 0 and
                        self.exact_distance_labels[current_node] == self.exact_distance_labels[neighbor] + 1 and
                        self.visited_flags[neighbor] == 0):

                        admissible_arc_found = True
                        self.predecessors[neighbor] = current_node
                        current_node = neighbor

                        if current_node == self.sink:
                            residual_network = self.update_residual_network(residual_network)
                            self.display_network(residual_network)
                            current_node = self.source
                            self.predecessors = [-1] * self.node_count
                        break

                if not admissible_arc_found:
                    self.visited_flags[current_node] = 1
                    if current_node != self.source:
                        current_node = self.predecessors[current_node]
            else:
                self.calculate_exact_distances_BFS(residual_network)
                print(self.exact_distance_labels)
                self.reset_visited_flags()

        return residual_network

    def run_stratified_network_algorithm(self, capacity_matrix):
        # Initialize flow and residual network
        flow_matrix = np.zeros((self.node_count, self.node_count), dtype=int)
        residual_network = self.initialize_residual_network(flow_matrix, capacity_matrix)
        self.display_network(residual_network)

        # Initialize distance labels and visited flags
        self.calculate_exact_distances_BFS(capacity_matrix)
        self.reset_visited_flags()

        # Apply the stratified network algorithm
        residual_network = self.calculate_stratified_networks(residual_network, capacity_matrix)

        # Display the final residual network
        self.display_network(residual_network)

        # Calculate and display the maximum flow
        max_flow = self.calculate_max_flow(flow_matrix, capacity_matrix, residual_network)
        self.display_flow_and_capacity(max_flow, capacity_matrix)

    def display_network(self, network):
        # Display the network matrix row by row
        for row in network:
            print(row)
