# Data Processor Task

A Python utility created as part of the Core Python Training Assignment.

## Features

- Member data management using lists and dictionaries
- Data cleaning using string operations
- Email and phone validation using Regular Expressions
- Object-Oriented Member class
- Custom exception handling
- Lambda functions with filter()
- map() for data transformation
- Python package structure
- Wheel package distribution

## Project Structure

data_processor_task/
├── my_processor/
│   ├── __init__.py
│   ├── core.py
│   └── utils.py
├── setup.py
└── README.md

## Usage

```python
from my_processor.core import Member

member = Member(
    "Garvit Shrivastava",
    "g.s@mail.com",
    "9876543210"
)

print(member)


##Build Package
python setup.py sdist bdist_wheel