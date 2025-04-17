import os
import json
import re

def parse_file(filepath):
    with open(filepath, "r") as f:
        lines = f.readlines()

    nodes = []
    stack = []  # Keeps track of parent node levels
    current_node = None

    for line in lines:
        line = line.rstrip()

        # Match a new heading like 1., 1.1, 1.1.1, etc.
        match = re.match(r'^(\d+(\.\d+)*)(?:\s+)(.+)', line)
        if match:
            node_id = match.group(1)
            title = match.group(3).strip()
            level = node_id.count(".")

            parent_id = None
            while stack and stack[-1]["level"] >= level:
                stack.pop()
            if stack:
                parent_id = stack[-1]["id"]

            current_node = {
                "id": node_id,
                "title": title,
                "content": "",
                "parent_id": parent_id,
                "level": level
            }
            nodes.append(current_node)
            stack.append(current_node)
        elif current_node:
            # Append content to the last matched node
            current_node["content"] += line + "\n"

    return nodes


def save_graph_data(nodes, output_dir="data"):
    os.makedirs(output_dir, exist_ok=True)

    # Save nodes
    with open(os.path.join(output_dir, "parsed_nodes.json"), "w") as f:
        json.dump(nodes, f, indent=4)

    # Save edges
    edges = [{"from": node["parent_id"], "to": node["id"]}
             for node in nodes if node["parent_id"]]
    with open(os.path.join(output_dir, "edges.json"), "w") as f:
        json.dump(edges, f, indent=4)


if __name__ == "__main__":
    filepath = "data/raw_docs/ddu_guide.txt"
    nodes = parse_file(filepath)
    save_graph_data(nodes)
    print(f"Parsed {len(nodes)} nodes. Saved to `parsed_nodes.json` and `edges.json`.")
