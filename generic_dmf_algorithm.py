import random

class GenericFlowAlgorithm:
    
    def __init__(self, node_count, source, sink):
        self.source = source - 1 # source node
        self.sink = sink - 1 # desitation node
        self.node_count = node_count
        self.nodes = list(range(node_count))
        self.residual_capacities = []
        self.predecessors = [-1] * self.node_count

    
    def initialize_residual_network(self, flows, capacities):
        residual_network = [[0] * self.node_count for _ in range(self.node_count)]
        for i in range(self.node_count):
            for j in range(self.node_count):
                residual_network[i][j] = capacities[i][j] - flows[i][j] + flows[j][i]
        return residual_network

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

    def compute_path_residual_capacity(self, residual_network):
        print("Computing Path Residual Capacity")
        self.residual_capacities = []
        path_capacity = float('inf')
        node = self.sink
        
        while node != self.source:
            previous_node = self.predecessors[node]
            print(f"Residual Capacity from {previous_node} to {node}: {residual_network[previous_node][node]}")
            path_capacity = min(path_capacity, residual_network[previous_node][node])
            node = previous_node
            
        self.residual_capacities.append(path_capacity)
        return path_capacity

    def update_residual_network(self, residual_network):
        print("Updating Residual Network")
        path_capacity = self.compute_path_residual_capacity(residual_network)
        print(f"Path Capacity: {path_capacity}")
        node = self.sink
        
        while node != self.source:
            previous_node = self.predecessors[node]
            residual_network[previous_node][node] -= path_capacity
            residual_network[node][previous_node] += path_capacity
            node = previous_node
            
        return residual_network

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

    def calculate_max_flow(self, flows, capacities, residual_network):
        max_flow = [row[:] for row in flows]
        
        for i in range(self.node_count):
            for j in range(self.node_count):
                if capacities[i][j] >= residual_network[i][j]:
                    max_flow[i][j] = capacities[i][j] - residual_network[i][j]
                    max_flow[j][i] = 0
                else:
                    max_flow[i][j] = 0
                    max_flow[j][i] = residual_network[i][j] - capacities[i][j]
                    
        return max_flow

    def display_flow_and_capacity(self, flows, capacities):
        for i in range(self.node_count):
            for j in range(self.node_count):
                if capacities[i][j] != 0:
                    print(f"({i + 1},{j + 1}): {flows[i][j]}, {capacities[i][j]}", end="")
                    if capacities[j][i] != 0:
                        initial_flow_ij = flows[i][j]
                        initial_flow_ji = flows[j][i]
                        while (flows[i][j] + 1 <= capacities[i][j] and 
                               flows[j][i] + 1 <= capacities[j][i]):
                            flows[i][j] += 1
                            flows[j][i] += 1
                            print(f"; {flows[i][j]}, {capacities[i][j]}", end="")
                        flows[i][j] = initial_flow_ij
                        flows[j][i] = initial_flow_ji
                    print()

    def run_algorithm(self, flows, capacities):
        print("Running Generic Max Flow Algorithm")
        residual_network = self.initialize_residual_network(flows, capacities)
        for row in residual_network:
            print(' '.join(map(str, row)))

        residual_network = self.calculate_max_flow_residual_network(residual_network)
        for row in residual_network:
            print(' '.join(map(str, row)))

        max_flow = self.calculate_max_flow(flows, capacities, residual_network)
        self.display_flow_and_capacity(max_flow, capacities)
