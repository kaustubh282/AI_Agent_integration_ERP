import pytest

from core.exceptions import ERPValidationError
from core.security import sanitize_message, sanitize_parameters


def test_sanitize_message_strips_control_characters():
    assert sanitize_message("  hello\x00world  ") == "helloworld"


def test_sanitize_message_rejects_empty_input():
    with pytest.raises(ERPValidationError):
        sanitize_message("   ")


def test_sanitize_message_rejects_overlong_input():
    with pytest.raises(ERPValidationError):
        sanitize_message("a" * 2001)


def test_sanitize_parameters_accepts_valid_values():
    result = sanitize_parameters(
        {
            "student_name": "Rahul Sharma",
            "class_name": "8A",
            "date_range": "this_month",
            "exam_name": "Mid Term",
        }
    )

    assert result["class_name"] == "8A"
    assert result["student_name"] == "Rahul Sharma"


def test_sanitize_parameters_rejects_invalid_class_name():
    with pytest.raises(ERPValidationError):
        sanitize_parameters({"class_name": "../../etc"})


def test_sanitize_parameters_rejects_invalid_student_name():
    with pytest.raises(ERPValidationError):
        sanitize_parameters({"student_name": "<script>alert(1)</script>"})
