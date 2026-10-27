# multi-erp-etl

Converts invoice and order data from different ERP exports (JSON or XML, each with its own shape and field names) into one canonical schema, so the reporting code downstream never has to check which ERP a record came from.

## How it works

```
raw ERP record (dict / XML) --> Adapter.parse() --> CanonicalInvoice --> validate()
```

- `schema.py` holds the target `CanonicalInvoice` dataclass.
- `adapters/` has one adapter per source format (`JsonErpAdapter`, `XmlErpAdapter`). A new source only needs a `parse()`.
- `pipeline.py` runs an adapter over a batch. A bad record does not stop the batch: it is passed to `on_error` and the rest goes on.

## Quick start

```python
from multi_erp_etl.adapters.json_erp import JsonErpAdapter
from multi_erp_etl.pipeline import run_pipeline

adapter = JsonErpAdapter()
invoices = run_pipeline(adapter, raw_json_records, on_error=lambda exc, raw: log.warning(exc))
```

## Adding a new ERP source

Implement the `ErpAdapter` protocol in `adapters/base.py`: a `name` and a `parse()` generator that yields `CanonicalInvoice` objects. Nothing else in the pipeline changes.

## Development

```bash
pip install pytest ruff
pytest
ruff check .
```

## License

MIT, see [LICENSE](LICENSE).
