from retrieval.search import retrieve_answer
from chatbot.prompts import build_prompt
from openai import OpenAI  # or use LangChain
from chatbot.auth import client_llm

query = input("What do you want to know? ")
results = retrieve_answer(query)

best_context = results[0]['expanded_context']
prompt = build_prompt(query, best_context)

print("Building messages...")
print("===================")
messages = [{"role": "user", "content": prompt}]

client = client_llm(messages)

print("Response:\n", client)
