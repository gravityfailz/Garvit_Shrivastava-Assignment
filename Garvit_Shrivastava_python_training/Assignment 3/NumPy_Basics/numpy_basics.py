"""
Assignment 1 - NumPy Fundamentals
"""

import numpy as np


# -----------------------------------
# Question 1: Create a NumPy Array
# -----------------------------------
array_values = [5, 15, 25, 35, 45]

# Convert the list into a NumPy array.
numbers = np.array(array_values)

print("Question 1: NumPy Array")
print(numbers)


# -----------------------------------
# Question 2: Find Mean, Maximum,
# Minimum, and Sum
# -----------------------------------

print("\nQuestion 2: Array Statistics")

# Calculate basic statistics of the array.
print("Average:", np.mean(numbers))
print("Maximum:", np.max(numbers))
print("Minimum:", np.min(numbers))
print("Sum:", np.sum(numbers))


# -----------------------------------
# Question 3: Perform Addition and
# Multiplication on Two Arrays
# -----------------------------------

first_array = np.array([2, 4, 6])
second_array = np.array([1, 3, 5])

print("\nQuestion 3: Array Operations")

# Add corresponding elements of both arrays.
print("Addition:")
print(first_array + second_array)

# Multiply corresponding elements of both arrays.
print("\nMultiplication:")
print(first_array * second_array)


# -----------------------------------
# Question 4: Create a 3x3 Matrix
# -----------------------------------

# Create a matrix with 3 rows and 3 columns.
matrix = np.array([
    [1, 2, 3],
    [4, 5, 6],
    [7, 8, 9]
])

print("\nQuestion 4: 3x3 Matrix")
print(matrix)