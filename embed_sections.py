import json
from sentence_transformers import SentenceTransformer

model = SentenceTransformer(
    "all-MiniLM-L6-v2"
)

with open(
    "data/sections.json",
    "r",
    encoding="utf-8"
) as f:
    sections = json.load(f)

texts = [
    s["content"]
    for s in sections
]

embeddings = model.encode(
    texts,
    show_progress_bar=True
)

for i, emb in enumerate(embeddings):
    sections[i]["embedding"] = emb.tolist()

with open(
    "data/sections_embeddings.json",
    "w",
    encoding="utf-8"
) as f:
    json.dump(
        sections,
        f
    )

print("Embeddings created!")