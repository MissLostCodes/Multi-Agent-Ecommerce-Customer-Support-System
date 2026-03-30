from pydantic import BaseModel

class Output(BaseModel):
    classification: str
    confidence: float
    questions: list
    decision: str
    rationale: str
    citations: list
    response: str
    notes: str
