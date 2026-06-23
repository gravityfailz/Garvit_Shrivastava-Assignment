"""
Assignment 4 - Data Analysis

Tasks:
1. Find average salary by department.
2. Find maximum salary by department.
3. Count employees per department.
"""

import pandas as pd


if __name__ == "__main__":

    employee_records = {
        "Name": ["Rahul", "Priya", "Amit", "Anuj"],
        "Department": ["HR", "IT", "Finance", "IT"],
        "Salary": [30000, 50000, 45000, 60000]
    }

    employees_df = pd.DataFrame(
        employee_records
    )

    print("Employee Information:")
    print(employees_df)

    # Group employees according to
    # their department for analysis.
    department_groups = employees_df.groupby(
        "Department"
    )

    # -----------------------------------
    # Question 1: Average Salary
    # by Department
    # -----------------------------------

    print("\nQuestion 1: Average Salary by Department")

    # mean() calculates the average
    # salary for each department.
    print(
        department_groups["Salary"].mean()
    )

    # -----------------------------------
    # Question 2: Maximum Salary
    # by Department
    # -----------------------------------

    print("\nQuestion 2: Maximum Salary by Department")

    # max() returns the highest salary
    # available in each department.
    print(
        department_groups["Salary"].max()
    )

    # -----------------------------------
    # Question 3: Employee Count
    # by Department
    # -----------------------------------

    print("\nQuestion 3: Employee Count by Department")

    # count() determines the number
    # of employees in each department.
    print(
        department_groups["Name"].count()
    )