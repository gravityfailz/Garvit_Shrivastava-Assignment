"""
Question 2 - Regular Expressions

Write a regex pattern to
validate an email address.
"""

import re


def is_valid_email(email: str) -> bool:
    """
    Return True if the email format is valid otherwise false.
    """

    # ^           -> Start of string
    # [\w.-]+     -> Username part
    # @           -> Mandatory @ symbol
    # [\w.-]+     -> Domain name
    # \.          -> Dot before extension
    # \w+         -> Domain extension
    # $           -> End of string
    pattern = r"^[\w.-]+@[\w.-]+\.\w+$"

    return bool(re.match(pattern, email))


if __name__ == "__main__":

    print("\n--- Email Validation ---")

    email = input("Enter email: ")

    if is_valid_email(email):
        print("Valid email address.")
    else:
        print("Invalid email address.")