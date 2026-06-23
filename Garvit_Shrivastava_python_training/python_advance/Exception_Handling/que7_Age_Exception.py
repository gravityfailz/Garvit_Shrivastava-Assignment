"""
Question 7 - Exception Handling

Create a custom exception called AgeException
and raise it if age is less than 18.
"""

# Custom exception used to represent
# age-specific validation errors.
class AgeException(Exception):
    """
    Custom exception raised when
    age is less than 18.
    """


def validate_age(age: int) -> int:
    """
    Validate that the provided age
    is at least 18.
    """

    # Users below 18 are not allowed.
    if age < 18:
        raise AgeException(
            "Age must be 18 or above."
        )

    return age


if __name__ == "__main__":

    print("\n--- Age Validation ---")

    try:
        age = int(input("Enter age: "))

        print(
            f"Valid Age: "
            f"{validate_age(age)}"
        )

    except AgeException as error:
        print(f"Error: {error}")

    except ValueError:
        print(
            "Invalid input. "
            "Please enter a valid age."
        )