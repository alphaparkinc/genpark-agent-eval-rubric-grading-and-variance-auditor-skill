"""MCP server for LLM-as-a-Judge Evaluation Rubric Grader & Score Variance Auditor."""
import sys
import json
from client import AgentEvalRubricAuditor

def handle_request(req):
    method = req.get("method")
    if method == "tools/list":
        return {
            "tools": [{
                "name": "grade_agent_trajectory",
                "description": "Grades agent task completion against weighted rubrics and audits score variance",
                "inputSchema": {
                    "type": "object",
                    "properties": {
                        "trajectory": {"type": "object"},
                        "criteria_weights": {"type": "object"},
                        "scores": {"type": "object"}
                    },
                    "required": ["trajectory", "criteria_weights", "scores"]
                }
            }]
        }
    elif method == "tools/call":
        params = req.get("params", {})
        if params.get("name") == "grade_agent_trajectory":
            args = params.get("arguments", {})
            res = AgentEvalRubricAuditor.grade_trajectory(
                args.get("trajectory", {}),
                args.get("criteria_weights", {}),
                args.get("scores", {})
            )
            return {"content": [{"type": "text", "text": json.dumps(res, indent=2)}]}
    return {"error": "Method not found"}

if __name__ == "__main__":
    for line in sys.stdin:
        if line.strip():
            print(json.dumps(handle_request(json.loads(line))))
            sys.stdout.flush()
