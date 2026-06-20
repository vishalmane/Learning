from lc_lab.models import get_chat_model
from lc_lab.schemas import InvoiceSummary


def main() -> None:
    model = get_chat_model().with_structured_output(InvoiceSummary)
    invoice_text = "Invoice from Acme AI Tools: embeddings kit 120 USD, prompt book 30 USD. Total 150 USD."
    result = model.invoke(f"Extract invoice fields from this text: {invoice_text}")
    print(result.model_dump_json(indent=2))


if __name__ == "__main__":
    main()
