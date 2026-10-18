"""Example usage for LLM-as-a-Judge Evaluation Rubric Grader & Score Variance Auditor."""
from client import AgentEvalRubricAuditor

if __name__ == "__main__":
    res = AgentEvalRubricAuditor.grade_trajectory(
        {"task_id": "eval_code_refactor"},
        {"correctness": 0.5, "security": 0.3, "efficiency": 0.2},
        {"correctness": 95, "security": 100, "efficiency": 90}
    )
    print("Composite Score:", res["composite_score"], "Grade:", res["grade"])
