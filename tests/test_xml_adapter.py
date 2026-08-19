from datetime import date

from multi_erp_etl.adapters.xml_erp import XmlErpAdapter

SAMPLE_XML = """
<nota numero="9001" data_emissao="05/01/2026" filial="SP">
    <cliente>
        <nome>Beta Comercio</nome>
        <documento>98.765.432/0001-10</documento>
    </cliente>
    <valor_total>2300.00</valor_total>
</nota>
"""


def test_parses_xml_record():
    adapter = XmlErpAdapter()
    [invoice] = list(adapter.parse([SAMPLE_XML]))
    assert invoice.external_id == "9001"
    assert invoice.customer_name == "Beta Comercio"
    assert invoice.issue_date == date(2026, 1, 5)
    assert invoice.total_amount == 2300.0
    assert invoice.branch == "SP"
