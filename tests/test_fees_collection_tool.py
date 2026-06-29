from tools.fees_collection_tool import get_fees_collection


def test_get_fees_collection_for_class_and_month(fixed_today):
    result = get_fees_collection(
        {"class_name": "8A", "date_range": "this_month"}
    )

    assert result["status"] == "success"
    assert result["type"] == "fees_collection"
    assert result["data"]["total_collected"] == 13000
    assert result["data"]["payment_count"] == 2


def test_get_fees_collection_returns_not_found_when_empty(fixed_today):
    result = get_fees_collection(
        {"class_name": "8B", "date_range": "today"}
    )

    assert result["status"] == "not_found"
    assert "No fee collections found" in result["message"]
