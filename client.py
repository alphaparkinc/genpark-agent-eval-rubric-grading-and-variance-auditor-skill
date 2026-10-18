"""LLM-as-a-Judge Evaluation Rubric Grader & Score Variance Auditor.
100% Python Standard Library.
"""

import math

class AgentEvalRubricAuditor:
    """Grades agent trajectories across weighted evaluation rubrics and detects scoring variance anomalies."""

    @staticmethod
    def grade_trajectory(trajectory: dict, criteria_weights: dict, scores: dict) -> dict:
        total_weight = sum(criteria_weights.values())
        if total_weight <= 0:
            return {"error": "Total weight must be positive"}

        weighted_sum = 0.0
        details = {}
        for crit, weight in criteria_weights.items():
            score = scores.get(crit, 0.0)
            weighted_sum += score * weight
            details[crit] = {"score": score, "weight": weight, "contribution": round(score * (weight / total_weight), 2)}

        final_score = round(weighted_sum / total_weight, 2)
        score_values = list(scores.values())
        mean = sum(score_values) / max(1, len(score_values))
        variance = sum((s - mean) ** 2 for s in score_values) / max(1, len(score_values))
        std_dev = round(math.sqrt(variance), 2)

        return {
            "task_id": trajectory.get("task_id", "unknown"),
            "composite_score": final_score,
            "score_std_dev": std_dev,
            "grade": "EXEMPLARY" if final_score >= 90 else ("SATISFACTORY" if final_score >= 70 else "NEEDS_IMPROVEMENT"),
            "rubric_details": details
        }
