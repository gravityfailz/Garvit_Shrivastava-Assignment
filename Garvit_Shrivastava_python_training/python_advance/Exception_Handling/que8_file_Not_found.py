
"""
Question 8 - Exception Handling
Handle FileNotFoundError when trying
to open a file.
"""


def read_file(file_name: str) -> str:
    """
    Open a file and return its contents.
    """

    try:
        # Open the file and read its contents.
        with open(
                file_name,
                "r",
                encoding="utf-8"
        ) as file:

            content = file.read()

        return content

    except FileNotFoundError:
        return "File not found."


if __name__ == "__main__":

    print("\n--- File Reader ---")

    file_name = input(
        "Enter file name: "
    )

    print(
        read_file(file_name)
    )

