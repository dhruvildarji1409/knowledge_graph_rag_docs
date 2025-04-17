def build_prompt(user_query: str, expanded_context: str) -> str:
    return f"""
You are a helpful assistant trained to guide engineers in flashing and generating DDU images across Linux, QNX, and QNX-Safety systems.

Please answer the following question based **only** on the provided context. If the answer is not found in the context, say:
"I'm not sure based on the current knowledge graph."

---

User Question:
{user_query}

---

Relevant Context (from graph-based retrieval):
{expanded_context}

---

Answer:
"""
