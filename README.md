# Playnasty Cipher

A two-square Polybius cipher variation, nicknamed Playnasty Cipher. It encodes and decodes text
based on a date key.

The 6-digit date key (YYMMDD) 'spins' the rows and columns of a 6x6 Polybius square (A-Z, 0-9):
each digit of the date spins the row or column with the same index. That is how the square is
'shuffled'. The first square (for characters at even indexes: 1st, 3rd, ...) is spun right and
down; the second square (2nd, 4th, ...) is spun left and up. A digit of 6-9 leaves its row or
column unspun.

The transformation takes the (row, col) of the input character and returns the character at
(col, row) in the same square. So the same command both encodes and decodes.

**Not for serious encryption: just a toy example to play with the concepts.**

## Usage

```sh
uv run playnasty --text "YOUR TEXT HERE" --date YYMMDD
```

- `--text` (required): the text to encode or decode. Letters, digits and spaces only; spaces
  are dropped, lowercase is upper-cased, and an odd length is padded with `X`.
- `--date` (optional, default today): the key as exactly 6 digits, `YYMMDD`, and it must be a
  real calendar date. `241301` or `24-11-22` is rejected with an error.
- `--show-boxes`: also print both cipher squares.

## Example

```sh
uv run playnasty --text "HELLO WORLD" --date 230101
```

Output:

```
Transformed text: ZEBNO6OTB9
```

Run it again on `ZEBNO6OTB9` with the same date to get `HELLOWORLD` back.

## As a library

```python
from datetime import date

from playnasty import PlaynastyCipher, parse_date

cipher = PlaynastyCipher(parse_date("230101"))  # or PlaynastyCipher(date(2023, 1, 1))
cipher.transform("HELLO WORLD")  # 'ZEBNO6OTB9'
```

## Development

Toolchain: `~/Code/local/templates/STANDARDS.md`. Before committing, run:

```sh
uv run ruff check
uv run ruff format --check
uv run ty check
uv run pytest
```

## License

This project is licensed under the MIT License.
