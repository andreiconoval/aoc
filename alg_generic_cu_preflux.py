import numpy as np
import random
import alg_ahuja_orlin_shortest_path

class GenericPreflowAlgorithm(alg_ahuja_orlin_shortest_path.ShortestPathAlgorithm):
    def __init__(self, node_count, source, sink):
        # Initialize the algorithm with the number of nodes, source, and sink
        super().__init__(node_count, source, sink)
        self.node_excesses = []

    def calculate_node_excess(self, flow_matrix, node):
        # Calculate the excess flow for a given node
        excess = 0
        for i in range(self.node_count):
            excess += flow_matrix[i][node] - flow_matrix[node][i]  # Total inflow - total outflow
        return excess

    def initialize_node_excesses(self, flow_matrix):
        # Initialize the excess flow for all nodes
        self.node_excesses = [self.calculate_node_excess(flow_matrix, i) for i in range(self.node_count)]
        print(self.node_excesses)

    def get_active_nodes(self):
        # Return a list of active nodes (with excess flow) that are not the source or sink
        return [i for i in range(self.node_count) if i != self.source and i != self.sink and self.node_excesses[i] > 0]

    def calculate_residual_network_with_preflows(self, flow_matrix, capacity_matrix, residual_network):
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
        active_nodes = self.get_active_nodes()

        # Process active nodes until there are none left
        while active_nodes:
            random_index = random.randint(0, len(active_nodes) - 1)
            current_node = active_nodes[random_index]
            print(f"Selected Active Node: {current_node}")

            for neighbor in range(self.node_count):
                if (residual_network[current_node][neighbor] > 0 and
                    self.exact_distance_labels[current_node] == self.exact_distance_labels[neighbor] + 1):
                    
                    flow_amount = min(self.node_excesses[current_node], residual_network[current_node][neighbor])
                    
                    # Update the excess flows and the residual network
                    self.node_excesses[current_node] -= flow_amount
                    self.node_excesses[neighbor] += flow_amount
                    residual_network[current_node][neighbor] -= flow_amount
                    residual_network[neighbor][current_node] += flow_amount

                    break
            else:
                # If no admissible arc is found, relabel the current node
                self.update_distance_label_by_min_neighbor(residual_network, current_node)
                print(self.exact_distance_labels)

            # Update the list of active nodes
            active_nodes = self.get_active_nodes()

        return residual_network

    def run_generic_preflow_algorithm(self, capacity_matrix):
        # Initialize flow and residual networks
        flow_matrix = np.zeros((self.node_count, self.node_count), dtype=int)
        residual_network = self.initialize_residual_network(flow_matrix, capacity_matrix)
        self.display_network(residual_network)

        # Calculate initial distance labels
        self.calculate_exact_distances_BFS(capacity_matrix)

        # Calculate the residual network using the generic preflow algorithm
        residual_network = self.calculate_residual_network_with_preflows(flow_matrix, capacity_matrix, residual_network)
        self.display_network(residual_network)

        # Calculate and display the maximum flow
        max_flow = self.calculate_max_flow(flow_matrix, capacity_matrix, residual_network)
        self.display_flow_and_capacity(max_flow, capacity_matrix)

    def display_network(self, network):
        # Display the network matrix row by row
        for row in network:
            print(row)
