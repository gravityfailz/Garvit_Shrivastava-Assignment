"""
Question 40
"""


class Student:
    """Student class."""

    def __init__(
        self,
        student_id: int,
        student_name: str
    ) -> None:
        self.student_id = student_id
        self.student_name = student_name

    def display_details(
        self
    ) -> None:
        """Display details."""

        print(
            self.student_id,
            self.student_name
        )


student = Student(
    101,
    "Garvit"
)

student.display_details()

"""
Question 41
"""


class Car:
    """Car class."""

    def __init__(
        self,
        brand: str,
        model: str
    ) -> None:
        self.brand = brand
        self.model = model

    def display_car(self) -> None:
        """Display car details."""

        print(
            self.brand,
            self.model
        )


car = Car(
    "Toyota",
    "Innova"
)

car.display_car()