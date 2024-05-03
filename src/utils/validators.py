from functools import partial
from datetime import datetime


def validate_required_properties(obj, required_properties):
    """
    This function checks if all required properties exist and are not empty (after trim for strings).

    Args:
        obj: The object to be validated.
        required_properties: A list of strings representing the required property names.

    Returns:
        None if all properties are valid, otherwise returns a dictionary containing an "error" key with a message.
    """
    missing_or_empty = []
    for prop in required_properties:
        value = getattr(obj, prop)
        if value is None or (isinstance(value, str) and value.strip() == ""):
            missing_or_empty.append(prop)
    if missing_or_empty:
        return {"error": f"Missing required properties: {', '.join(missing_or_empty)}"}
    return None


def date_str_format(date_or_time: str, format: str):
    return datetime.strptime(date_or_time, format)


def validate_time_format(time_str):
    """
    This function validates if the given string is in the format "hh:mm:ss".

    Args:
        time_str: The string to validate.

    Returns:
        True if the format is valid, False otherwise.
    """
    try:
        date_str_format(time_str, "%H:%M:%S")
        return True
    except ValueError:
        return False


def validate_date_format(date_str):
    """
    This function validates if the given string is in the format "YYYY-MM-DD".

    Args:
        date_str: The string to validate.

    Returns:
        True if the format is valid, False otherwise.
    """
    try:
        date = date_str_format(date_str, "%Y-%m-%d")
        return date
    except ValueError:
        return False


def validate_datetime_format(date_str):
    """
    This function validates if the given string is in the format "YYYY-MM-DD HH:mm:ss".

    Args:
        date_str: The string to validate.

    Returns:
        True if the format is valid, False otherwise.
    """
    try:
        date = date_str_format(date_str, "%Y-%m-%d %H:%M:%S")
        return date
    except ValueError:
        return False
