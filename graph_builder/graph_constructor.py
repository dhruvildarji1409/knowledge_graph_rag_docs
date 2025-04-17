import json
import os
import networkx as nx
import matplotlib.pyplot as plt


def load_data(node_path="data/parsed_nodes.json", edge_path="data/edges.json"):
    with open(node_path, "r") as f:
        nodes = json.load(f)

    with open(edge_path, "r") as f:
        edges = json.load(f)

    return nodes, edges


def build_graph(nodes, edges):
    G = nx.DiGraph()  # Directed graph

    # Add nodes with attributes
    for node in nodes:
        G.add_node(node["id"], **node)

    # Add edges
    for edge in edges:
        G.add_edge(edge["from"], edge["to"])

    return G


def visualize_graph(G, output_file="data/graph_visual.png"):
    plt.figure(figsize=(20, 12))
    pos = nx.spring_layout(G, k=0.5)
    nx.draw(G, pos, with_labels=True, node_size=5000, node_color="skyblue", font_size=10, font_weight="bold", arrows=True)
    plt.title("Knowledge Graph")
    os.makedirs(os.path.dirname(output_file), exist_ok=True)
    plt.savefig(output_file)
    print(f"Graph visualization saved to {output_file}")


def save_graph(G, path="data/graph.gpickle"):
    import pickle
    os.makedirs(os.path.dirname(path), exist_ok=True)
    with open(path, "wb") as f:
        pickle.dump(G, f)
    print(f"Graph saved as {path}")



if __name__ == "__main__":
    nodes, edges = load_data()
    G = build_graph(nodes, edges)
    visualize_graph(G)
    save_graph(G)
