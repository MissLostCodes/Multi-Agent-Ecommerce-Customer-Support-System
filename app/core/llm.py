# DeprecationWarning
from google import genai
from google.genai import types
from dotenv import load_dotenv
import os


class LLM:
    _client = None

    def __init__(self, model="gemini-2.5-flash"):
        if LLM._client is None:
            load_dotenv()  # load .env file

            api_key = os.getenv("GOOGLE_API_KEY")
            if not api_key:
                raise ValueError("GOOGLE_API_KEY not found in .env")

            LLM._client = genai.Client(api_key=api_key)

        self.client = LLM._client
        self.model = model

    def generate(self, prompt: str):
        response = self.client.models.generate_content(
            model=self.model,
            contents =  prompt,
            config=types.GenerateContentConfig(
                temperature=0.3
            )
        )

        return response.text