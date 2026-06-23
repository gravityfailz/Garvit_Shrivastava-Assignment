"""
Assignment 2 - Pandas DataFrame Creation
"""

import pandas as pd

BONUS_RATE = 0.10


# -----------------------------------
# Question 1: Create DataFrame
# -----------------------------------

employee_records = {
    "Name": ["Rahul", "Priya", "Amit", "Anuj"],
    "Age": [25, 30, 28, 35],
    "Department": ["HR", "IT", "Finance", "IT"],
    "Salary": [30000, 50000, 45000, 60000]
}

employees_df = pd.DataFrame(employee_records)

print("Question 1: Employee Data")
print(employees_df)


# -----------------------------------
# Question 2: Display First 2 Rows
# -----------------------------------

print("\nQuestion 2: First Two Records")
print(employees_df.head(2))


# -----------------------------------
# Question 3: Summary Statistics
# -----------------------------------

print("\nQuestion 3: Statistical Summary")
print(employees_df.describe())


# -----------------------------------
# Question 4: Display IT Employees
# -----------------------------------

it_staff = employees_df[
    employees_df["Department"] == "IT"
    ]

print("\nQuestion 4: Employees from IT Department")
print(it_staff)


# -----------------------------------
# Question 5: Add Bonus Column
# -----------------------------------

employees_df["Bonus"] = (
        employees_df["Salary"] * BONUS_RATE
)


print("\nQuestion 5: Data After Adding Bonus")
print(employees_df)