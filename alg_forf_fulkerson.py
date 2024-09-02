import random
import generic_dmf_algorithm

class FordFulkersonAlgorithm(generic_dmf_algorithm.GenericFlowAlgorithm):
    def __init__(self, node_count, source, sink):
        super().__init__(node_count, source, sink)

    def find_augmenting_path(self, residual_network):
        visited_nodes = [self.source]
        analyzed_nodes = []
        self.predecessors = [-1] * self.node_count

        while visited_nodes and self.predecessors[self.sink] < 0:
            current_node = random.choice(visited_nodes)
            print(f"Selected Node: {current_node}")

            for neighbor in range(self.node_count):
                if (residual_network[current_node][neighbor] > 0 and 
                    neighbor not in visited_nodes and 
                    neighbor not in analyzed_nodes):
                    visited_nodes.append(neighbor)
                    self.predecessors[neighbor] = current_node
                    print(f"Updated Predecessors: {self.predecessors}")
                    if neighbor == self.sink:
                        print("Path Found")
                        break
            else:
                visited_nodes.remove(current_node)
                analyzed_nodes.append(current_node)

            print(f"Visited Nodes: {visited_nodes}")
            print(f"Analyzed Nodes: {analyzed_nodes}")

        return self.predecessors[self.sink] > -1

    def calculate_max_flow_residual_network(self, residual_network):
        path_found = self.find_augmenting_path(residual_network)

        while path_found:
            print(f"Predecessors: {self.predecessors}")
            residual_network = self.update_residual_network(residual_network)

            for row in residual_network:
                print(' '.join(map(str, row)))

            path_found = self.find_augmenting_path(residual_network)

        print(f"Residual Capacities: {self.residual_capacities}")
        return residual_network

    def run_ford_fulkerson_algorithm(self, flows, capacities):
        print("Running Ford-Fulkerson Algorithm")
        residual_network = self.initialize_residual_network(flows, capacities)
        for row in residual_network:
            print(' '.join(map(str, row)))

        residual_network = self.calculate_max_flow_residual_network(residual_network)
        for row in residual_network:
            print(' '.join(map(str, row)))

        max_flow = self.calculate_max_flow(flows, capacities, residual_network)
        self.display_flow_and_capacity(max_flow, capacities)
