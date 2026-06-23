"""
Question 5 - Regular Expressions

Use re.findall() to extract
all words starting with a
capital letter.
"""

import re


def extract_capital_words(text: str) -> list[str]:
    """
    Return words starting
    with a capital letter.
    """

    # re.findall() returns all
    # matching words as a list.

    # \b      -> Word boundary
    # [A-Z]   -> First uppercase letter
    # [a-z]*  -> Remaining lowercase letters
    pattern = r"\b[A-Z][a-z]*\b"

    return re.findall(pattern, text)


if __name__ == "__main__":

    print("\n--- Capital Words ---")

    text = (
        "The NucleusTeq is One of the Best "
        "Company in the World."
    )

    # Display all matching words.
    capital_words = extract_capital_words(text)

    # Display all matching words.
    if capital_words:
        print(capital_words)
    else:
        print("No capitalized words found.")