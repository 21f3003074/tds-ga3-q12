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

    # 1️⃣ Ticket Status
    m = re.match(r"What is the status of ticket (\d+)\??", q)
    if m:
        return {
            "name": "get_ticket_status",
            "arguments": json.dumps({
                "ticket_id": int(m.group(1))
            })
        }

    # 2️⃣ Meeting
    m = re.match(r"Schedule a meeting on (\d{4}-\d{2}-\d{2}) at (\d{2}:\d{2}) in (.+)\.", q)
    if m:
        return {
            "name": "schedule_meeting",
            "arguments": json.dumps({
                "date": m.group(1),
                "time": m.group(2),
                "meeting_room": m.group(3)
            })
        }

    # 3️⃣ Expense
    m = re.match(r"Show my expense balance for employee (\d+)\.", q)
    if m:
        return {
            "name": "get_expense_balance",
            "arguments": json.dumps({
                "employee_id": int(m.group(1))
            })
        }

    # 4️⃣ Bonus
    m = re.match(r"Calculate performance bonus for employee (\d+) for (\d{4})\.", q)
    if m:
        return {
            "name": "calculate_performance_bonus",
            "arguments": json.dumps({
                "employee_id": int(m.group(1)),
                "current_year": int(m.group(2))
            })
        }

    # 5️⃣ Office Issue
    m = re.match(r"Report office issue (\d+) for the (.+) department\.", q)
    if m:
        return {
            "name": "report_office_issue",
            "arguments": json.dumps({
                "issue_code": int(m.group(1)),
                "department": m.group(2)
            })
        }

    return {"error": "Query not recognized"}
