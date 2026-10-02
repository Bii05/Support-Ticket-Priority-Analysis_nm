# Customer Support Ticket Priority Prediction and Automated Assignment System — VS Code Demo

## Purpose
This is the **first/local demonstration version** of the project. It is designed to run directly from VS Code on a local computer without Salesforce.

It reproduces the behavior documented in the supplied project instructions:
- Account Name input
- Retrieve the latest support ticket for that account
- Analyze the ticket description
- Classify High / Medium / Low
- Assign the appropriate support level
- Create an urgent handling task for High priority
- Perform the documented optional SLA-risk check
- Return a clear final action message

## Important
This local application is a demonstration/simulation of the documented Salesforce + Agentforce workflow. It does not connect to Salesforce and does not require Salesforce credentials.

## Run in VS Code

### 1. Open the folder
Open this project folder in VS Code.

### 2. Create a virtual environment
Windows PowerShell:
```powershell
python -m venv .venv
.venv\Scripts\Activate.ps1
```

Windows Command Prompt:
```bat
python -m venv .venv
.venv\Scripts\activate
```

### 3. Install dependency
```bash
pip install -r requirements.txt
```

### 4. Run
```bash
python app.py
```

### 5. Open the demo
Open:
`http://127.0.0.1:5000`

## Demo accounts

### High
Account: `Acme Corporation`
Description contains `urgent` and `not working`.
Expected:
- Priority: High
- Assigned To: Senior Support Agent
- Urgent Ticket Handling task: Created

### Medium
Account: `Bright Solutions`
Description contains `slow` and `delay`.
Expected:
- Priority: Medium
- Assigned To: Support Agent
- No urgent task

### Low
Account: `Nova Retail`
Description contains none of the configured urgency keywords.
Expected:
- Priority: Low
- Assigned To: Support Queue
- No urgent task

## Priority rules
High:
- urgent
- not working
- failure

Medium:
- issue
- slow
- delay

Low:
- none of the above

## Suggested demo video
1. Open the project in VS Code.
2. Show the folder and `README.md`.
3. Run `pip install -r requirements.txt`.
4. Run `python app.py`.
5. Open the local browser page.
6. Run the High test.
7. Show High priority, Senior Support Agent, and the created urgent task.
8. Run the Medium test.
9. Show Medium priority and Support Agent.
10. Run the Low test.
11. Show Low priority and Support Queue.
12. Briefly show the priority-rule section at the bottom.

The GitHub repository should contain this same project folder. Do not add Salesforce metadata to this first demo repository.
