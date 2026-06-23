"""
Question 1 - Regular Expressions

Write a program to extract all numbers
from a given string using regular expressions.
"""

import re


def extract_numbers(text: str) -> list[str]:
    """
    Return all numbers
    found in a string.
    """

    # findall() returns all values
    # \d+ matches one or more digits.
    return re.findall(r"\d+", text)


if __name__ == "__main__":

    print("\n--- Extract Numbers ---")

    text = "Mahak scored 85 marks in 2024 and 92 marks in 2025."

    # Display all numbers found in the string.
    print(extract_numbers(text))