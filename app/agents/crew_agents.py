from app.core.llm import LLM
from app.core.crewai_llm_adapter import CrewAILLMAdapter
from crewai import Agent
from langchain_groq import ChatGroq
import os
from app.agents.tools import search_policy

from dotenv import load_dotenv
load_dotenv()

class AgentFactory:
    def __init__(self):

        # llm = ChatGroq(temperature=0,
        #                model_name="llama3-70b-8192",
        #                api_key=os.getenv("GROQ_API_KEY"))
        self.llm = "groq/llama-3.1-8b-instant"

    def triage(self):
        return Agent(
            role="Triage Agent",
            backstory="Expert customer support analyst who classifies tickets accurately.",
            goal="""Classify the support ticket into one:
[refund, shipping, cancellation, dispute, marketplace , promotions ]

Also:
- Identify missing info (max 3 questions)
- Return JSON:
{
  "classification": "...",
  "confidence": 0-1,
  "questions": []
}""",
            llm=self.llm,
            verbose=True
        )

    def retriever(self):
        return Agent(
            role="Policy Retriever",
            backstory="Expert in retrieving precise policy documents using tools.",
            goal="""Retrieve ONLY relevant policy excerpts.

You MUST use the tool "Policy Search Tool".

Input format:
{
  "query": "<ticket>",
  "classification": "<category>"
}

Rules:
- DO NOT answer yourself
- ONLY call the tool
- Return tool output directly
""",

            tools=[search_policy],
            llm=self.llm,
            verbose=True
        )

    def writer(self):
        return Agent(
            role="Resolution Writer",
            backstory="Customer support specialist who writes clear, policy-compliant responses.",
            goal="""You MUST follow STRICT rules:

- ONLY use retrieved context
- EVERY claim MUST include citation
- If ANY claim lacks citation → respond "ESCALATE"
- Do NOT infer or assume policy

Output format:
1. Decision (approve/deny/partial/escalate)
2. Rationale (with citations)
3. Customer response (polite, clear)
4. Citations list""",
            llm=self.llm,
            verbose=True
        )

    def compliance(self):
        return Agent(
            role="Compliance Agent",
            backstory="Strict auditor ensuring no hallucinations and enforcing policy adherence.",
            goal="""Validate the response:

Reject if:
- citations < 1
- vague words ("usually", "generally")
- claims not present in context
- missing justification

If invalid → REWRITE or ESCALATE
If valid → APPROVED""",
            llm=self.llm,
            verbose=True
        )