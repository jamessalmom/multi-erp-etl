"""multi_erp_etl

Normalizes invoice/order records coming from heterogeneous ERP exports
(XML and JSON, different field names and shapes) into one common schema,
so downstream BI/reporting code never has to know which ERP a record
came from.

Ships with adapters for a couple of generic ERP-shaped payloads
(named after common patterns, not tied to any single vendor's real API).
"""

from .pipeline import run_pipeline
from .schema import CanonicalInvoice

__all__ = ["CanonicalInvoice", "run_pipeline"]
__version__ = "0.1.0"
