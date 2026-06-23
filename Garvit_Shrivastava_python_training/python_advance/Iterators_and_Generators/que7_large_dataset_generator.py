"""
Question 7

Write a program that processes a
large dataset using a generator
instead of storing all values in a list.
"""


def generate_numbers(limit: int):
    """
    Generate numbers one at a time.
    """

    for number in range(1, limit + 1):

        # Return one number at a time.
        yield number


if __name__ == "__main__":

    print(
        "\n--- Large Dataset Processing ---"
    )

    limit = int(
        input("Enter dataset size: ")
    )

    processed_records = 0

    # Process each number as it is generated.
    for number in generate_numbers(limit):
        processed_records += 1

    print(
        f"Processed {processed_records:,} records."
    )

