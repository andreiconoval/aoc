import random
import generic_dmf_algorithm 

class FordFulkersonAlgorithm(generic_dmf_algorithm.GenericDMFAlgorithm):
    def __init__(self, num_nodes, source, sink):
        super().__init__(num_nodes, source, sink)

    def find_augmenting_path(self, residual_network):
        visited_nodes = [self.source_node]
        analyzed_nodes = []
        self.predecessor_nodes = [-1] * self.num_nodes

        while visited_nodes and self.predecessor_nodes[self.sink_node] < 0:
            random_index = random.randint(0, len(visited_nodes) - 1)
            current_node = visited_nodes[random_index]
            print(f"Current node: {current_node}")

            i = 0
            while i < self.num_nodes:
                print(f"i: {i}: ")
                if (residual_network[current_node][i] > 0 and 
                    i not in visited_nodes and 
                    i not in analyzed_nodes):
                    visited_nodes.append(i)
                    self.predecessor_nodes[i] = current_node
                    print(f"Predecessor nodes: {self.predecessor_nodes}")
                    if i == self.sink_node:
                        print("Path found")
                        break
                i += 1

            if i == self.num_nodes:
                visited_nodes.remove(current_node)
                analyzed_nodes.append(current_node)

            print(f"Visited nodes: {visited_nodes}")
            print(f"Analyzed nodes: {analyzed_nodes}")

        return self.predecessor_nodes[self.sink_node] > -1

    def calculate_residual_network_for_max_flow(self, residual_network):
        path_found = self.find_augmenting_path(residual_network)

        while path_found:
            print(self.predecessor_nodes)
            residual_network = self.update_residual_network(residual_network)

            for i in range(self.num_nodes):
                print(' '.join(map(str, residual_network[i])))

            path_found = self.find_augmenting_path(residual_network)

        print(f"Residual capacities: {self.residual_capacity_list}")
        return residual_network

    def execute_ford_fulkerson_algorithm(self, flow_matrix, capacity_matrix):
        print("EXECUTING FORD-FULKERSON ALGORITHM")
        residual_network = self.calculate_initial_residual_network(self.num_nodes, flow_matrix, capacity_matrix)
        for row in residual_network:
            print(' '.join(map(str, row)))

        residual_network = self.calculate_residual_network_for_max_flow(residual_network)
        for row in residual_network:
            print(' '.join(map(str, row)))

        max_flow_matrix = self.calculate_max_flow(flow_matrix, capacity_matrix, residual_network)
        self.display_max_flow_and_capacity(max_flow_matrix, capacity_matrix)
