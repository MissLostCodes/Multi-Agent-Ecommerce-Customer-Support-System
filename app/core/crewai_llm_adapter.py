# DeprecationWarning
from crewai import LLM as CrewLLM


class CrewAILLMAdapter:
    def __init__(self):
        # ✅ Use CrewAI-native LLM (this fixes LiteLLM error)
        self.llm = CrewLLM(
            model="gemini/gemini-2.0-flash",
            temperature=0.3
        )

    def call(self, messages, **kwargs):
        """
        CrewAI sends messages like:
        [
          {"role": "system", "content": "..."},
          {"role": "user", "content": "..."}
        ]

        We convert to string prompt
        """

        if isinstance(messages, list):
            prompt = "\n".join([m["content"] for m in messages])
        else:
            prompt = str(messages)

        response = self.llm.call(prompt)

        return response