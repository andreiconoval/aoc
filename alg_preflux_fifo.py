from collections import deque
import numpy as np
import alg_generic_cu_preflux

class FIFOPreflowAlgorithm(alg_generic_cu_preflux.GenericPreflowAlgorithm):
    def __init__(self, node_count, source, sink):
        # Initialize with the number of nodes, source, and sink
        super().__init__(node_count, source, sink)
        self.active_nodes_queue = deque()

    def calculate_residual_network_with_fifo_preflow(self, flow_matrix, capacity_matrix, residual_network):
        # Initialize preflows from the source node
        for i in range(self.node_count):
            if residual_network[self.source][i] > 0:
                flow_matrix[self.source][i] = capacity_matrix[self.source][i]
                residual_network[i][self.source] = residual_network[self.source][i]
                residual_network[self.source][i] = 0

                if i != self.sink:
                    self.active_nodes_queue.append(i)

        # Set the source node's distance label to the total number of nodes
        self.exact_distance_labels[self.source] = self.node_count

        # Initialize the excess flows for all nodes
        self.initialize_node_excesses(flow_matrix)

        # Process active nodes using FIFO (First-In-First-Out) approach
        while self.active_nodes_queue:
            current_node = self.active_nodes_queue.popleft()

            for neighbor in range(self.node_count):
                if (residual_network[current_node][neighbor] > 0 and 
                    self.exact_distance_labels[current_node] == self.exact_distance_labels[neighbor] + 1):
                    
                    flow_amount = min(self.node_excesses[current_node], residual_network[current_node][neighbor])

                    # Update the excess flows and the residual network
                    self.node_excesses[current_node] -= flow_amount
                    self.node_excesses[neighbor] += flow_amount
                    residual_network[current_node][neighbor] -= flow_amount
                    residual_network[neighbor][current_node] += flow_amount

                    if neighbor not in self.active_nodes_queue and neighbor != self.source and neighbor != self.sink:
                        self.active_nodes_queue.append(neighbor)

                    break
            else:
                # If no admissible arc is found, relabel the current node
                self.update_distance_label_by_min_neighbor(residual_network, current_node)
                print(self.exact_distance_labels)
                self.active_nodes_queue.append(current_node)

        return residual_network

    def run_fifo_preflow_algorithm(self, capacity_matrix):
        # Initialize flow and residual networks
        flow_matrix = np.zeros((self.node_count, self.node_count), dtype=int)
        residual_network = self.initialize_residual_network(flow_matrix, capacity_matrix)
        self.display_network(residual_network)

        # Calculate initial distance labels
        self.calculate_exact_distances_BFS(capacity_matrix)

        # Calculate the residual network using the FIFO preflow algorithm
        residual_network = self.calculate_residual_network_with_fifo_preflow(flow_matrix, capacity_matrix, residual_network)
        self.display_network(residual_network)

        # Calculate and display the maximum flow
        max_flow = self.calculate_max_flow(flow_matrix, capacity_matrix, residual_network)
        self.display_flow_and_capacity(max_flow, capacity_matrix)

    def display_network(self, network):
        # Display the network matrix row by row
        for row in network:
            print(row)
