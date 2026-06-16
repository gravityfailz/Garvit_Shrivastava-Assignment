"""
Question 4
"""


def display_data_types() -> None:
    """Display variable types."""

    integer_value: int = 10
    float_value: float = 15.5
    string_value: str = "Python"
    boolean_value: bool = True

    print(type(integer_value))
    print(type(float_value))
    print(type(string_value))
    print(type(boolean_value))


if __name__ == "__main__":
    display_data_types()