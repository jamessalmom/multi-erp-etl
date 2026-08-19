from datetime import date

from multi_erp_etl.adapters.json_erp import JsonErpAdapter


def test_parses_nested_json_record():
    adapter = JsonErpAdapter()
    raw = [{
        "invoice_id": 501,
        "customer": {"name": "Acme Ltda", "document": "12.345.678/0001-90"},
        "issued_at": "2026-03-14T10:00:00",
        "total": 1500.5,
        "branch": "RJ",
    }]
    [invoice] = list(adapter.parse(raw))
    assert invoice.external_id == "501"
    assert invoice.customer_name == "Acme Ltda"
    assert invoice.issue_date == date(2026, 3, 14)
    assert invoice.total_amount == 1500.5
    assert invoice.source_system == "json_erp"
