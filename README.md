## Advanced Calculator Application

### Project Description

This project is an advanced calculator application built using Python. It supports a wide range of arithmetic operations and leverages several software design patterns to ensure scalability, maintainability, and reliability. The calculator includes features such as undo/redo, logging, history management, and automatic data persistence, with comprehensive unit tests and a GitHub Actions CI/CD pipeline for continuous integration.

Key design patterns implemented:

Factory Pattern — for creating different operation instances dynamically.

Memento Pattern — for implementing undo and redo functionality.

Observer Pattern — for logging calculations and auto-saving history automatically.

After creating the environment we install the dependencies in requirements.txt which contains below

python-dotenv==1.0.1
pandas==2.2.3
pytest==8.3.3
pytest-cov==5.0.0


### Configuration Setup
The calculator relies on environment variables defined in a .env file to manage configurations such as log directories, history persistence, and precision.

Create a .env file in the project root:
CALCULATOR_LOG_DIR=logs
CALCULATOR_HISTORY_DIR=history
CALCULATOR_MAX_HISTORY_SIZE=1000
CALCULATOR_AUTO_SAVE=true
CALCULATOR_PRECISION=6
CALCULATOR_MAX_INPUT_VALUE=1000000000
CALCULATOR_DEFAULT_ENCODING=utf-8


### Usage Guide

### Run the calculator application in interactive mode (REPL):

| Command          | Description                                      |
| ---------------- | ------------------------------------------------ |
| `add a b`        | Adds two numbers                                 |
| `subtract a b`   | Subtracts b from a                               |
| `multiply a b`   | Multiplies two numbers                           |
| `divide a b`     | Divides a by b (handles divide by zero)          |
| `power a b`      | Raises a to the power of b                       |
| `root a b`       | Calculates the b-th root of a                    |
| `modulus a b`    | Returns a % b                                    |
| `int_divide a b` | Performs integer division                        |
| `percent a b`    | Computes (a / b) * 100                           |
| `abs_diff a b`   | Computes the absolute difference between a and b |
| `history`        | Displays past calculations                       |
| `undo` / `redo`  | Undo or redo the last calculation                |
| `save`           | Manually saves the calculation history           |
| `load`           | Loads the calculation history from a CSV file    |
| `clear`          | Clears history                                   |
| `help`           | Lists available commands                         |
| `exit`           | Exits the calculator gracefully                  |

All calculations are logged to a file and auto-saved to a CSV if enabled.

### Error Handling and Logging

Invalid input values or operations raise custom exceptions (ValidationError, OperationError).

All important events and calculation results are logged to the file specified in .env.

Logs include timestamps, operation names, operands, and results for audit and debugging purposes.

Example log snippet:
INFO 2025-10-30 14:32:10 - add(5.0, 2.0) = 7.0
INFO 2025-10-30 14:32:12 - divide(10.0, 2.0) = 5.0

### CI/CD Integration (GitHub Actions)

The project uses GitHub Actions for continuous integration. Every push and pull request to the main branch triggers automated testing and coverage checks.

Workflow file: .github/workflows/python-app.yml

Key steps:

Check out the repository.

Set up Python 3.11/3.12.

Install dependencies.

Run tests with pytest and enforce 90% coverage.

Upload coverage reports as artifacts.