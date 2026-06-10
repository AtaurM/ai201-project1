import os
import chromadb
from dotenv import load_dotenv
from groq import Groq
from sentence_transformers import SentenceTransformer

load_dotenv()

COLLECTION_NAME = "unofficial_guide"
MODEL_NAME = "llama-3.3-70b-versatile"

_embedder = None
_collection = None
_groq = None

def _init():
    global _embedder, _collection, _groq
    if _embedder is None:
        _embedder = SentenceTransformer("all-MiniLM-L6-v2")
    if _collection is None:
        client = chromadb.PersistentClient(path="chroma_db")
        _collection = client.get_collection(COLLECTION_NAME)
    if _groq is None:
        _groq = Groq(api_key=os.getenv("GROQ_API_KEY"))


def retrieve(query, k=5):
    _init()
    embedding = _embedder.encode([query]).tolist()
    results = _collection.query(query_embeddings=embedding, n_results=k)
    chunks = []
    for doc, meta in zip(results["documents"][0], results["metadatas"][0]):
        chunks.append({"text": doc, "source": meta["source"]})
    return chunks


SYSTEM_PROMPT = """You are a helpful assistant that answers questions about CS professors at Hunter College using student reviews.

Answer ONLY using the document excerpts provided below. Do not use any knowledge from your training data.
If the provided excerpts do not contain enough information to answer the question, respond with exactly:
"I don't have enough information on that."

Do not speculate, generalize, or fill in gaps with outside knowledge. Stick strictly to what the excerpts say."""


def ask(question):
    _init()
    chunks = retrieve(question)
    sources = list(dict.fromkeys(c["source"] for c in chunks))

    context = "\n\n".join(
        f"[Source: {c['source']}]\n{c['text']}" for c in chunks
    )

    messages = [
        {"role": "system", "content": SYSTEM_PROMPT},
        {"role": "user", "content": f"Documents:\n{context}\n\nQuestion: {question}"},
    ]

    response = _groq.chat.completions.create(
        model=MODEL_NAME,
        messages=messages,
        temperature=0.2,
    )

    answer = response.choices[0].message.content.strip()
    return {"answer": answer, "sources": sources}


if __name__ == "__main__":
    q = input("Question: ")
    result = ask(q)
    print(f"\n{result['answer']}\n")
    print("Sources:")
    for s in result["sources"]:
        print(f"  - {s}")
