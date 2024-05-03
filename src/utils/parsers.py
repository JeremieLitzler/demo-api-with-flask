from functools import partial
from datetime import datetime

from utils.validators import validate_date_format, validate_time_format


def convert_str_datetime(date_str: str):
    try:
        # Validate format
        result = validate_date_format(date_str)
        if result is False:
            return False

        return result
    except ValueError:
        return None


def extract_time_values(time_str: str):
    """
    This function validates the format of the given string and extracts hours, minutes, seconds as integers.

    Args:
        time_str: The string to process.

    Returns:
        A tuple of (hours, minutes, seconds) as integers, or None if format is invalid.
    """
    try:
        # Validate format
        result = validate_time_format(time_str)
        if result is False:
            return False

        # Split and convert to integers
        hours, minutes, seconds = map(int, time_str.split(":"))
        return hours, minutes, seconds
    except ValueError:
        return None
