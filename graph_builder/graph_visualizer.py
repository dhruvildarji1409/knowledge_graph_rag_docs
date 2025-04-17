from pyvis.network import Network
import pickle
import os

def visualize_interactive(graph_path="data/graph.gpickle", out_file="data/graph_ui.html"):
    with open(graph_path, "rb") as f:
        G = pickle.load(f)

    net = Network(height="750px", width="100%", directed=True)
    net.barnes_hut()

    for node_id, data in G.nodes(data=True):
        label = f"{node_id}: {data['title']}"
        net.add_node(node_id, label=label, title=data.get("content", ""), color="#a7c7e7")

    for source, target in G.edges():
        net.add_edge(source, target)

    os.makedirs(os.path.dirname(out_file), exist_ok=True)
    net.show(out_file)
    print(f"Interactive graph saved at {out_file}")


if __name__ == "__main__":
    visualize_interactive()
