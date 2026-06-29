import pytest

from clients.erp_api_client import ERPAPIClient
from core.exceptions import ERPAPIError


def test_load_json_rejects_path_traversal():
    client = ERPAPIClient()

    with pytest.raises(ERPAPIError):
        client.load_json("../students.json")


def test_get_fees_collection_summary_filters_by_class(fixed_today):
    client = ERPAPIClient()
    summary = client.get_fees_collection_summary(class_name="8A")

    assert summary["payment_count"] == 3
    assert summary["total_collected"] == 28000
    assert all(record["class_name"] == "8A" for record in summary["records"])


def test_get_fees_collection_summary_filters_by_date_range(fixed_today):
    client = ERPAPIClient()
    summary = client.get_fees_collection_summary(date_range="today")

    assert summary["payment_count"] == 1
    assert summary["total_collected"] == 5000
