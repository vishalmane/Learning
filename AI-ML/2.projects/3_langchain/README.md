# LangChain Lab

A UV-based Python workspace for trying the main LangChain capabilities with Gemini:

- Models, messages, prompts, and output parsing
- LCEL chains
- Tools and agents
- Retrieval augmented generation
- Short-term memory patterns
- Streaming
- Structured output
- LangGraph orchestration
- LangSmith tracing hooks
- A basic Streamlit UI

The current LangChain docs describe `create_agent` as the main configurable agent harness and note that LangChain agents are built on LangGraph for durable execution and persistence-oriented workflows. This scaffold follows that split: simple examples use LangChain directly, while graph-shaped control flow lives under `examples/08_langgraph`.

## Setup

```powershell
uv venv
uv sync --extra dev
Copy-Item .env.example .env
```

Edit `.env` and set `GOOGLE_API_KEY`. You can create one in Google AI Studio.

## Run Examples

```powershell
uv run python examples/01_models_prompts/chat_model.py
uv run python examples/02_chains/lcel_chain.py
uv run python examples/03_agents_tools/tool_agent.py
uv run python examples/04_retrieval_rag/local_rag.py
uv run python examples/05_memory/chat_history.py
uv run python examples/06_streaming/stream_tokens.py
uv run python examples/07_structured_output/extract_invoice.py
uv run python examples/08_langgraph/simple_graph.py
```

## Run UI

```powershell
uv run streamlit run ui/app.py
```

The UI starts in `Demo` mode, which does not call Gemini and does not use quota. Use the sidebar `Live Gemini` option when `GOOGLE_API_KEY` is configured.

## Suggested Learning Order

1. Start with `01_models_prompts` to understand messages and model configuration.
2. Move to `02_chains` for LCEL composition.
3. Try `07_structured_output` before agents, because reliable schemas are useful everywhere.
4. Use `03_agents_tools` for tool calling.
5. Use `04_retrieval_rag` for document Q&A.
6. Use `05_memory` and `06_streaming` to make interactions feel application-ready.
7. Use `08_langgraph` when your workflow needs explicit state and branching.

## LangSmith

Set these in `.env` to trace runs:

```text
LANGSMITH_TRACING=true
LANGSMITH_API_KEY=your-key
LANGSMITH_PROJECT=langchain-lab
```
