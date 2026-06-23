"""
Question 3 - Regular Expressions

Write a regular expression to
validate a 10-digit mobile number.
"""

import re


def is_valid_mobile(mobile_number: str) -> bool:
    """
    Return True if the mobil number is valid.
    """

    # ^      -> Start of string
    # \d{10} -> Exactly 10 digits
    # $      -> End of string
    pattern = r"^\d{10}$"

    return bool(re.match(pattern, mobile_number))


if __name__ == "__main__":

    print("\n--- Mobile Validation ---")

    mobile_number = input(
        "Enter mobile number: "
    )

    if is_valid_mobile(mobile_number):
        print("Valid mobile number.")
    else:
        print("Invalid mobile number.")