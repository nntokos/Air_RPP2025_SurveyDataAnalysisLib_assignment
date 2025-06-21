# Air_RPP2025_SurveyDataAnalysisLib

A Python library for loading, analyzing, and querying survey data, designed for the Air_RPP2025 project. This package provides tools to efficiently process survey data from Excel files and perform common analysis tasks.

## Table of Contents
- [Features](#features)
- [Requirements](#requirements)
- [Installation](#installation)
- [Usage](#usage)
- [Command Line Interface](#command-line-interface)
- [Running Tests](#running-tests)
- [Project Structure](#project-structure)
- [License](#license)

## Features
- Load survey data from Excel files
- Perform common queries and analyses
- Command-line interface for quick access
- Easily extensible for new analysis tasks

## Requirements
- Python 3.8+
- See `requirements.txt` for dependencies

## Installation

1. **Clone the repository:**
   ```bash
   git clone <repository-url>
   cd Air_RPP2025_SurveyDataAnalysisLib_assignment
   ```

2. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

3. **(Optional) Install the package locally:**
   ```bash
   pip install -e .
   ```

## Usage

### As a Library
Import and use the main modules in your Python code:

```python
from so_surveyanalysis import loader, queries

data = loader.load_excel('data/so_2024_raw.xlsx')
result = queries.some_query_function(data)
print(result)
```

Refer to the docstrings in `loader.py` and `queries.py` for available functions and usage examples.

### Command Line Interface

You can use the CLI to run common analysis tasks:

```bash
python -m so_surveyanalysis.cli --help
```

This will display available commands and options.

#### Entry Point Usage

If you installed the package with `pip install -e .` or `pip install .`, you can use the provided entry point directly from the command line:

```bash
so-surveyanalysis --help
```

This command is equivalent to running the CLI module and will show all available options and commands.

## Running Tests

Tests are located in the `tests/` directory and use `pytest`.

1. **Install test dependencies (if not already):**
   ```bash
   pip install -r requirements.txt
   pip install pytest
   ```

2. **Run all tests:**
   ```bash
   pytest
   ```

## Project Structure

```
Air_RPP2025_SurveyDataAnalysisLib_assignment/
├── data/                  # Survey data files (e.g., Excel)
├── so_surveyanalysis/     # Main library code
│   ├── __init__.py
│   ├── loader.py          # Data loading utilities
│   ├── queries.py         # Analysis and query functions
│   └── cli.py             # Command-line interface
├── tests/                 # Unit tests
│   ├── test_loader.py
│   └── test_queries.py
├── requirements.txt       # Python dependencies
├── setup.py               # Package setup
└── README.md              # Project documentation
```

## License

This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for details.
