from multi_erp_etl.adapters.json_erp import JsonErpAdapter
from multi_erp_etl.pipeline import run_pipeline


def test_isolates_bad_records_and_keeps_good_ones():
    adapter = JsonErpAdapter()
    raw_records = [
        {
            "invoice_id": 1,
            "customer": {"name": "Good Co", "document": "111"},
            "issued_at": "2026-01-01T00:00:00",
            "total": 100,
        },
        {
            "invoice_id": 2,
            "customer": {"name": "Bad Co", "document": ""},  # invalid: empty document
            "issued_at": "2026-01-02T00:00:00",
            "total": 50,
        },
    ]
    errors = []
    results = run_pipeline(adapter, raw_records, on_error=lambda exc, raw: errors.append(raw))

    assert len(results) == 1
    assert results[0].customer_name == "Good Co"
    assert len(errors) == 1
    assert errors[0]["invoice_id"] == 2
