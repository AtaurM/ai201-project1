import chromadb
from sentence_transformers import SentenceTransformer

model = SentenceTransformer("all-MiniLM-L6-v2")
client = chromadb.PersistentClient(path="chroma_db")
collection = client.get_collection("unofficial_guide")

print("Ready. Type a question to see the top 3 retrieved chunks. Ctrl+C to quit.\n")

while True:
    query = input("Question: ").strip()
    if not query:
        continue
    embeddings = model.encode([query]).tolist()
    results = collection.query(query_embeddings=embeddings, n_results=3)
    print()
    for i, (doc, meta, dist) in enumerate(zip(results["documents"][0], results["metadatas"][0], results["distances"][0]), 1):
        print(f"[{i}] {meta['source']} (distance: {dist:.4f})")
        print(doc)
        print()
