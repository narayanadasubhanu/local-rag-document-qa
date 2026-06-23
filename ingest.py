import pymupdf4llm

markdown = pymupdf4llm.to_markdown(
    "docs/ADC manual pdf.pdf"
)

with open("data/document.md", "w", encoding="utf-8") as f:
    f.write(markdown)

print("PDF converted successfully!")