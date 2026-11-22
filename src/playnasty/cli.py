"""Command line: playnasty --text TEXT [--date YYMMDD] [--show-boxes]."""

import argparse
from collections.abc import Sequence
from datetime import date

from playnasty.cipher import PlaynastyCipher, format_grid
from playnasty.dates import parse_date


def _date_arg(text: str) -> date:
    """Argparse type for --date: a clean usage error instead of a traceback."""
    try:
        return parse_date(text)
    except ValueError as err:
        raise argparse.ArgumentTypeError(str(err)) from None


def build_parser() -> argparse.ArgumentParser:
    """Return the argument parser."""
    parser = argparse.ArgumentParser(prog="playnasty", description="Playnasty cipher (a toy).")
    parser.add_argument("--text", required=True, help="text to encode or decode")
    parser.add_argument("--date", type=_date_arg, help="date key as YYMMDD (default: today)")
    parser.add_argument("--show-boxes", action="store_true", help="also print both boxes")
    return parser


def main(argv: Sequence[str] | None = None) -> int:
    """Entry point for the `playnasty` command."""
    parser = build_parser()
    args = parser.parse_args(argv)
    cipher = PlaynastyCipher(args.date)
    try:
        result = cipher.transform(args.text)
    except ValueError as err:
        parser.error(str(err))  # exits with status 2
    if args.show_boxes:
        print(f"Cipherbox 1:\n{format_grid(cipher.box1)}\n")
        print(f"Cipherbox 2:\n{format_grid(cipher.box2)}\n")
    print(f"Transformed text: {result}")
    return 0
