"""Date keys: parse and check YYMMDD input, and turn a date into the 6-digit cipher key."""

import re
from datetime import date, datetime

DATE_FORMAT = "%y%m%d"
# [0-9], not \d: \d also matches non-ASCII digits such as "٢".
_SIX_DIGITS = re.compile(r"[0-9]{6}")


def parse_date(text: str) -> date:
    """Parse a YYMMDD string into a date.

    Strips surrounding whitespace, then requires exactly six ASCII digits that form a real
    calendar date. Raises TypeError for a non-string and ValueError for a bad date.
    """
    if not isinstance(text, str):
        msg = f"date must be a str in YYMMDD format, got {type(text).__name__}"
        raise TypeError(msg)
    cleaned = text.strip()
    if not _SIX_DIGITS.fullmatch(cleaned):
        msg = f"date must be 6 digits in YYMMDD format, got {text!r}"
        raise ValueError(msg)
    try:
        return datetime.strptime(cleaned, DATE_FORMAT).date()
    except ValueError:
        msg = f"{cleaned!r} is not a real calendar date (YYMMDD)"
        raise ValueError(msg) from None


def date_key(value: date) -> str:
    """Return the 6-digit YYMMDD key for a date. Raises TypeError for anything but a date."""
    if not isinstance(value, date):
        msg = f"date key must be a datetime.date, got {type(value).__name__}"
        raise TypeError(msg)
    return value.strftime(DATE_FORMAT)
