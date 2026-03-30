class Evaluator:
    def score(self, output):
        score = 0

        if output.citations:
            score += 1
        if "ESCALATE" not in output.response:
            score += 1
        if output.rationale:
            score += 1

        return score
