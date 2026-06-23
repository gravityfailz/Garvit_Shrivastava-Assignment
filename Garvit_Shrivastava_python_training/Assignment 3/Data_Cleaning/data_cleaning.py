"""
Assignment 3 - Data Cleaning

Tasks:
1. Detect missing values.
2. Replace missing Age with mean.
3. Replace missing Salary with 0.
"""

import pandas as pd

DEFAULT_SALARY = 0


if __name__ == "__main__":

    employee_data = {
        "Name": ["Rahul", "Priya", "Anuj"],
        "Age": [25, None, 29],
        "Salary": [30000, 40000, None]
    }

    employee_dataframe = pd.DataFrame(
        employee_data
    )

    # -----------------------------------
    # Question 1: Check for missing data
    # -----------------------------------

    print("Question 1: Original DataFrame")
    print(employee_dataframe)

    print("\nMissing Values:")

    # Shows which cells have missing values.
    print(employee_dataframe.isnull())

    # -----------------------------------
    # Question 2: Fill missing Age values
    # with the average age
    # -----------------------------------

    # Calculate the average age
    # from the available records.
    average_age = employee_dataframe[
        "Age"
    ].mean()

    # Replace empty age values
    # with the calculated average.
    employee_dataframe["Age"] = (
        employee_dataframe["Age"].fillna(
            average_age
        )
    )

    # -----------------------------------
    # Question 3: Fill missing Salary
    # values with 0
    # -----------------------------------

    # Replace missing salary entries
    # with the default value.
    employee_dataframe["Salary"] = (
        employee_dataframe["Salary"].fillna(
            DEFAULT_SALARY
        )
    )

    print("\nQuestion 3: Cleaned DataFrame")
    print(employee_dataframe)