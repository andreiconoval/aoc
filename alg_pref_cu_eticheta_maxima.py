import numpy as np
from heapq import heappush, heappop
import alg_generic_cu_preflux

class DistanceComparator:
    def __init__(self, distances):
        # Initialize with the distance labels for each node
        self.distances = distances

    def __call__(self, node):
        # Return the negated distance for max-heap behavior
        return -self.distances[node]

class MaxLabelPreflowAlgorithm(alg_generic_cu_preflux.GenericPreflowAlgorithm):
    def __init__(self, node_count, source, sink):
        # Initialize with the number of nodes, source, and sink
        super().__init__(node_count, source, sink)
        self.active_nodes_queue = []

    def calculate_residual_network_with_max_label_preflow(self, flow_matrix, capacity_matrix, residual_network):
        # Initialize preflows from the source node
        for i in range(self.node_count):
            if residual_network[self.source][i] > 0:
                flow_matrix[self.source][i] = capacity_matrix[self.source][i]
                residual_network[i][self.source] = residual_network[self.source][i]
                residual_network[self.source][i] = 0

        # Set the source node's distance label to the total number of nodes
        self.exact_distance_labels[self.source] = self.node_count

        # Initialize the excess flows for all nodes
        self.initialize_node_excesses(flow_matrix)

        # Create a max-heap (priority queue) for active nodes based on distance labels
        distance_comparator = DistanceComparator(self.exact_distance_labels)
        self.active_nodes_queue = []

        for i in range(self.node_count):
            if residual_network[i][self.source] > 0 and i != self.sink:
                heappush(self.active_nodes_queue, (distance_comparator(i), i))

        # Process active nodes until there are none left
        while self.active_nodes_queue:
            _, current_node = heappop(self.active_nodes_queue)

            for neighbor in range(self.node_count):
                if (residual_network[current_node][neighbor] > 0 and 
                    self.exact_distance_labels[current_node] == self.exact_distance_labels[neighbor] + 1):
                    
                    flow_amount = min(self.node_excesses[current_node], residual_network[current_node][neighbor])

                    # Update the excess flows and the residual network
                    self.node_excesses[current_node] -= flow_amount
                    self.node_excesses[neighbor] += flow_amount
                    residual_network[current_node][neighbor] -= flow_amount
                    residual_network[neighbor][current_node] += flow_amount

                    if (neighbor not in [self.source, self.sink] and 
                        not any(neighbor == item[1] for item in self.active_nodes_queue)):
                        heappush(self.active_nodes_queue, (distance_comparator(neighbor), neighbor))

                    break
            else:
                # If no admissible arc is found, relabel the current node
                self.update_distance_label_by_min_neighbor(residual_network, current_node)
                print(self.exact_distance_labels)

                if (current_node not in [self.source, self.sink] and 
                    not any(current_node == item[1] for item in self.active_nodes_queue)):
                    heappush(self.active_nodes_queue, (distance_comparator(current_node), current_node))

        return residual_network

    def run_max_label_preflow_algorithm(self, capacity_matrix):
        # Initialize flow and residual networks
        flow_matrix = np.zeros((self.node_count, self.node_count), dtype=int)
        residual_network = self.initialize_residual_network(flow_matrix, capacity_matrix)
        self.display_network(residual_network)

        # Calculate initial distance labels
        self.calculate_exact_distances_BFS(capacity_matrix)

        # Calculate the residual network using the max-label preflow algorithm
        residual_network = self.calculate_residual_network_with_max_label_preflow(flow_matrix, capacity_matrix, residual_network)
        self.display_network(residual_network)

        # Calculate and display the maximum flow
        max_flow = self.calculate_max_flow(flow_matrix, capacity_matrix, residual_network)
        self.display_flow_and_capacity(max_flow, capacity_matrix)

    def display_network(self, network):
        # Display the network matrix row by row
        for row in network:
            print(row)
