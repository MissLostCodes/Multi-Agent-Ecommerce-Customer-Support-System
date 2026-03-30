from crewai.tools import tool

class Tools:
    def __init__(self, rag_pipeline):
        self.rag = rag_pipeline

    @tool("Policy Search Tool")
    def search_policy(self, input: dict):
        """
        input = {
            "query": "...",
            "classification": "refund"
        }
        """
        return self.rag.run(input)
