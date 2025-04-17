# 📘 Knowledge Graph RAG Documentation

This repository contains tools and guidelines for creating documentation that can be parsed into a **Knowledge Graph** and used in a **Graphical RAG (Retrieval-Augmented Generation)** system.

## 🎯 What is this repository for?

This project helps you:

1. Structure technical documentation in a specific format
2. Parse this documentation into knowledge graph nodes and edges
3. Create interactive visualizations of the resulting graph
4. Build a more intelligent search and retrieval system

## 🖼️ Knowledge Graph Example

![Knowledge Graph Visualization](data/graph_visual.png)

*The image above shows a knowledge graph built from a properly formatted document. See [ddu_guide.txt](data/raw_docs/ddu_guide.txt) for an example of the underlying documentation format.*

## 🔍 Interactive Graph Explorer

This repository includes an interactive graph visualization:

- **File:** `data/graph_ui.html`
- **Features:**
  - Zoom in/out to explore different parts of the graph
  - Click on nodes to see their content
  - Drag nodes to rearrange the visualization
  - Hover over nodes to see detailed information

### How to View the Interactive Graph

1. Clone this repository
2. Open `data/graph_ui.html` in any modern web browser
3. Explore the graph by clicking, dragging, and zooming

### How to Generate a New Graph Visualization

The interactive graph is generated using the `graph_visualizer.py` script:

```python
python -m graph_builder.graph_visualizer
```

This will create a new HTML visualization from the current graph data (`data/graph.gpickle`).

## 📚 How to Use This Repository

1. **Read the documentation format guidelines below**
2. **Create your technical documentation** following the format
3. **Save your files** as `.txt` in the `data/raw_docs/` directory
4. **Run the graph builder** to parse your documents
5. **Explore the results** using the interactive visualization

## 📝 Documentation Format Guidelines

### Document Structure

Use a numeric hierarchical structure like:

```
1. Main Topic
1.1 Subtopic
1.1.1 Step Description
1.1.1.1 Command or Sub-step
```

Each heading:
- Represents a **graph node**
- Its number implies **depth and relationship**
- Its indented content becomes the **node content**

### Authoring Rules

| Level     | Format         | Example                                  |
|-----------|----------------|------------------------------------------|
| Heading 1 | `1.`           | `1. Generating DDU Image`                |
| Heading 2 | `1.1`          | `1.1 QNX`                                |
| Step      | `1.1.1`        | `1.1.1 Launch the container`             |
| Sub-step  | `1.1.1.1`      | `1.1.1.1 PDK = 6080`                      |
| Commands  | Indented (4 spaces) | `    dazel run ...`                  |

### Authoring Best Practices

- Keep **titles short** and specific
- Always **indent command/code** blocks with 4 spaces (not tabs)
- Use **plain text** — avoid Markdown symbols like `#`, `-`, `*`
- Add **inline comments** for clarity (e.g., `# PDK = 6080`)
- Do **not skip levels** (you can't have `1.2.3` without `1.2.1`)

### Example (Well-Formatted Document)

```
1.2 QNX

1.2.1 Container Spinoff
    export NDAS_PARTNER=daimler

1.2.1.3 PDK = 652
    dazel run --config=drive-qnx_6.5.2 //partners/daimler/av/packaging/containers/avos:avos-qnx-daimler

1.2.2 Launch the container
    docker run --rm -dt --privileged --net host ...
```

This builds the following graph structure:
```
1 ──> 1.2 ──> 1.2.1 ──> 1.2.1.3
              │
              └──> 1.2.2
```

Each `─>` is a **parent → child** relationship.

### Common Mistakes to Avoid

| ❌ Incorrect                     | ✅ Correct                         |
|----------------------------------|-----------------------------------|
| Use of `- Step`                  | Use `1.1.1 Step`                  |
| Tabs for indent                 | 4 spaces only                    |
| Markdown like `## QNX`          | Use `1.1 QNX`                    |
| Long paragraph as a heading     | Break into smaller substeps     |
| Unstructured commands           | Always indent under heading     |

## 💡 Why Graphical RAG?

### Traditional RAG vs Graphical RAG

| **Feature**                | **Traditional RAG**                         | **Graphical RAG**                                     |
|----------------------------|---------------------------------------------|--------------------------------------------------------|
| **Data Structure**         | Unstructured chunks of text                | Structured, hierarchical nodes                        |
| **Search Type**            | Vector similarity only                     | Semantic + Graph traversal                            |
| **Context Expansion**      | Top-k chunks only                          | Nearby steps, parent sections, children nodes         |
| **Order of Operations**    | Lost in chunk boundaries                   | Preserved via graph path                              |
| **Scalability with Docs**  | Harder to deduplicate or group logic       | Graph allows clustering, deduplication                |
| **Debuggability**          | Opaque - hard to trace sources             | Transparent - every node is traceable                 |
| **Update Process**         | Requires re-embedding whole corpus         | Only new nodes/edges added                           |

### Key Benefits

1. **Context-Aware Retrieval**: Related steps, not just similar sentences
2. **Preserves Order and Dependencies**: Maintains instruction flow
3. **Fine-Grained Search**: Each step/command lives in its own graph node
4. **Extensibility**: Just drop new structured files into the raw doc folder
5. **Clear Auditability**: Every response is traceable to its source

## 📂 File Organization

- `data/raw_docs/` - Place for your raw documentation files
- `graph_builder/` - Code to parse documents and build the graph
- `data/` - Output directory for graph data and visualizations

## 💬 Questions or Need Help?

See a complete example in [ddu_guide.txt](data/raw_docs/ddu_guide.txt) or contact the Graphical RAG maintainer.

---

Write clean. Think structured. Build the graph 🚀