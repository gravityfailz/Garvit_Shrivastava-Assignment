"""
Question 6
Create a function that raises a ValueError
if a number is negative.
"""


def validate_number(number: float) -> float:
    """
    Validate that the provided
    number is non-negative.
    """

    # Negative values are not allowed
    # for the respective validation rule.
    if number < 0:
        raise ValueError(
            "Negative numbers are not allowed here."
        )

    return number


if __name__ == "__main__":

    print("\n--- Negative Number Validation ---")

    try:
        number = float(
            input("Enter a number: ")
        )

        print(
            f"Valid Number: "
            f"{validate_number(number)}"
        )

    except ValueError as error:
        print(f"Error: {error}")