from uuid import UUID


def validate_uuid(value: str) -> bool:
    try:
        uuid_obj = UUID(value)
        return str(uuid_obj) == value
    except ValueError:
        return False
