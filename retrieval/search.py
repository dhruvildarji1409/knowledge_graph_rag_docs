import pickle
import json
import numpy as np
from sentence_transformers import SentenceTransformer
from sklearn.metrics.pairwise import cosine_similarity
import networkx as nx

EMBEDDING_MODEL = "all-MiniLM-L6-v2"

def load_graph(path="data/graph.gpickle"):
    with open(path, "rb") as f:
        return pickle.load(f)

def load_embeddings(embedding_path="data/embedding_vectors.npy", index_path="data/embedding_index.json"):
    embeddings = np.load(embedding_path)
    with open(index_path, "r") as f:
        node_ids = json.load(f)
    return node_ids, embeddings

def embed_query(query, model):
    return model.encode([query.lower()], convert_to_numpy=True)[0]

def find_top_k(query_vector, node_ids, embeddings, k=10):
    scores = cosine_similarity([query_vector], embeddings)[0]
    top_k = scores.argsort()[-k:][::-1]
    return [(node_ids[i], scores[i]) for i in top_k]

def expand_context(G, base_node_id, depth=1):
    visited = set([base_node_id])
    frontier = set([base_node_id])

    for _ in range(depth):
        next_frontier = set()
        for node in frontier:
            next_frontier.update(G.successors(node))
            next_frontier.update(G.predecessors(node))
        frontier = next_frontier - visited
        visited.update(frontier)

    return list(visited)

def filter_by_keywords(G, candidate_nodes, query_keywords):
    filtered = []
    for node_id in candidate_nodes:
        node = G.nodes[node_id]
        full_text = f"{node['title']} {node['content']}".lower()
        if any(kw in full_text for kw in query_keywords):
            filtered.append(node_id)
    return filtered or candidate_nodes  # fallback to original if no match

def retrieve_answer(user_query, expand_depth=1):
    query_keywords = user_query.lower().split()
    G = load_graph()
    node_ids, embeddings = load_embeddings()
    model = SentenceTransformer(EMBEDDING_MODEL)

    q_vec = embed_query(user_query, model)
    top_matches = find_top_k(q_vec, node_ids, embeddings, k=10)

    print("\n🔍 Top Semantic Matches:")
    for nid, score in top_matches:
        print(f"• [{nid}] {G.nodes[nid]['title']} (score: {score:.4f})")

    # Merge all node IDs to a context pool
    expanded_node_ids = set()
    for node_id, _ in top_matches:
        expanded_node_ids.update(expand_context(G, node_id, expand_depth))

    # Optional keyword-based filtering
    final_node_ids = filter_by_keywords(G, list(expanded_node_ids), query_keywords)

    # Sort by original semantic score where possible
    final_node_ids = sorted(final_node_ids, key=lambda x: next((s for i, (nid, s) in enumerate(top_matches) if nid == x), 0), reverse=True)

    # Format context
    context_blocks = []
    for nid in final_node_ids:
        node = G.nodes[nid]
        context_blocks.append(f"{node['title']}:\n{node['content'].strip()}")

    return [{
        "query_match": top_matches[0][0] if top_matches else None,
        "score": top_matches[0][1] if top_matches else 0,
        "expanded_context": "\n\n".join(context_blocks)
    }]
