const form = document.querySelector("#ask-form");
const userIdInput = document.querySelector("#user-id");
const queryInput = document.querySelector("#query");
const statusEl = document.querySelector("#status");
const answerText = document.querySelector("#answer-text");
const approvalBadge = document.querySelector("#approval-badge");
const planList = document.querySelector("#plan-list");
const nodeTrace = document.querySelector("#node-trace");
const traceId = document.querySelector("#trace-id");
const submitButton = form.querySelector("button[type='submit']");

document.querySelector("#example-vpn").addEventListener("click", () => {
  queryInput.value = "My VPN stopped working";
  queryInput.focus();
});

document.querySelector("#example-approval").addEventListener("click", () => {
  queryInput.value = "Please remove access for this account";
  queryInput.focus();
});

form.addEventListener("submit", async (event) => {
  event.preventDefault();
  setLoading(true);
  clearError();

  try {
    const response = await fetch("/ask", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({
        user_id: userIdInput.value.trim(),
        query: queryInput.value.trim(),
      }),
    });

    const payload = await response.json();
    if (!response.ok) {
      throw new Error(payload.detail || payload.error || "Request failed");
    }

    renderResult(payload);
  } catch (error) {
    renderError(error);
  } finally {
    setLoading(false);
  }
});

function renderResult(payload) {
  answerText.classList.remove("empty");
  answerText.textContent = payload.answer || "No answer returned.";
  traceId.textContent = payload.trace_id || "-";

  approvalBadge.className = payload.approval_required ? "badge warn" : "badge ok";
  approvalBadge.textContent = payload.approval_required ? "Approval required" : "Approved path";

  planList.replaceChildren();
  for (const step of payload.plan || []) {
    const item = document.createElement("li");
    item.textContent = step;
    planList.appendChild(item);
  }

  renderNodeTrace(payload.execution_trace || []);
}

function renderError(error) {
  answerText.classList.remove("empty");
  answerText.textContent = error.message;
  approvalBadge.className = "badge error";
  approvalBadge.textContent = "Error";
  traceId.textContent = "-";
  planList.replaceChildren();
  nodeTrace.replaceChildren();
}

function setLoading(isLoading) {
  submitButton.disabled = isLoading;
  statusEl.textContent = isLoading ? "Working" : "Ready";
}

function clearError() {
  approvalBadge.className = "badge neutral";
  approvalBadge.textContent = "Running";
}

function renderNodeTrace(trace) {
  nodeTrace.replaceChildren();

  if (!trace.length) {
    const empty = document.createElement("p");
    empty.className = "empty";
    empty.textContent = "No node trace returned.";
    nodeTrace.appendChild(empty);
    return;
  }

  trace.forEach((entry, index) => {
    const details = document.createElement("details");
    details.className = "trace-item";
    details.open = index === 0;

    const summary = document.createElement("summary");
    const order = document.createElement("span");
    order.className = "trace-order";
    order.textContent = String(index + 1);

    const name = document.createElement("strong");
    name.textContent = entry.node_name || "node";

    summary.append(order, name);
    details.appendChild(summary);

    details.appendChild(traceBlock("What input it received", entry.received));
    details.appendChild(traceText("What it does", entry.action));
    details.appendChild(traceBlock("What it returned", entry.returned));
    nodeTrace.appendChild(details);
  });
}

function traceText(title, text) {
  const section = document.createElement("div");
  section.className = "trace-section";

  const label = document.createElement("span");
  label.textContent = title;

  const value = document.createElement("p");
  value.textContent = text || "-";

  section.append(label, value);
  return section;
}

function traceBlock(title, value) {
  const section = document.createElement("div");
  section.className = "trace-section";

  const label = document.createElement("span");
  label.textContent = title;

  const pre = document.createElement("pre");
  pre.textContent = JSON.stringify(value ?? {}, null, 2);

  section.append(label, pre);
  return section;
}
