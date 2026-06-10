import os


def chunk_text(text, size=400, overlap=50):
    chunks = []
    start = 0
    while start < len(text):
        chunks.append(text[start:start + size])
        start += size - overlap
    return chunks


def chunk_documents(folder="documents"):
    results = []
    for filename in os.listdir(folder):
        if not filename.endswith(".txt"):
            continue
        path = os.path.join(folder, filename)
        with open(path, "r", encoding="utf-8") as f:
            text = f.read()
        lines = text.splitlines()
        lines = [l for l in lines if l.strip() and not set(l.strip()) <= {"=", "-"}]
        text = "\n".join(lines)
        for chunk in chunk_text(text):
            results.append({"text": chunk, "source": filename})
    return results


if __name__ == "__main__":
    chunks = chunk_documents()
    print(f"Total chunks: {len(chunks)}")
    for c in chunks[:5]:
        print(f"\n--- {c['source']} ---")
        print(c["text"])
