from crewai import Crew, Task
from app.utils import parse_triage_output


class Workflow:
    def __init__(self, agents):
        self.agents = agents

    def run(self, ticket):

        # TRIAGE
        triage_task = Task(
            description=f"Classify: {ticket}",
            expected_output="JSON with classification, confidence, and questions",
            agent=self.agents['triage']
        )

        triage_output = Crew(
            agents=[self.agents['triage']],
            tasks=[triage_task]
        ).kickoff()

        parsed = parse_triage_output(triage_output)
        classification = parsed.get("classification", "other")

        print(f"🧠 Classification: {classification}")

        # RETRIEVER
        retrieval_task = Task(
            description=f"""
Use the tool to retrieve policy.

Input:
{{
  "query": "{ticket}",
  "classification": "{classification}"
}}
""",
            expected_output="Relevant policy snippets with sources",
            agent=self.agents['retriever']
        )

        retrieved_output = Crew(
            agents=[self.agents['retriever']],
            tasks=[retrieval_task]
        ).kickoff()

        # WRITER
        writer_task = Task(
            description=f"""
Ticket: {ticket}

Context:
{retrieved_output}

ONLY use this context. If insufficient → ESCALATE.
""",
            expected_output="Decision, rationale, customer response, citations",
            agent=self.agents['writer']
        )

        writer_output = Crew(
            agents=[self.agents['writer']],
            tasks=[writer_task]
        ).kickoff()

        # COMPLIANCE
        compliance_task = Task(
            description=f"Validate:\n{writer_output}",
            expected_output="APPROVED or corrected response",
            agent=self.agents['compliance']
        )

        final_output = Crew(
            agents=[self.agents['compliance']],
            tasks=[compliance_task]
        ).kickoff()

        return final_output