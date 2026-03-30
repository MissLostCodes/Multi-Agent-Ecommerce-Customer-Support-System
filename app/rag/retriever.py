
import chromadb
from app.rag.gemini_embedder import GeminiEmbedder

class Retriever:
    def __init__(self):
        self.embed = GeminiEmbedder()
        self.client = chromadb.Client()
        self.col = self.client.get_or_create_collection("policies")

    def search(self, query, k=3):
        emb = self.embed.encode([query])[0]
        results = self.col.query(
            query_embeddings=[emb],
            n_results=k,
            include=["documents", "metadatas"]
        )
        print("----------retrieved results ----------")
        print(results)
        print("--------------------------------------")
        return results
