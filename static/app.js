function useAccount(name) {
    document.getElementById("accountName").value = name;
    analyzeTicket();
}

async function analyzeTicket() {
    const accountName = document.getElementById("accountName").value.trim();
    const loading = document.getElementById("loading");
    const result = document.getElementById("result");
    const error = document.getElementById("error");

    result.classList.add("hidden");
    error.classList.add("hidden");

    if (!accountName) {
        error.textContent = "Please provide an Account Name.";
        error.classList.remove("hidden");
        return;
    }

    loading.classList.remove("hidden");

    try {
        const response = await fetch("/api/analyze", {
            method: "POST",
            headers: {"Content-Type": "application/json"},
            body: JSON.stringify({account_name: accountName})
        });

        const data = await response.json();
        loading.classList.add("hidden");

        if (!response.ok || !data.success) {
            error.textContent = data.message || "Unable to analyze the ticket.";
            error.classList.remove("hidden");
            return;
        }

        const t = data.ticket;
        document.getElementById("ticketId").textContent = t.id;
        document.getElementById("account").textContent = t.account;
        document.getElementById("contact").textContent = t.contact;
        document.getElementById("issueType").textContent = t.issue_type;
        document.getElementById("status").textContent = t.status;
        document.getElementById("description").textContent = t.description;

        document.getElementById("priorityText").textContent = data.priority;
        document.getElementById("assignedTo").textContent = data.assigned_to;
        document.getElementById("keywords").textContent =
            data.matched_keywords.length ? data.matched_keywords.join(", ") : "None";
        document.getElementById("sla").textContent = data.sla_breach_risk ? "Yes" : "No";
        document.getElementById("actionMessage").textContent = data.action_message;

        const priority = document.getElementById("priority");
        priority.textContent = data.priority;
        priority.className = "priority " + data.priority.toLowerCase();

        const taskBox = document.getElementById("taskBox");
        taskBox.classList.toggle("hidden", !data.urgent_task.created);

        document.getElementById("resultTitle").textContent =
            `${t.id} • ${t.account}`;

        result.classList.remove("hidden");
        result.scrollIntoView({behavior: "smooth", block: "start"});
    } catch (err) {
        loading.classList.add("hidden");
        error.textContent = "Could not connect to the local demo server. Make sure Flask is running.";
        error.classList.remove("hidden");
    }
}

document.getElementById("accountName").addEventListener("keydown", function(e) {
    if (e.key === "Enter") analyzeTicket();
});
