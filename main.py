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

    # ---------------------------
    # 1. Ticket Status
    # ---------------------------
    ticket_match = re.search(r"ticket\s*(\d+)", q_lower)
    if ticket_match and "status" in q_lower:
        return {
            "name": "get_ticket_status",
            "arguments": json.dumps({
                "ticket_id": int(ticket_match.group(1))
            })
        }

    # ---------------------------
    # 2. Schedule Meeting
    # ---------------------------
    meeting_match = re.search(
        r"(\d{4}-\d{2}-\d{2}).*?(\d{2}:\d{2}).*?(room\s*[a-z0-9]+)",
        q_lower
    )
    if meeting_match and "schedule" in q_lower:
        return {
            "name": "schedule_meeting",
            "arguments": json.dumps({
                "date": meeting_match.group(1),
                "time": meeting_match.group(2),
                "meeting_room": meeting_match.group(3).title()
            })
        }

    # ---------------------------
    # 3. Expense Balance
    # ---------------------------
    emp_match = re.search(r"employee\s*(\d+)", q_lower)
    if emp_match and "expense" in q_lower:
        return {
            "name": "get_expense_balance",
            "arguments": json.dumps({
                "employee_id": int(emp_match.group(1))
            })
        }

    # ---------------------------
    # 4. Performance Bonus
    # ---------------------------
    bonus_match = re.search(r"employee\s*(\d+).*?(\d{4})", q_lower)
    if bonus_match and "bonus" in q_lower:
        return {
            "name": "calculate_performance_bonus",
            "arguments": json.dumps({
                "employee_id": int(bonus_match.group(1)),
                "current_year": int(bonus_match.group(2))
            })
        }

    # ---------------------------
    # 5. Office Issue
    # ---------------------------
    issue_match = re.search(r"issue\s*(\d+)", q_lower)
    dept_match = re.search(r"department\s*([a-z]+)", q_lower)

    if issue_match and dept_match and "report" in q_lower:
        return {
            "name": "report_office_issue",
            "arguments": json.dumps({
                "issue_code": int(issue_match.group(1)),
                "department": dept_match.group(1).title()
            })
        }

    # If nothing matches
    return {
        "name": "get_ticket_status",
        "arguments": json.dumps({
            "ticket_id": 0
        })
    }
