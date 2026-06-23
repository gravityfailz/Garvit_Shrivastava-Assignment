
"""
Question 3 - Exception Handling

Write a program using try-except-else-finally
to read a number from a file and print its square.
"""


def calculate_square(number):
    """
    Return the square of a number.
    """

    return number ** 2


if __name__ == "__main__":

    print("\n--- File Square Calculator ---")

    file_name = input(
        "Enter file name: "
    )

    file = None

    try:
        # Open the file and read the number from it.
        file = open(
            file_name,
            "r",
            encoding="utf-8"
        )

        number = float(
            file.read().strip()
        )

    except FileNotFoundError:
        print("File not found.")

    except ValueError:
        print(
            "The file does not contain "
            "a valid number."
        )

    else:
        # Find the square of the number.
        square = calculate_square(number)

        print(
            f"Square of {number} is {square}."
        )

    finally:
        # Close the file before the program ends.
        if file is not None:
            file.close()

