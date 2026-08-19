"""Adapter for an XML-based ERP export (flat attributes, BR date format)."""

from __future__ import annotations

import xml.etree.ElementTree as ET
from collections.abc import Iterable
from datetime import datetime

from ..schema import CanonicalInvoice


class XmlErpAdapter:
    name = "xml_erp"

    def parse(self, raw_records: Iterable[str | ET.Element]) -> Iterable[CanonicalInvoice]:
        for raw in raw_records:
            element = ET.fromstring(raw) if isinstance(raw, str) else raw
            issue_date = datetime.strptime(  # noqa: DTZ007 - source dates are calendar-only, no TZ info
                element.attrib["data_emissao"], "%d/%m/%Y"
            ).date()
            yield CanonicalInvoice(
                source_system=self.name,
                external_id=element.attrib["numero"],
                customer_name=element.findtext("cliente/nome", default="").strip(),
                customer_document=element.findtext("cliente/documento", default="").strip(),
                issue_date=issue_date,
                total_amount=float(element.findtext("valor_total", default="0")),
                currency=element.attrib.get("moeda", "BRL"),
                branch=element.attrib.get("filial"),
            )
