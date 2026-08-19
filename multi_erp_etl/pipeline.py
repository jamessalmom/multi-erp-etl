"""Runs one or more adapters and yields validated, normalized invoices.

Records that fail validation are routed to `on_error` instead of raising,
so one bad row from one ERP does not stop the whole batch.
"""

from __future__ import annotations

import logging
from collections.abc import Callable, Iterable

from .adapters.base import ErpAdapter
from .schema import CanonicalInvoice

logger = logging.getLogger("multi_erp_etl.pipeline")


def run_pipeline(
    adapter: ErpAdapter,
    raw_records: Iterable[dict],
    on_error: Callable[[Exception, dict], None] | None = None,
) -> list[CanonicalInvoice]:
    results: list[CanonicalInvoice] = []
    for raw in raw_records:
        try:
            for invoice in adapter.parse([raw]):
                invoice.validate()
                results.append(invoice)
        except Exception as exc:  # noqa: BLE001 - intentionally broad, isolates bad rows
            logger.warning("record_rejected", extra={"adapter": adapter.name, "error": str(exc)})
            if on_error:
                on_error(exc, raw)
    return results
