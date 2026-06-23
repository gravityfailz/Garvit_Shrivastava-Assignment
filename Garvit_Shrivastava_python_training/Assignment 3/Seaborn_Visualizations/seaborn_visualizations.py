"""
Assignment 6 - Seaborn Visualizations

Tasks:
1. Create a Barplot.
2. Create a Boxplot.
3. Create a Heatmap.
"""

import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt

EMPLOYEE_DATA = {
    "Name": ["Rahul", "Priya", "Amit", "Anuj"],
    "Age": [25, 30, 28, 35],
    "Department": ["HR", "IT", "Finance", "IT"],
    "Salary": [30000, 50000, 45000, 60000]
}


def show_all_visualizations() -> None:
    """
    Display all required
    seaborn visualizations.
    """

    employee_dataframe = pd.DataFrame(EMPLOYEE_DATA)

    # Question 1: Barplot

    # Barplots compare values
    # across different categories.
    plt.figure(figsize=(6, 4))
    sns.barplot(data=employee_dataframe, x="Department", y="Salary")

    plt.title("Department vs Salary")
    plt.tight_layout()
    plt.show()

    # Question 2: Boxplot

    # Boxplots show data distribution,
    # median, and potential outliers.
    plt.figure(figsize=(6, 4))
    sns.boxplot(data=employee_dataframe, y="Salary")

    plt.title("Salary Distribution")
    plt.tight_layout()
    plt.show()

    # Question 3: Heatmap

    # Heatmaps visualize correlations
    # between numeric columns.
    plt.figure(figsize=(6, 4))

    # Calculate correlation
    # between Age and Salary.
    correlation_matrix = employee_dataframe[["Age", "Salary"]].corr()

    sns.heatmap(correlation_matrix, annot=True)

    plt.title("Age and Salary Correlation")
    plt.tight_layout()
    plt.show()


if __name__ == "__main__":
    show_all_visualizations()