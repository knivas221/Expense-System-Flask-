from datetime import datetime


def serialize_mongo_db(doc: dict) -> dict:
    serialized_doc = {}
    for key, value in doc.items():
        if isinstance(value, datetime):
            serialized_doc[key] = value.isoformat()
        else:
            serialized_doc[key] = value

    return serialized_doc


def validate_expense_date(date_str, field_name="expense_date"):
    try:
        return datetime.strptime(date_str, "%Y-%m-%d")

    except ValueError:
        raise ValueError(
            f"{field_name} must be in YYYY-MM-DD format"
        )
