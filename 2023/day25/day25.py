# https://adventofcode.com/2023/day/25
import networkx as nx

with open("input.txt") as f:
    lines = list(map(str.strip, f.readlines()))

def solve_part_1():
    # Create graph
    graph = nx.Graph()
    for line in lines:
        node, connections = line.split(": ")
        for connection in connections.split():
            graph.add_edge(node, connection)
    
    # Find the smallest number of edges that can be cut to disconnect the graph
    min_cut = nx.minimum_edge_cut(graph)

    # Remove the edges above (we could do a check to make sure there's two but she'll be right)
    graph.remove_edges_from(min_cut)

    # Find all disconnected graphs
    connected_components = nx.connected_components(graph)

    # Get the product of the number of nodes in each
    # Once again we assume there's only two but she'll be right
    ans = 1
    for subgraph in connected_components:
        ans *= len(subgraph)

    return ans

print(f"Part 1 answer: {solve_part_1()}")

