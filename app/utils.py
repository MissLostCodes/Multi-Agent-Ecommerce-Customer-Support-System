import json
import re

def parse_triage_output(output):
    text = str(output)

    print("🔍 RAW TRIAGE OUTPUT:", text)

    try:
        # 🔥 Extract JSON block
        match = re.search(r"\{.*\}", text, re.DOTALL)
        if match:
            parsed = json.loads(match.group())
            print("✅ PARSED:", parsed)
            return parsed
    except Exception as e:
        print("❌ PARSE ERROR:", e)

    return {"classification": "other", "confidence": 0, "questions": []}