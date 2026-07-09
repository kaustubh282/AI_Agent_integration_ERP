from clients.erp_api_client import ERPAPIClient
from config.settings import settings


def get_fees_outstanding(parameters: dict) -> dict:
    class_name = parameters.get("class_name")

    client = ERPAPIClient()

    if settings.ERP_DATA_MODE == "api":
        records = client.get_students_with_outstanding_fees(class_name=class_name)

        if not records:
            return {
                "status": "not_found",
                "message": (
                    "Outstanding fees data is not available from the ERP API yet. "
                    "The current endpoint is returning an empty response for the available students. "
                    "A student with fee records or the correct ERP endpoint is required."
                ),
            }

        return {
            "status": "success",
            "type": "fees_outstanding",
            "data": records,
        }

    records = client.get_students_with_outstanding_fees(class_name=class_name)

    if not records:
        return {
            "status": "not_found",
            "message": "No outstanding fees found.",
        }

    return {
        "status": "success",
        "type": "fees_outstanding",
        "data": records,
    }
