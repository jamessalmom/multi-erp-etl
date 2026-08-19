"""The canonical (target) schema every adapter normalizes into."""

from __future__ import annotations

from dataclasses import dataclass
from datetime import date


@dataclass(frozen=True)
class CanonicalInvoice:
    source_system: str
    external_id: str
    customer_name: str
    customer_document: str
    issue_date: date
    total_amount: float
    currency: str = "BRL"
    branch: str | None = None

    def validate(self) -> None:
        if self.total_amount < 0:
            raise ValueError(f"negative total_amount for invoice {self.external_id}")
        if not self.customer_document.strip():
            raise ValueError(f"missing customer_document for invoice {self.external_id}")
