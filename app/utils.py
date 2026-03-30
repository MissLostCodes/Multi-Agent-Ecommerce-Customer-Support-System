import json

def parse_triage_output(output):
    try:
        return json.loads(output)
    except:
        return {"classification": "other", "confidence": 0, "questions": []}