# LangChain Learning Path

Start with chat models, messages, prompts, and output parsers. After that, use LCEL chains to compose model calls with prompts and transformations.

Once basic chains are comfortable, try structured output. It is useful when the application needs reliable JSON-like fields rather than free text.

After prompts and structured output, try tools and agents. Agents combine a model, instructions, and tools so the model can decide when to call functions.

For knowledge-heavy applications, try retrieval augmented generation. RAG loads documents, splits them into chunks, embeds the chunks, retrieves relevant context, and asks the model to answer from that context.

Use LangGraph when a workflow needs explicit state, branching, retries, checkpoints, or a mix of deterministic and model-driven steps.

