import json
from llama_cpp import Llama

print("Loading model...")

llm = Llama(
    model_path="models/qwen2.5-3b-instruct-q4_k_m.gguf",
    n_ctx=4096,
    n_threads=8,
    verbose=False
)

print("Model loaded!")

with open("data/sections.json", "r", encoding="utf-8") as f:
    sections = json.load(f)

catalog = "\n".join(
    [f"{s['id']}: {s['title']}" for s in sections]
)

def find_section(question):

    prompt = f"""
You are a document router.

Sections:
{catalog}

Question:
{question}

Return ONLY the section number.
"""

    response = llm(
        prompt,
        max_tokens=10,
        temperature=0
    )

    text = response["choices"][0]["text"].strip()

    try:
        return int(text)
    except:
        return 0


def answer_question(question):

    section_id = find_section(question)

    section = next(
        (s for s in sections if s["id"] == section_id),
        sections[0]
    )

    prompt = f"""
Answer ONLY from the document section below.

SECTION:
{section['content']}

QUESTION:
{question}

If the answer is not present, say:
"Answer not found in document."
"""

    result = llm(
        prompt,
        max_tokens=300,
        temperature=0.1
    )

    return result["choices"][0]["text"]


while True:

    question = input("\nAsk a question (or type exit): ")

    if question.lower() == "exit":
        break

    answer = answer_question(question)

    print("\nAnswer:")
    print(answer)