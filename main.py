from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import re
import json

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/execute")
def execute(q: str):

    q_lower = q.lower()

    # ---------------- TICKET STATUS ----------------
    ticket_match = re.search(r"ticket\s*(\d+)", q_lower)
    if ticket_match and "status" in q_lower:
        ticket_id = int(ticket_match.group(1))
        return {
            "name": "get_ticket_status",
            "arguments": json.dumps({
                "ticket_id": ticket_id
            })
        }

    # ---------------- MEETING ----------------
    if "schedule" in q_lower:
        meeting_match = re.search(
            r"(\d{4}-\d{2}-\d{2}).*?(\d{2}:\d{2}).*?room\s*([a-z0-9]+)",
            q_lower
        )
        if meeting_match:
            return {
                "name": "schedule_meeting",
                "arguments": json.dumps({
                    "date": meeting_match.group(1),
                    "time": meeting_match.group(2),
                    "meeting_room": f"Room {meeting_match.group(3).upper()}"
                })
            }

    # ---------------- EXPENSE ----------------
    if "expense" in q_lower:
        emp_match = re.search(r"employee\s*(\d+)", q_lower)
        if emp_match:
            return {
                "name": "get_expense_balance",
                "arguments": json.dumps({
                    "employee_id": int(emp_match.group(1))
                })
            }

    # ---------------- BONUS ----------------
    if "bonus" in q_lower:
        bonus_match = re.search(r"employee\s*(\d+).*?(\d{4})", q_lower)
        if bonus_match:
            return {
                "name": "calculate_performance_bonus",
                "arguments": json.dumps({
                    "employee_id": int(bonus_match.group(1)),
                    "current_year": int(bonus_match.group(2))
                })
            }

    # ---------------- OFFICE ISSUE ----------------
    if "issue" in q_lower and "department" in q_lower:
        issue_match = re.search(r"issue\s*(\d+)", q_lower)
        dept_match = re.search(r"for\s+the\s+([a-z]+)\s+department", q_lower)
        if issue_match and dept_match:
            return {
                "name": "report_office_issue",
                "arguments": json.dumps({
                    "issue_code": int(issue_match.group(1)),
                    "department": dept_match.group(1).capitalize()
                })
            }

    # STRICT fallback
    return {
        "error": "Query not recognized"
    }
