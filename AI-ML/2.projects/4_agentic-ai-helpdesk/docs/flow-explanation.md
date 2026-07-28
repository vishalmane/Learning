# Agentic Helpdesk Flow

![Agentic AI Helpdesk Flow](agent-flow.svg)

## Sample Request

```json
{
  "user_id": "123",
  "query": "My VPN stopped working"
}
```

## Step By Step

| Step | Node | Input received | What it does | What it creates or returns |
|---:|---|---|---|---|
| 1 | User Request | `user_id`, `query` | FastAPI validates the request body and starts the graph. | Initial state with `user_id`, `user_query`, `conversation_history`, and `trace_id`. |
| 2 | Planner | `user_query` | Uses Gemini, or fallback logic if no key is configured, to create an execution plan. | `plan`, for example `["Search support knowledge", "Run VPN diagnostics", "Determine root cause", "Escalate if needed"]`. |
| 3 | Governance | `user_query`, `plan` | Runs deterministic policy rules for password reset, account deletion, account disablement, access removal, and other sensitive operations. Optional LLM classification can supplement rules. | `approval_required` and governance metadata. If sensitive, routes to `human_review`; otherwise routes to `retriever`. |
| 4 | Retriever | `user_query` | Searches the support knowledge base for relevant documents. Current local implementation uses an in-memory retriever with production seams for pgvector ingestion. | `retrieved_docs`, including document content, source, metadata, and score. |
| 5 | Tool Executor | `user_id`, `user_query`, `plan` | Selects registered tools based on request intent. A VPN query calls `check_vpn_status`; ticket/escalation language calls `create_ticket`. | `tool_output`, for example VPN status with `connected: false` and `error: "MFA timeout"`. |
| 6 | Reasoning | `user_query`, `plan`, `retrieved_docs`, `tool_output`, `conversation_history` | Uses Gemini, or fallback logic, to combine knowledge and tool results into a structured resolution. | `reasoning_output` with `confidence`, `summary`, `recommended_action`, and `escalation_required`. |
| 7 | Memory | `user_id`, `reasoning_output` | Saves the completed interaction into short-term memory using Redis when available, otherwise an in-process fallback. | Saved memory item containing query, plan, reasoning, and timestamp. |
| 8 | Response | `approval_required`, `reasoning_output` | Formats the final user-facing answer. If approval is required, returns the human approval message instead. | `final_answer`. |

## Example Standard Output

```json
{
  "answer": "The request appears related to a VPN failure caused by MFA timeout.\n\nRecommended action: Ask the user to retry MFA, confirm network connectivity, and escalate if MFA continues to time out.",
  "plan": [
    "Search support knowledge",
    "Run VPN diagnostics",
    "Determine root cause",
    "Escalate if needed"
  ],
  "approval_required": false,
  "trace_id": "generated-trace-id",
  "execution_trace": [
    {
      "node_name": "planner",
      "received": {
        "user_query": "My VPN stopped working"
      },
      "action": "Creates an execution plan for the support request using the configured LLM, with deterministic fallback logic if no key is configured.",
      "returned": {
        "plan": [
          "Search support knowledge",
          "Run VPN diagnostics",
          "Determine root cause",
          "Escalate if needed"
        ]
      }
    }
  ]
}
```

## Sensitive Request Example

```json
{
  "user_id": "123",
  "query": "Please remove access for this account"
}
```

This request matches the access-removal governance rule. The graph routes:

```text
Planner -> Governance -> Human Review -> Response
```

It returns:

```json
{
  "approval_required": true,
  "answer": "This request requires human approval before any sensitive account operation can be performed."
}
```
