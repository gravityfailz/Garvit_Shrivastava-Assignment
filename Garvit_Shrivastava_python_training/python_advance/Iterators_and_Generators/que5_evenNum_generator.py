
"""
Question 5 - Iterators and Generators

Write a generator expression to generate
even numbers from 1 to 50.
"""


if __name__ == "__main__":

    print("\n--- Even Numbers Generator ---")

    # Generate even numbers from 1 to 50.
    even_numbers = (
        number
        for number in range(1, 51)
        if number % 2 == 0
    )

    for number in even_numbers:
        print(number)
