"""
Question 7 - Regular Expressions

Write a pattern to check
if a string contains only
alphabets.
"""

import re


def contains_only_alphabets(text: str) -> bool:
    """
    Return True if the string
    contains only alphabets.
    """

    # ^      -> Start of string
    # [A-Za-z]+ -> One or more alphabets
    # $      -> End of string
    pattern = r"^[A-Za-z]+$"

    return bool(re.match(pattern, text))


if __name__ == "__main__":

    print("\n--- Alphabet Validation ---")

    text = input("Enter text: ")

    if contains_only_alphabets(text):
        print("The string contains only alphabets.")
    else:
        print("The string contains non-alphabet characters.")