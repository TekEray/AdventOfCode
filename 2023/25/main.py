import networkx as nx
import os

def readInput():
    script_dir = os.path.dirname(__file__)
    rel_path = "inputs/input.txt"
    abs_file_path = os.path.join(script_dir, rel_path)
    graph = nx.Graph()
    with open(abs_file_path,'r') as f:
        input_lines = f.read().splitlines()
        for line in input_lines:
            node, *neighbors = line.replace(":", "").replace(",", "").split()[0:]
            graph.add_edges_from((node, neighbor) for neighbor in neighbors)
    return graph

def find_critical_edges(graph):
    # Calculate edge betweenness centrality
    edge_betweenness = nx.edge_betweenness_centrality(graph)

    # Sort edges by betweenness centrality in descending order
    sorted_edges = sorted(edge_betweenness.items(), key=lambda x: x[1], reverse=True)

    return sorted_edges

def main():
    graph = readInput()

    # Find edges with high betweenness centrality
    critical_edges = find_critical_edges(graph)

    # Select the first three critical edges
    selected_edges = [edge[0] for edge in critical_edges[:3]]

    # Temporarily remove the selected edges
    temp_graph = graph.copy()
    temp_graph.remove_edges_from(selected_edges)

    # Check if the graph is divided into two components
    components = list(nx.connected_components(temp_graph))
    if len(components) == 2:
        print('PART A:', len(components[0]) * len(components[1]))
        print(selected_edges)

if __name__ == "__main__":
    main()
