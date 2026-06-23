import json
import re

# Read the markdown file created by ingest.py
with open("data/document.md", "r", encoding="utf-8") as f:
    md = f.read()

# Split document into sections based on Markdown headings
parts = re.split(r"(?=^#{1,3}\s)", md, flags=re.MULTILINE)

sections = []

for idx, part in enumerate(parts):
    if part.strip():
        title = part.split("\n")[0]

        sections.append({
            "id": idx,
            "title": title,
            "content": part
        })

# Save sections as JSON
with open("data/sections.json", "w", encoding="utf-8") as f:
    json.dump(
        sections,
        f,
        indent=2,
        ensure_ascii=False
    )

print(f"Created {len(sections)} sections")