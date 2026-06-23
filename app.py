import streamlit as st
import json
import numpy as np
from sklearn.metrics.pairwise import cosine_similarity
from sentence_transformers import SentenceTransformer
from llama_cpp import Llama

st.set_page_config(page_title="Local RAG QA", layout="wide")

@st.cache_resource
def load_models():
    embedder = SentenceTransformer("all-MiniLM-L6-v2")

    llm = Llama(
        model_path="models/qwen2.5-3b-instruct-q4_k_m.gguf",
        n_ctx=4096,
        n_threads=8,
        verbose=False
    )

    return embedder, llm


embedder, llm = load_models()

with open("data/sections_embeddings.json", "r", encoding="utf-8") as f:
    sections = json.load(f)


def retrieve(question, k=3):
    q_emb = embedder.encode([question])
    doc_embs = np.array([s["embedding"] for s in sections])

    scores = cosine_similarity(q_emb, doc_embs)[0]
    top_k = np.argsort(scores)[-k:][::-1]

    return [sections[i] for i in top_k]


def generate_answer(question):
    top_sections = retrieve(question)

    context = "\n\n".join([s["content"] for s in top_sections])

    prompt = f"""
You are a helpful assistant.
Answer ONLY from context.

CONTEXT:
{context}

QUESTION:
{question}
"""

    output = llm(prompt, max_tokens=300, temperature=0.2)

    return output["choices"][0]["text"]


st.title("📄 Local Document Q&A (RAG)")

query = st.text_input("Ask a question from your document")

if query:
    with st.spinner("Thinking..."):
        answer = generate_answer(query)

    st.subheader("Answer")
    st.write(answer)