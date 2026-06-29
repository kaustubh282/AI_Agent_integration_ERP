import os
from pathlib import Path

import pytest

@pytest.fixture(autouse=True)
def project_root(monkeypatch):
    root = Path(__file__).resolve().parents[1]
    monkeypatch.chdir(root)
    return root

@pytest.fixture
def fixed_today():
    from datetime import date
    from unittest.mock import patch

    with patch("clients.erp_api_client.date") as mock_date:
        mock_date.today.return_value = date(2026, 6, 29)
        yield date(2026, 6, 29)
