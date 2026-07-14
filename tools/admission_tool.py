from clients.erp_api_client import ERPAPIClient


def get_new_admissions(parameters: dict) -> dict:
    date_range = parameters.get("date_range")
    class_name = parameters.get("class_name")
    show_all = parameters.get("show_all", False)

    client = ERPAPIClient()

    admissions = client.get_admissions(
        date_range=date_range,
        class_name=class_name,
    )

    if not admissions:
        return {
            "status": "not_found",
            "message": "No admission records found for the requested filters.",
        }

    return {
        "status": "success",
        "type": "new_admission",
        "show_all": show_all,
        "filters": {
            "date_range": date_range or "all",
            "class_name": class_name or "All",
        },
        "data": admissions,
    }
