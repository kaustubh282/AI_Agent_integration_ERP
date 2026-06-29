from tools.fees_outstanding_tool import get_fees_outstanding


def test_get_fees_outstanding_for_class():
    result = get_fees_outstanding({"class_name": "8A"})

    assert result["status"] == "success"
    assert len(result["data"]) == 2
    assert {record["student"]["name"] for record in result["data"]} == {
        "Rahul Sharma",
        "Priya Patel",
    }


def test_get_fees_outstanding_for_single_student():
    result = get_fees_outstanding(
        {"student_name": "Rahul Sharma", "class_name": "8A"}
    )

    assert result["status"] == "success"
    assert result["data"][0]["fees"]["outstanding_fees"] == 5000
