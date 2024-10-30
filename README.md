# Playnasty Cipher

This script implements a two-square Playfair Cipher variation, nicknamed Playnasty Cipher. It allows encoding and decoding of text based on a date key.

The 6-digit date key is used to 'spin' the rows and columns of the Polybius square the appropriate amount of times, each index of the date used for the respective row or column index. That is how the square is 'shuffled'. First square (for odd indexed characters) is 'spun' right and down, the second square (for even characters in the string) is 'spun' left and up.

The transformation uses the (row, col) index of the input character and returns the character found at (col, row).

#### NOT FOR SERIOUS ENCRYPTION, JUST A TOY EXAMPLE TO PLAY WITH THE CONCEPTS

## Usage

To use the script, run the following command:

```sh
python play_nasty.py --text "YOUR TEXT HERE" --date YYMMDD
```

## Arguments

- `--text`: The text to encode or decode. This argument is required.
- `--date`: The date key in the format YYMMDD. This argument is optional and defaults to the current date.

## Example

```sh
python play_nasty.py --text "HELLO WORLD" --date 230101
```

This will encode or decode the text "HELLO WORLD" using the date key "230101". The output should be:
```sh
Transformed text: ZEBNO6OTB9
```

## License

This project is licensed under the MIT License.