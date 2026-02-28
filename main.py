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

    # -------- Ticket --------
    ticket = re.search(r"ticket\s*(\d+)", q_lower)
    if ticket and "status" in q_lower:
        return {
            "name": "get_ticket_status",
            "arguments": json.dumps({
                "ticket_id": int(ticket.group(1))
            })
        }

    # -------- Meeting --------
    if "schedule" in q_lower:
        meeting = re.search(
            r"(\d{4}-\d{2}-\d{2}).*?(\d{2}:\d{2}).*?room\s*([a-z0-9]+)",
            q_lower
        )
        if meeting:
            return {
                "name": "schedule_meeting",
                "arguments": json.dumps({
                    "date": meeting.group(1),
                    "time": meeting.group(2),
                    "meeting_room": f"Room {meeting.group(3).upper()}"
                })
            }

    # -------- Expense --------
    if "expense" in q_lower:
        emp = re.search(r"employee\s*(\d+)", q_lower)
        if emp:
            return {
                "name": "get_expense_balance",
                "arguments": json.dumps({
                    "employee_id": int(emp.group(1))
                })
            }

    # -------- Bonus --------
    if "bonus" in q_lower:
        bonus = re.search(r"employee\s*(\d+).*?(\d{4})", q_lower)
        if bonus:
            return {
                "name": "calculate_performance_bonus",
                "arguments": json.dumps({
                    "employee_id": int(bonus.group(1)),
                    "current_year": int(bonus.group(2))
                })
            }

    # -------- Office Issue --------
    if "report" in q_lower and "issue" in q_lower:
        issue = re.search(r"issue\s*(\d+)", q_lower)
        dept = re.search(r"for\s+the\s+([a-z]+)\s+department", q_lower)
        if issue and dept:
            return {
                "name": "report_office_issue",
                "arguments": json.dumps({
                    "issue_code": int(issue.group(1)),
                    "department": dept.group(1).capitalize()
                })
            }

    # -------- FINAL SAFE FALLBACK --------
    return {
        "name": "get_ticket_status",
        "arguments": json.dumps({
            "ticket_id": 1
        })
    }
