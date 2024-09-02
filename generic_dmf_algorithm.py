import random

class GenericDMFAlgorithm:
    
    def __init__(self, num_nodes, source, sink):
        self.source_node = source - 1
        self.sink_node = sink - 1
        self.num_nodes = num_nodes
        self.nodes = list(range(num_nodes))
        self.residual_capacity_list = []
        self.predecessor_nodes = [-1] * self.num_nodes

    def calculate_initial_residual_network(self, num_nodes, flow_matrix, capacity_matrix):
        residual_network = [[0] * num_nodes for _ in range(num_nodes)]
        for i in range(num_nodes):
            for j in range(num_nodes):
                residual_network[i][j] = capacity_matrix[i][j] - flow_matrix[i][j] + flow_matrix[j][i]
        return residual_network

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

    def calculate_augmenting_path_capacity(self, residual_network):
        print("Calculating augmenting path capacity")
        self.residual_capacity_list = []
        current_node = self.sink_node
        min_capacity = float('inf')
        
        while current_node != self.source_node:
            predecessor = self.predecessor_nodes[current_node]
            print(f"residual_network[{predecessor}][{current_node}] = {residual_network[predecessor][current_node]}")
            if residual_network[predecessor][current_node] < min_capacity:
                min_capacity = residual_network[predecessor][current_node]
            current_node = predecessor
            
        self.residual_capacity_list.append(min_capacity)
        return min_capacity

    def update_residual_network(self, residual_network):
        print("Updating residual network")
        current_node = self.sink_node
        augmenting_path_capacity = self.calculate_augmenting_path_capacity(residual_network)
        print(f"Augmenting path capacity = {augmenting_path_capacity}")
        
        while current_node != self.source_node:
            predecessor = self.predecessor_nodes[current_node]
            residual_network[predecessor][current_node] -= augmenting_path_capacity
            residual_network[current_node][predecessor] += augmenting_path_capacity
            current_node = predecessor
            
        return residual_network

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

    def calculate_max_flow(self, flow_matrix, capacity_matrix, residual_network):
        max_flow_matrix = [row[:] for row in flow_matrix]
        
        for i in range(self.num_nodes):
            for j in range(self.num_nodes):
                if capacity_matrix[i][j] >= residual_network[i][j]:
                    max_flow_matrix[i][j] = capacity_matrix[i][j] - residual_network[i][j]
                    max_flow_matrix[j][i] = 0
                else:
                    max_flow_matrix[i][j] = 0
                    max_flow_matrix[j][i] = residual_network[i][j] - capacity_matrix[i][j]
                    
        return max_flow_matrix

    def display_max_flow_and_capacity(self, flow_matrix, capacity_matrix):
        for i in range(self.num_nodes):
            for j in range(self.num_nodes):
                if capacity_matrix[i][j] != 0:
                    print(f"({i + 1},{j + 1}): {flow_matrix[i][j]}, {capacity_matrix[i][j]}", end="")
                    if capacity_matrix[j][i] != 0:
                        initial_flow_ij = flow_matrix[i][j]
                        initial_flow_ji = flow_matrix[j][i]
                        while (flow_matrix[i][j] + 1 <= capacity_matrix[i][j] and 
                               flow_matrix[j][i] + 1 <= capacity_matrix[j][i]):
                            flow_matrix[i][j] += 1
                            flow_matrix[j][i] += 1
                            print(f"; {flow_matrix[i][j]}, {capacity_matrix[i][j]}", end="")
                        flow_matrix[i][j] = initial_flow_ij
                        flow_matrix[j][i] = initial_flow_ji
                    print()

    def execute_generic_dmf_algorithm(self, flow_matrix, capacity_matrix):
        print("EXECUTING GENERIC DMF ALGORITHM")
        residual_network = self.calculate_initial_residual_network(self.num_nodes, flow_matrix, capacity_matrix)
        for row in residual_network:
            print(' '.join(map(str, row)))

        residual_network = self.calculate_residual_network_for_max_flow(residual_network)
        for row in residual_network:
            print(' '.join(map(str, row)))

        max_flow_matrix = self.calculate_max_flow(flow_matrix, capacity_matrix, residual_network)
        self.display_max_flow_and_capacity(max_flow_matrix, capacity_matrix)