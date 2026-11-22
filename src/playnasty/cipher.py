"""Modified two-square Polybius cipher, keyed by a date. A toy: not for real encryption.

Both 6x6 boxes start as A-Z then 0-9, read row by row. Each digit of the YYMMDD key spins
one column, then one row: box 1 right and down, box 2 left and up. A character at
(row, col) in its box becomes the character at (col, row) in the same box. Characters at
even indexes use box 1 and odd indexes use box 2, so applying the transform twice gives back
the original text (plus a trailing X if the length was odd).
"""

from datetime import date

from playnasty.dates import date_key

ALPHABET = "ABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789"
SIZE = 6
PAD = "X"

type Grid = list[list[str]]


def _base_grid() -> Grid:
    """Return the unspun 6x6 grid."""
    return [list(ALPHABET[i : i + SIZE]) for i in range(0, len(ALPHABET), SIZE)]


def _rotate(items: list[str], shift: int, *, forward: bool) -> list[str]:
    """Rotate items by shift places.

    The slicing matches the original script exactly: a shift of 6-9 leaves the line
    unchanged (it is not taken mod 6), so text encoded with older versions still decodes.
    """
    if forward:
        return items[shift:] + items[:shift]
    return items[-shift:] + items[:-shift]


def _spin(key: str, *, forward: bool) -> Grid:
    """Return the base grid spun by the key: columns first, then rows."""
    grid = _base_grid()
    shifts = [int(digit) for digit in key]
    for col, shift in enumerate(shifts):
        column = _rotate([row[col] for row in grid], shift, forward=forward)
        for row, char in zip(grid, column, strict=True):
            row[col] = char
    return [_rotate(row, shift, forward=forward) for row, shift in zip(grid, shifts, strict=True)]


def _positions(grid: Grid) -> dict[str, tuple[int, int]]:
    """Map each character to its (row, col) in the grid."""
    return {char: (r, c) for r, row in enumerate(grid) for c, char in enumerate(row)}


def format_grid(grid: Grid) -> str:
    """Return the grid as text, one row per line."""
    return "\n".join(" ".join(row) for row in grid)


class PlaynastyCipher:
    """The two cipher boxes for one date key."""

    def __init__(self, key_date: date | None = None) -> None:
        """Build the boxes for key_date, or for today when it is None."""
        self.key_date = date.today() if key_date is None else key_date
        self.key = date_key(self.key_date)  # checks the type
        self.box1 = _spin(self.key, forward=True)
        self.box2 = _spin(self.key, forward=False)
        self._pos1 = _positions(self.box1)
        self._pos2 = _positions(self.box2)

    def transform(self, text: str) -> str:
        """Encode or decode text (the same operation).

        Drops whitespace, upper-cases, and pads an odd length with X. Raises TypeError for a
        non-string and ValueError for characters outside A-Z and 0-9.
        """
        if not isinstance(text, str):
            msg = f"text must be a str, got {type(text).__name__}"
            raise TypeError(msg)
        cleaned = "".join(text.split()).upper()
        bad = sorted({char for char in cleaned if char not in self._pos1})
        if bad:
            msg = f"only A-Z, 0-9 and spaces are allowed; got {''.join(bad)!r}"
            raise ValueError(msg)
        if len(cleaned) % 2:
            cleaned += PAD

        output = []
        for i, char in enumerate(cleaned):
            box, pos = (self.box1, self._pos1) if i % 2 == 0 else (self.box2, self._pos2)
            row, col = pos[char]
            output.append(box[col][row])
        return "".join(output)
