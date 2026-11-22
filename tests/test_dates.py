from datetime import date, datetime

import pytest

from playnasty.dates import date_key, parse_date


@pytest.mark.parametrize(
    ("text", "expected"),
    [
        ("230101", date(2023, 1, 1)),
        ("241122", date(2024, 11, 22)),
        ("  241122\n", date(2024, 11, 22)),  # surrounding whitespace is stripped
        ("240229", date(2024, 2, 29)),  # leap day
    ],
)
def test_parse_date_valid(text: str, expected: date) -> None:
    assert parse_date(text) == expected


@pytest.mark.parametrize(
    "text",
    [
        "",
        "2411",  # too short
        "2411221",  # too long
        "24-11-22",  # separators
        "24112a",  # letter
        "24 1122",  # inner space
        "٢٤١١٢٢",  # non-ASCII digits
        "241122\n5",  # trailing junk after a newline
    ],
)
def test_parse_date_bad_format(text: str) -> None:
    with pytest.raises(ValueError, match="6 digits"):
        parse_date(text)


@pytest.mark.parametrize("text", ["241301", "240230", "230229", "241100", "241132"])
def test_parse_date_not_a_calendar_date(text: str) -> None:
    with pytest.raises(ValueError, match="not a real calendar date"):
        parse_date(text)


@pytest.mark.parametrize("value", [241122, None, b"241122", date(2024, 11, 22)])
def test_parse_date_wrong_type(value: object) -> None:
    with pytest.raises(TypeError):
        parse_date(value)  # ty: ignore[invalid-argument-type]


def test_date_key_round_trip() -> None:
    assert date_key(parse_date("070304")) == "070304"


def test_date_key_accepts_datetime() -> None:
    assert date_key(datetime(2023, 1, 1, 12, 30)) == "230101"


@pytest.mark.parametrize("value", ["230101", 230101, None])
def test_date_key_wrong_type(value: object) -> None:
    with pytest.raises(TypeError):
        date_key(value)  # ty: ignore[invalid-argument-type]
