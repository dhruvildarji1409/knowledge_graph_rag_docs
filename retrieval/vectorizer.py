import pickle
import os
from sentence_transformers import SentenceTransformer
import numpy as np
import json

EMBEDDING_MODEL = "all-MiniLM-L6-v2"  # Lightweight and fast

def load_graph(graph_path="data/graph.gpickle"):
    with open(graph_path, "rb") as f:
        G = pickle.load(f)
    return G


def generate_embeddings(G):
    model = SentenceTransformer(EMBEDDING_MODEL)
    node_texts = []
    node_ids = []

    for node_id, data in G.nodes(data=True):
        combined_text = f"{data['title']}\n{data['content']}"
        node_texts.append(combined_text)
        node_ids.append(node_id)

    embeddings = model.encode(node_texts, convert_to_numpy=True)
    return node_ids, embeddings


def save_embeddings(node_ids, embeddings, out_dir="data"):
    os.makedirs(out_dir, exist_ok=True)

    np.save(os.path.join(out_dir, "embedding_vectors.npy"), embeddings)
    with open(os.path.join(out_dir, "embedding_index.json"), "w") as f:
        json.dump(node_ids, f)

    print(f"Saved {len(node_ids)} embeddings.")


if __name__ == "__main__":
    G = load_graph()
    node_ids, embeddings = generate_embeddings(G)
    save_embeddings(node_ids, embeddings)
