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

    # Ticket
    ticket = re.search(r"ticket (\d+)", q_lower)
    if "status" in q_lower and ticket:
        return {
            "name": "get_ticket_status",
            "arguments": json.dumps({
                "ticket_id": int(ticket.group(1))
            })
        }

    # Meeting
    meeting = re.search(r"on (\d{4}-\d{2}-\d{2}) at (\d{2}:\d{2}) in (.+)", q)
    if "schedule" in q_lower and meeting:
        return {
            "name": "schedule_meeting",
            "arguments": json.dumps({
                "date": meeting.group(1),
                "time": meeting.group(2),
                "meeting_room": meeting.group(3).replace(".", "")
            })
        }

    # Expense
    expense = re.search(r"employee (\d+)", q_lower)
    if "expense" in q_lower and expense:
        return {
            "name": "get_expense_balance",
            "arguments": json.dumps({
                "employee_id": int(expense.group(1))
            })
        }

    # Bonus
    bonus = re.search(r"employee (\d+).*?(\d{4})", q_lower)
    if "bonus" in q_lower and bonus:
        return {
            "name": "calculate_performance_bonus",
            "arguments": json.dumps({
                "employee_id": int(bonus.group(1)),
                "current_year": int(bonus.group(2))
            })
        }

    # Office Issue
    issue = re.search(r"issue (\d+)", q_lower)
    dept = re.search(r"for the (.+?) department", q_lower)
    if "report" in q_lower and issue and dept:
        return {
            "name": "report_office_issue",
            "arguments": json.dumps({
                "issue_code": int(issue.group(1)),
                "department": dept.group(1).title()
            })
        }

    return {
        "name": "unknown",
        "arguments": json.dumps({})
    }
