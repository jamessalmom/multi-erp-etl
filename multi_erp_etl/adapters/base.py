"""Adapter protocol: every ERP source implements `parse`."""

from __future__ import annotations

from collections.abc import Iterable
from typing import Protocol

from ..schema import CanonicalInvoice


class ErpAdapter(Protocol):
    name: str

    def parse(self, raw_records: Iterable[dict]) -> Iterable[CanonicalInvoice]:
        ...
