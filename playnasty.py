import argparse
from datetime import datetime


class PlaynastyCipher:
    """
    Modified two-square Playfair Cipher toy example
    """

    def __init__(self, date: str=datetime.strftime(datetime.now(), "%y%m%d")) -> None:
        self.date_key = date
        self.characters = "ABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789"
        self.cipherbox1 = self.shift_matrix_1()
        self.positions1 = {
            char: (row, col)
            for row in range(6)
            for col, char in enumerate(self.cipherbox1[row])
        }
        self.cipherbox2 = self.shift_matrix_2()
        self.positions2 = {
            char: (row, col)
            for row in range(6)
            for col, char in enumerate(self.cipherbox2[row])
        }

    @staticmethod
    def print_matrix(matrix: list) -> None:
        """
        Print the matrix
        """
        for row in matrix:
            print(row)

    def create_matrix(self) -> list:
        """
        Create the matrix for the cipher
        """
        return [
            list(self.characters[i : i + 6]) for i in range(0, len(self.characters), 6)
        ]

    def shift_matrix_1(self) -> list:
        """
        Shift the matrix based on the date key
        right and down
        """
        # init matrix
        matrix = self.create_matrix()

        # shift cols based on date string
        for col in range(6):
            spin_value = int(self.date_key[col])
            column = [matrix[row][col] for row in range(6)]
            spun_column = column[spin_value:] + column[:spin_value]
            for row in range(6):
                matrix[row][col] = spun_column[row]

        # shift rows based on date string
        for row in range(6):
            spin_value = int(self.date_key[row])
            spun_row = matrix[row][spin_value:] + matrix[row][:spin_value]
            matrix[row] = spun_row

        return matrix

    def shift_matrix_2(self) -> list:
        """
        Reverse shift the matrix based on the date key
        left and up
        """
        # init matrix
        matrix = self.create_matrix()

        # reverse shift cols based on date string
        for col in range(6):
            spin_value = int(self.date_key[col])
            column = [matrix[row][col] for row in range(6)]
            spun_column = column[-spin_value:] + column[:-spin_value]
            for row in range(6):
                matrix[row][col] = spun_column[row]

        # reverse shift rows based on date string
        for row in range(6):
            spin_value = int(self.date_key[row])
            spun_row = matrix[row][-spin_value:] + matrix[row][:-spin_value]
            matrix[row] = spun_row

        return matrix

    def transform(self, text: str) -> str:
        """
        encode/decode the text
        """
        # remove spaces and convert to uppercase
        text = text.replace(" ", "").upper()

        # pad with X if odd length
        if len(text) % 2 != 0:
            text += "X"

        # init output
        output = ""

        # use cipherbox1 for odd chars and cipherbox2 for even chars
        for i, c in enumerate(text):
            # print(f"idx: {i}, char: {c}")
            if i % 2 == 0:  # odd chars
                pos = self.positions1[c]
                char = self.cipherbox1[pos[1]][pos[0]]
                output += char
            if i % 2 != 0:  # even chars
                pos = self.positions2[c]
                char = self.cipherbox2[pos[1]][pos[0]]
                output += char

        return output

def main():
    # handle cli arguments
    parser = argparse.ArgumentParser(description="Playnasty Cipher")
    parser.add_argument("--text", type=str, help="Text to encode/decode")
    parser.add_argument("--date", type=str, default=datetime.strftime(datetime.now(), "%y%m%d"), help="Date key (YYMMDD)")
    args = parser.parse_args()
    # init cipher object
    cipher = PlaynastyCipher(date=str(args.date))
    # encode/decode text
    text = args.text
    transformed_text = cipher.transform(text)
    # print results
    print(f"Transformed text: {transformed_text}")

if __name__ == "__main__":
    main()