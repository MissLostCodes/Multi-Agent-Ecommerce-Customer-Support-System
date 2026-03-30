import chromadb
from app.rag.gemini_embedder import GeminiEmbedder

class RAGPipeline:
    def __init__(self):
        self.client = chromadb.Client(
            settings=chromadb.config.Settings(
                persist_directory="./chroma_db"
            )
        )
        self.embedder = GeminiEmbedder()

    def get_collection(self, classification):
        mapping = {
            "refund": "policies_returns_refunds",
            "shipping": "policies_shipping_delivery",
            "cancellation": "policies_cancellations",
            "dispute": "policies_disputes",
            "marketplace": "policies_marketplace",
            "promotions": "policies_promotions"
        }

        return mapping.get(classification, "policies_returns_refunds")

    def run(self, input):
        query = input["query"]
        classification = input["classification"]

        collection_name = self.get_collection(classification)

        print(f"🔍 Routing to collection: {collection_name}")

        collection = self.client.get_collection(collection_name)

        emb = self.embedder.embed([query])[0]

        results = collection.query(
            query_embeddings=[emb],
            n_results=3,
            include=["documents", "metadatas"]
        )

        docs = results.get("documents", [[]])[0]

        if len(docs) < 2:
            return None

        return results