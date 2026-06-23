"""
Assignment 7: Student Performance Analysis

Tasks:
1. Load data into Pandas.
2. Add Performance column.
3. Create Line Chart.
4. Create Scatter Plot.
5. Create Seaborn Bar plot.
"""

import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns


PASS_MARKS: int = 65


def create_student_dataframe() -> pd.DataFrame:
    """
    Create student DataFrame.
    """

    student_data = {
        "Name": [
            "Rahul",
            "Priya",
            "Siri",
            "Anuj"
        ],
        "Marks": [
            70,
            80,
            90,
            60
        ],
        "Hours Studied": [
            2,
            3,
            5,
            1
        ]
    }

    return pd.DataFrame(
        student_data
    )


def add_performance_column(
        student_dataframe: pd.DataFrame
) -> None:
    """
    Add Pass/Fail column.
    """

    student_dataframe["Performance"] = (
        student_dataframe["Marks"]
        .apply(
            lambda marks:
            "Pass"
            if marks > PASS_MARKS
            else "Fail"
        )
    )


def create_line_chart(
        student_dataframe: pd.DataFrame
) -> None:
    """
    Create Hours vs Marks line chart.
    """

    plt.figure(
        figsize=(6, 4)
    )

    plt.plot(
        student_dataframe["Hours Studied"],
        student_dataframe["Marks"],
        marker="o"
    )

    plt.title(
        "Hours Studied vs Marks"
    )

    plt.xlabel(
        "Hours Studied"
    )

    plt.ylabel(
        "Marks"
    )

    plt.show()


def create_scatter_plot(
        student_dataframe: pd.DataFrame
) -> None:
    """
    Create scatter plot.
    """

    plt.figure(
        figsize=(6, 4)
    )

    plt.scatter(
        student_dataframe["Hours Studied"],
        student_dataframe["Marks"]
    )

    plt.title(
        "Study Hours vs Marks"
    )

    plt.xlabel(
        "Hours Studied"
    )

    plt.ylabel(
        "Marks"
    )

    plt.show()


def create_performance_barplot(
        student_dataframe: pd.DataFrame
) -> None:
    """
    Create performance barplot.
    """

    plt.figure(
        figsize=(6, 4)
    )

    sns.barplot(
        data=student_dataframe,
        x="Performance",
        y="Marks"
    )

    plt.title(
        "Performance vs Marks"
    )

    plt.show()


def main() -> None:
    """
    Execute project workflow.
    """

    student_dataframe = (
        create_student_dataframe()
    )

    add_performance_column(
        student_dataframe
    )

    print(
        "Student Data:"
    )

    print(student_dataframe)

    create_line_chart(
        student_dataframe
    )

    create_scatter_plot(
        student_dataframe
    )

    create_performance_barplot(
        student_dataframe
    )


if __name__ == "__main__":
    main()