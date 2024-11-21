from datetime import datetime


def from_string_to_datetime(datetime_str: str):
    return datetime.fromisoformat(datetime_str)
