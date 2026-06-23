"""
Question 6 - Regular Expressions

Replace multiple spaces in a
string with a single space
using re.sub().
"""

import re


def replace_multiple_spaces(text: str) -> str:
    """
    Replace multiple spaces
    with a single space.
    """
    # re.sub() replaces all matches.
    # \s+ matches one or more
    # consecutive whitespace characters.
    return re.sub(r"\s+", " ", text)


if __name__ == "__main__":

    print("\n--- Replace Multiple Spaces ---")

    text = "NucleusTeq     is     a     Leading    Product    based   Company"

    modified_text = replace_multiple_spaces(text)

    # Display the modified string.
    print(modified_text)