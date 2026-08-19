# multi-erp-etl

Normalizes invoice/order data from **heterogeneous ERP exports** (JSON,
XML — different shapes, different field names) into one canonical schema,
so BI and reporting code never has to branch on "which ERP did this come
from".

Generalized from integration work across TOTVS-, SAP- and Omie-style
exports feeding a data warehouse.

## How it works

```
raw ERP record (dict / XML) --> Adapter.parse() --> CanonicalInvoice --> validate()
```

- `schema.py` — the target `CanonicalInvoice` dataclass
- `adapters/` — one adapter per source shape (`JsonErpAdapter`, `XmlErpAdapter`); add your own by implementing `parse()`
- `pipeline.py` — runs an adapter over a batch, **isolates bad rows** instead of failing the whole batch, and routes them to `on_error`

## Quick start

```python
from multi_erp_etl.adapters.json_erp import JsonErpAdapter
from multi_erp_etl.pipeline import run_pipeline

adapter = JsonErpAdapter()
invoices = run_pipeline(adapter, raw_json_records, on_error=lambda exc, raw: log.warning(exc))
```

## Adding a new ERP source

Implement the `ErpAdapter` protocol (`adapters/base.py`) — just a `name`
and a `parse()` generator that yields `CanonicalInvoice` instances. No
changes needed anywhere else in the pipeline.

## Development

```bash
pip install pytest ruff
pytest
ruff check .
```

## License

MIT — see [LICENSE](LICENSE).
