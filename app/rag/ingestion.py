import os
import chromadb
from langchain_text_splitters import RecursiveCharacterTextSplitter
import uuid
from app.rag.gemini_embedder import GeminiEmbedder


class IngestionPipeline:
    def __init__(self, data_path="data/policies"):
        self.data_path = data_path
        self.embedder = GeminiEmbedder()
        self.client = chromadb.Client()

        self.splitter = RecursiveCharacterTextSplitter(
            chunk_size=500,
            chunk_overlap=100
        )

    def get_collection_name(self, filename):
        base = os.path.splitext(filename)[0]
        return f"policies_{base}"

    def load_documents(self):
        docs = []

        for file in os.listdir(self.data_path):
            path = os.path.join(self.data_path, file)

            if file.endswith(".txt") or file.endswith(".md"):
                with open(path, "r", encoding="utf-8") as f:
                    text = f.read()

                    docs.append({
                        "text": text,
                        "source": file,
                        "collection": self.get_collection_name(file)
                    })

        print(f"Loaded {len(docs)} documents")
        return docs

    def chunk_documents(self, docs):
        all_chunks = []

        for doc in docs:
            chunks = self.splitter.split_text(doc["text"])

            for i, chunk in enumerate(chunks):
                all_chunks.append({
                    "id": str(uuid.uuid4()),
                    "text": chunk,
                    "collection": doc["collection"],
                    "metadata": {
                        "source": doc["source"],
                        "chunk_id": i
                    }
                })

        return all_chunks

    def embed_and_store(self, chunks):
        # group by collection
        collection_map = {}

        for chunk in chunks:
            col = chunk["collection"]
            if col not in collection_map:
                collection_map[col] = []
            collection_map[col].append(chunk)

        #store per collection
        for col_name, col_chunks in collection_map.items():
            print(f"Storing in collection: {col_name}")

            collection = self.client.get_or_create_collection(col_name)

            texts = [c["text"] for c in col_chunks]
            embeddings = self.embedder.embed(texts)

            collection.add(
                ids=[c["id"] for c in col_chunks],
                embeddings=embeddings,
                documents=texts,
                metadatas=[c["metadata"] for c in col_chunks]
            )

    def run(self):
        print("Loading documents...")
        docs = self.load_documents()

        print("Chunking documents...")
        chunks = self.chunk_documents(docs)

        print(f"Total chunks: {len(chunks)}")

        print("Embedding + storing...")
        self.embed_and_store(chunks)

        print("✅ Ingestion complete!")