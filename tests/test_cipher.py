from datetime import date, timedelta

import pytest

from playnasty import ALPHABET, PlaynastyCipher, format_grid

README_DATE = date(2023, 1, 1)


def all_dates() -> list[date]:
    """Every 7th day from 2000 to 2099, so every key digit pattern is covered."""
    start, end = date(2000, 1, 1), date(2099, 12, 31)
    return [start + timedelta(days=n) for n in range(0, (end - start).days + 1, 7)]


def test_readme_example() -> None:
    assert PlaynastyCipher(README_DATE).transform("HELLO WORLD") == "ZEBNO6OTB9"


def test_key_with_digits_six_to_nine() -> None:
    # Pins the original behaviour: a key digit of 6-9 leaves its line unspun.
    assert PlaynastyCipher(date(1999, 8, 27)).transform("HELLO WORLD") == "HY55O1O65S"


@pytest.mark.parametrize("key_date", all_dates()[::50])
def test_transform_is_its_own_inverse(key_date: date) -> None:
    cipher = PlaynastyCipher(key_date)
    text = ALPHABET + ALPHABET[::-1]
    assert cipher.transform(cipher.transform(text)) == text


def test_boxes_are_permutations_of_the_alphabet() -> None:
    for key_date in all_dates():
        cipher = PlaynastyCipher(key_date)
        for box in (cipher.box1, cipher.box2):
            assert len(box) == 6
            assert all(len(row) == 6 for row in box)
            assert sorted("".join(map("".join, box))) == sorted(ALPHABET)


def test_default_date_is_today() -> None:
    assert PlaynastyCipher().key_date == date.today()


def test_odd_length_is_padded_with_x() -> None:
    cipher = PlaynastyCipher(README_DATE)
    assert cipher.transform("ABC") == cipher.transform("ABCX")
    assert len(cipher.transform("ABC")) == 4


def test_whitespace_and_case_are_ignored() -> None:
    cipher = PlaynastyCipher(README_DATE)
    assert cipher.transform(" hello\tworld\n") == cipher.transform("HELLOWORLD")


def test_empty_text() -> None:
    assert PlaynastyCipher(README_DATE).transform("") == ""


def test_bad_characters_raise() -> None:
    with pytest.raises(ValueError, match="'!,'"):
        PlaynastyCipher(README_DATE).transform("HELLO, WORLD!")


@pytest.mark.parametrize("key_date", ["230101", 230101])
def test_wrong_date_type_raises(key_date: object) -> None:
    with pytest.raises(TypeError):
        PlaynastyCipher(key_date)  # ty: ignore[invalid-argument-type]


def test_wrong_text_type_raises() -> None:
    with pytest.raises(TypeError):
        PlaynastyCipher(README_DATE).transform(123)  # ty: ignore[invalid-argument-type]


def test_format_grid() -> None:
    assert format_grid([["A", "B"], ["C", "D"]]) == "A B\nC D"
