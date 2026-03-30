from google import genai
from google.genai import types
import os
from dotenv import load_dotenv

load_dotenv()


class GeminiEmbedder:
    def __init__(self):
        api_key = os.getenv("GOOGLE_API_KEY")
        if not api_key:
            raise ValueError("GOOGLE_API_KEY not found")

        self.client = genai.Client(api_key=api_key)

        self.model = "gemini-embedding-001"

    def embed(self, texts):
        print("embedder called")

        # Ensure list input
        if isinstance(texts, str):
            texts = [texts]

        response = self.client.models.embed_content(
            model=self.model,
            contents=texts,
            config=types.EmbedContentConfig(
                task_type="RETRIEVAL_DOCUMENT"
            )
        )

        embeddings = [e.values for e in response.embeddings]

        return embeddings