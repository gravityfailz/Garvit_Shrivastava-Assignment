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


"""
Question 42
"""


class Person:
    """Parent class."""

    def __init__(
        self,
        name: str
    ) -> None:
        self.name = name


class Employee(Person):
    """Child class."""

    def __init__(
        self,
        name: str,
        salary: float
    ) -> None:
        super().__init__(name)
        self.salary = salary

    def display_employee(
        self
    ) -> None:
        """Display employee."""

        print(
            self.name,
            self.salary
        )


employee = Employee(
    "Garvit",
    50000
)

employee.display_employee()


"""
Question 43
"""


class Bank:
    """Bank class."""

    def __init__(
        self,
        balance: float
    ) -> None:
        self.__balance = balance

    def deposit(
        self,
        amount: float
    ) -> None:
        self.__balance += amount

    def get_balance(
        self
    ) -> float:
        return self.__balance


account = Bank(1000)

account.deposit(500)

print(
    account.get_balance()
)

"""
Question 44
"""


class Dog:
    """Dog class."""

    def speak(self) -> None:
        print("Bark")


class Cat:
    """Cat class."""

    def speak(self) -> None:
        print("Meow")


def animal_sound(
    animal
) -> None:
    """Polymorphism example."""

    animal.speak()


dog = Dog()
cat = Cat()

animal_sound(dog)
animal_sound(cat)