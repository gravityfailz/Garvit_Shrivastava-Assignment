"""
Question 2 - Packaging

Explain the difference
between a module and
a package with an example.
"""

# Module:
# A module is an individual Python file that
# contains code such as functions, classes,
# and variables that can be reused in other
# programs.
#
# Example:
# math_operations.py
#
# def square(num):
#     return num ** 2
#
# Package:
# A package is a folder that groups multiple
# related Python modules together. It usually
# contains an __init__.py file to indicate that
# the directory should be treated as a package.
#
# Example Structure:
#
# utilities/
# ├── __init__.py
# ├── math_operations.py
# └── string_operations.py
#
# Key Differences:
#
# 1. A module consists of a single .py file,
#    whereas a package is a directory that
#    contains one or more modules.
#
# 2. Modules help organize code into reusable
#    units, while packages help organize
#    multiple modules in a structured manner.
#
# 3. A package can contain sub-packages and
#    multiple modules, whereas a module cannot
#    contain other modules.
#
# Example:
# 'math_operations.py' is a module because it
# is a single Python file. The 'utilities'
# directory is a package because it contains
# multiple related modules.
#
# Conclusion:
# Modules are used to store reusable code in a
# single file, while packages are used to group
# related modules and maintain a better project
# structure.