from app.core.llm import LLM
from app.rag.pipeline import RAGPipeline
from app.agents.tools import Tools
from app.agents.crew_agents import AgentFactory
from app.graph.workflow import Workflow


llm = LLM()

rag = RAGPipeline()
tools = Tools(rag)

factory = AgentFactory(tools)

agents = {
    "triage": factory.triage(),
    "retriever": factory.retriever(),
    "writer": factory.writer(),
    "compliance": factory.compliance()
}

workflow = Workflow(agents)

if __name__ == "__main__":
    ticket = "Cookies arrived melted, want refund"
    result = workflow.run(ticket)
    print(result)

