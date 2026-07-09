from clients.erp_api_client import ERPAPIClient
from config.settings import settings


def get_expenses(parameters: dict) -> dict:
    date_range = parameters.get("date_range")

    client = ERPAPIClient()

    if settings.ERP_DATA_MODE == "api":
        expenses = client.get_expenses()

        if not expenses:
            return {
                "status": "not_found",
                "message": (
                    "Expense data is not available yet from the ERP API. "
                    "The current ERP backend shared so far does not expose a confirmed "
                    "expense reporting endpoint. The API endpoint or controller is required "
                    "to complete this module."
                ),
            }

        return {
            "status": "success",
            "type": "expenses",
            "date_range": date_range,
            "data": expenses,
        }

    expenses = client.get_expenses()

    if not expenses:
        return {
            "status": "not_found",
            "message": "No expense records found.",
        }

    return {
        "status": "success",
        "type": "expenses",
        "date_range": date_range,
        "data": expenses,
    }
