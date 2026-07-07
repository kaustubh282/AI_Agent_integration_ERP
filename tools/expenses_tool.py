from clients.erp_api_client import ERPAPIClient


def get_expenses(parameters: dict) -> dict:
    date_range = parameters.get("date_range")

    client = ERPAPIClient()
    expenses = client.get_expenses()

    if not expenses:
        return {"status": "not_found", "message": "No expense records found."}

    return {
        "status": "success",
        "type": "expenses",
        "date_range": date_range,
        "data": expenses,
    }