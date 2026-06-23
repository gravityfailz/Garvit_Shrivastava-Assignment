
"""
Question 2
Write a program to divide two numbers entered by
the user and handle ZeroDivisionError.
"""


def divide_numbers(first_number, second_number):
    """
    Divide two numbers and return the result.
    """

    return first_number / second_number


if __name__ == "__main__":

    print("\n--- Division Exception Handling ---")

    try:
        # Read both numbers from the user.
        first_number = float(
            input("Enter first number: ")
        )

        second_number = float(
            input("Enter second number: ")
        )

        result = divide_numbers(
            first_number,
            second_number
        )

        print(
            f"Division Result: {result}"
        )

    except ZeroDivisionError:
        # This exception occurs when
        # the divisor is zero.
        print(
            "Division by zero is not allowed."
        )

    except ValueError:
        # This exception occurs when
        # the input is not numeric.
        print(
            "Invalid input. "
            "Please enter numeric values only."
        )
