import chromadb
from sentence_transformers import SentenceTransformer
from ingest import chunk_documents

COLLECTION_NAME = "unofficial_guide"

def build_index():
    chunks = chunk_documents()
    model = SentenceTransformer("all-MiniLM-L6-v2")
    client = chromadb.PersistentClient(path="chroma_db")

    try:
        client.delete_collection(COLLECTION_NAME)
    except Exception:
        pass

    collection = client.create_collection(COLLECTION_NAME)
    texts = [c["text"] for c in chunks]
    sources = [c["source"] for c in chunks]
    embeddings = model.encode(texts, show_progress_bar=True).tolist()

    collection.add(
        documents=texts,
        embeddings=embeddings,
        metadatas=[{"source": s} for s in sources],
        ids=[str(i) for i in range(len(chunks))],
    )
    print(f"Indexed {len(chunks)} chunks into '{COLLECTION_NAME}'")


if __name__ == "__main__":
    build_index()
