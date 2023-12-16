# Interpreter (sort of)

## Overview

This repository contains the "Challenge Project: Interpreter," a programming project that enhances a basic parser into a full-fledged interpreter capable of executing programs. The project is an advanced extension of a school assignment and utilizes a top-down predictive approach. It's designed to interpret and execute specific code segments while returning values for further use in the program.

## Features

The interpreter supports the following features:
- `input` and `print` statements for interactive user input and output.
- Variable assignments using a symbol table for dynamic value management.
- Arithmetic expression evaluation for basic mathematical computations.
- Implementation of `if` statements for conditional execution.
- Handling of `while`, `do while`, and `for` loops for iterative execution.

## Project Structure

- `interpreter.py`: The main file containing the interpreter logic.
- `lexer.py`: Lexer module used for tokenizing the input program.
- `test_programs`: Directory containing sample programs to test the interpreter's functionality.

### Core Functions

- `input_statement`: Handles input.
- `block`: Processes statement blocks.
- `atom`: Evaluates single values in expressions.
- `expression`, `term`, `factor`: Evaluate expressions.
- Conditional (`if`) and loop (`while`, `do while`, `for`) structures implementation.

## Getting Started

### Prerequisites

- A Python environment.

### Installation

- Clone the repository to your local machine.

### Usage

1. Navigate to the project directory in your command line interface.
2. Execute the interpreter with one of the example file as an argument, e.g., `python interpreter.py <program_name>`.
3. The program will display the output for the given test file in the terminal.

## Contributing

This project was developed as an extension of a class assignment, and while it is primarily for educational purposes, contributions or suggestions for improvements are welcome. To contribute:
1. Fork the repository.
2. Create a new branch (`git checkout -b feature/AmazingFeature`).
3. Commit your changes (`git commit -m 'Add some AmazingFeature'`).
4. Push to the branch (`git push origin feature/AmazingFeature`).
5. Open a pull request.

## Contact
Matheus K. Westphalen - mkwestphalen@gmail.com

Project Link: [https://github.com/mwestphalen/interpreter](https://github.com/mwestphalen/interpreter)
  
