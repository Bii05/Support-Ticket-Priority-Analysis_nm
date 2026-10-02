from flask import Flask, render_template, request, jsonify
from datetime import datetime

app = Flask(__name__)

# Demo data representing the "latest support ticket" for each customer account.
TICKETS = [
    {
        "id": "TKT-0001",
        "account": "Acme Corporation",
        "contact": "John Carter",
        "issue_type": "Technical",
        "description": "The payment gateway is urgent and the service is not working.",
        "status": "New",
        "created_date": "2026-10-01",
    },
    {
        "id": "TKT-0002",
        "account": "Bright Solutions",
        "contact": "Anita Sharma",
        "issue_type": "Technical",
        "description": "The application is slow and there is a delay while loading reports.",
        "status": "New",
        "created_date": "2026-10-01",
    },
    {
        "id": "TKT-0003",
        "account": "Nova Retail",
        "contact": "David Wilson",
        "issue_type": "General",
        "description": "Customer requested general information about account settings.",
        "status": "New",
        "created_date": "2026-10-02",
    },
]

HIGH_KEYWORDS = ["urgent", "not working", "failure"]
MEDIUM_KEYWORDS = ["issue", "slow", "delay"]


def classify_priority(description):
    text = (description or "").lower()

    high_matches = [word for word in HIGH_KEYWORDS if word in text]
    if high_matches:
        return "High", high_matches

    medium_matches = [word for word in MEDIUM_KEYWORDS if word in text]
    if medium_matches:
        return "Medium", medium_matches

    return "Low", []


def analyze_ticket(ticket):
    priority, matched_keywords = classify_priority(ticket["description"])

    if priority == "High":
        assigned_to = "Senior Support Agent"
        action = "High priority ticket detected. Assigned to senior agent."
        task = {
            "created": True,
            "subject": "Urgent Ticket Handling",
            "priority": "High",
            "status": "Not Started",
            "ticket_id": ticket["id"],
        }
    elif priority == "Medium":
        assigned_to = "Support Agent"
        action = "Ticket marked as medium priority. Will be handled shortly."
        task = {"created": False}
    else:
        assigned_to = "Support Queue"
        action = "Ticket is low priority and queued for processing."
        task = {"created": False}

    # The source document describes SLA risk as an optional check for older unresolved tickets.
    try:
        created = datetime.strptime(ticket["created_date"], "%Y-%m-%d").date()
        age_days = (datetime.now().date() - created).days
    except ValueError:
        age_days = 0

    sla_risk = age_days > 2 and ticket["status"] != "Resolved"

    return {
        "ticket": ticket,
        "priority": priority,
        "matched_keywords": matched_keywords,
        "assigned_to": assigned_to,
        "action_message": action,
        "urgent_task": task,
        "sla_breach_risk": sla_risk,
    }


def latest_ticket(account_name):
    matches = [
        t for t in TICKETS
        if t["account"].strip().lower() == account_name.strip().lower()
    ]
    if not matches:
        return None
    return sorted(matches, key=lambda x: x["created_date"], reverse=True)[0]


@app.route("/")
def home():
    return render_template("index.html", accounts=sorted({t["account"] for t in TICKETS}))


@app.post("/api/analyze")
def api_analyze():
    data = request.get_json(silent=True) or {}
    account_name = str(data.get("account_name", "")).strip()

    if not account_name:
        return jsonify({
            "success": False,
            "message": "Please provide an Account Name."
        }), 400

    ticket = latest_ticket(account_name)
    if not ticket:
        return jsonify({
            "success": False,
            "message": f"No support ticket was found for account: {account_name}"
        }), 404

    result = analyze_ticket(ticket)
    return jsonify({"success": True, **result})


@app.get("/api/tickets")
def api_tickets():
    return jsonify(TICKETS)


if __name__ == "__main__":
    app.run(debug=True, host="127.0.0.1", port=5000)
