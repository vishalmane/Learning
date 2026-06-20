from __future__ import annotations

from pydantic import BaseModel, Field


class InvoiceSummary(BaseModel):
    vendor: str = Field(description="Vendor name")
    total: float = Field(description="Total invoice amount")
    currency: str = Field(description="ISO currency code")
    line_items: list[str] = Field(description="Short item names")

