"""
Question 8 - Regular Expressions

Create a password validation
program using regex.
"""

import re


def is_valid_password(password: str) -> bool:
    """
    Check whether the password
    meets the required conditions.
    """

    # (?=.*[A-Z])     -> At least one uppercase letter
    # (?=.*\d)        -> At least one digit
    # (?=.*[@#$%&!])  -> At least one special character
    # .{8,}           -> Minimum length of 8 characters
    pattern = (
        r"^(?=.*[A-Z])"
        r"(?=.*\d)"
        r"(?=.*[@#$%&!])"
        r".{8,}$"
    )

    return bool(
        re.match(pattern, password)
    )


if __name__ == "__main__":

    print("\n--- Password Validation ---")

    password = input(
        "Enter password: "
    )

    # Check whether the password is valid.
    if is_valid_password(password):
        print("Valid password.")
    else:
        print(
            "Password must contain at least "
            "8 characters, one uppercase letter, "
            "one digit and one special character."
        )