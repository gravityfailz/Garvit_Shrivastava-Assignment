"""
Assignment 5 - Matplotlib Charts

Tasks:
1. Create a Bar Chart.
2. Create a Line Chart.
3. Create a Histogram.
4. Create a Scatter Plot.
"""

import matplotlib.pyplot as plt

DEPARTMENTS = ["HR", "IT", "Finance"]
EMPLOYEE_COUNT = [5, 12, 7]

SALARIES = [30000, 40000, 50000, 60000, 45000]
AGES = [25, 30, 28, 35, 29]


def show_all_charts() -> None:
    """
    Display all required
    matplotlib charts.
    """

    # Question 1: Bar Chart

    # Figure size keeps the chart
    # readable across screen sizes.
    plt.figure(figsize=(6, 4))

    # Bar charts compare values
    # across categories.
    plt.bar(DEPARTMENTS, EMPLOYEE_COUNT)

    plt.title("Employees by Department")
    plt.xlabel("Department")
    plt.ylabel("Employees")

    # Grid improves readability
    # when comparing values.
    plt.grid(True, axis="y")

    # Tight layout prevents labels
    # and titles from overlapping.
    plt.tight_layout()
    plt.show()

    # Question 2: Line Chart

    # Line charts help visualize
    # changes between data points.
    plt.figure(figsize=(6, 4))

    plt.plot(DEPARTMENTS, EMPLOYEE_COUNT, marker="o", linewidth=2)

    plt.title("Employee Count by Department")
    plt.xlabel("Department")
    plt.ylabel("Employees")

    plt.grid(True)
    plt.tight_layout()
    plt.show()

    # Question 3: Histogram

    # Histograms show how
    # values are distributed.
    plt.figure(figsize=(6, 4))

    plt.hist(SALARIES, bins=3, edgecolor="black")

    plt.title("Salary Distribution")
    plt.xlabel("Salary")
    plt.ylabel("Frequency")

    plt.tight_layout()
    plt.show()

    # Question 4: Scatter Plot

    # Scatter plots help identify
    # relationships between variables.
    plt.figure(figsize=(6, 4))

    plt.scatter(AGES, SALARIES)

    plt.title("Age vs Salary")
    plt.xlabel("Age")
    plt.ylabel("Salary")

    plt.tight_layout()
    plt.show()


if __name__ == "__main__":

    show_all_charts()