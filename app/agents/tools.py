from crewai.tools import tool
import json

@tool("Policy Search Tool")
def search_policy(input: str):
    """
    CrewAI ALWAYS sends input as string
    """

    print("🔧 RAW TOOL INPUT:", input)

    try:
        data = json.loads(input)
    except Exception as e:
        print("❌ JSON parse failed:", e)
        return None

    print("✅ PARSED INPUT:", data)

    from app.rag.pipeline import RAGPipeline
    rag = RAGPipeline()

    return rag.run(data)