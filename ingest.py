import os


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

        # first line is always the professor/course header
        header = lines[0] if lines else ""

        # split into one chunk per review, each starting at "Quality:"
        current = []
        for line in lines[1:]:
            if line.startswith("Quality:") and current:
                results.append({"text": header + "\n" + "\n".join(current), "source": filename})
                current = [line]
            else:
                current.append(line)
        if current:
            results.append({"text": header + "\n" + "\n".join(current), "source": filename})

    return results


if __name__ == "__main__":
    chunks = chunk_documents()
    print(f"Total chunks: {len(chunks)}")
    for c in chunks[:5]:
        print(f"\n--- {c['source']} ---")
        print(c["text"])
