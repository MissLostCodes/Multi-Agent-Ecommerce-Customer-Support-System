class CrewAILLMAdapter:
    def __init__(self, llm):
        self.llm = llm

    def call(self, prompt, **kwargs):
        return self.llm.generate(prompt)