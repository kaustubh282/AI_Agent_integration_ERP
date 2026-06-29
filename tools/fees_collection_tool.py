from clients.erp_api_client import ERPAPIClient


def get_fees_collection(parameters: dict) -> dict:
    date_range = parameters.get("date_range")
    class_name = parameters.get("class_name")

    client = ERPAPIClient()
    summary = client.get_fees_collection_summary(date_range, class_name)

    if summary["payment_count"] == 0:
        message = "No fee collections found for the selected filters."
        if class_name and date_range:
            message = (
                f"No fee collections found for class {class_name} "
                f"during {date_range.replace('_', ' ')}."
            )
        elif class_name:
            message = f"No fee collections found for class {class_name}."
        elif date_range:
            message = (
                f"No fee collections found for {date_range.replace('_', ' ')}."
            )

        return {"status": "not_found", "message": message}

    return {
        "status": "success",
        "type": "fees_collection",
        "data": summary,
    }
