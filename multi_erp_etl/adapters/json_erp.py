"""Adapter for a JSON-based ERP export (nested customer object, ISO dates)."""

from __future__ import annotations

from collections.abc import Iterable
from datetime import date

from ..schema import CanonicalInvoice


class JsonErpAdapter:
    name = "json_erp"

    def parse(self, raw_records: Iterable[dict]) -> Iterable[CanonicalInvoice]:
        for rec in raw_records:
            customer = rec.get("customer", {})
            yield CanonicalInvoice(
                source_system=self.name,
                external_id=str(rec["invoice_id"]),
                customer_name=customer.get("name", "").strip(),
                customer_document=customer.get("document", "").strip(),
                issue_date=date.fromisoformat(rec["issued_at"][:10]),
                total_amount=float(rec["total"]),
                currency=rec.get("currency", "BRL"),
                branch=rec.get("branch"),
            )
