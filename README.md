# Stack Overflow Survey Data Analysis Library

A comprehensive Python library for analyzing Stack Overflow survey data. This library provides tools for loading, parsing, and analyzing survey data from XLSX files, with support for both single-choice and multiple-choice questions.

## Features

- **Data Loading**: Load survey data from XLSX files with automatic question type detection
- **Question Classification**: Automatically classify questions as Single Choice (SC) or Multiple Choice (MC)
- **Search Functionality**: Search for specific questions or answer options
- **Data Analysis**: Generate answer distributions with statistics and percentages
- **Respondent Filtering**: Create subsets of respondents based on specific criteria
- **Command Line Interface**: Full CLI support for quick data exploration
- **Programmatic API**: Use as a Python library in your own applications

## Installation

### Prerequisites

- Python 3.6 or higher
- pip package manager

### Option 1: Install in Development Mode (Recommended)

1. Clone or download the repository
2. Navigate to the project directory:
```bash
cd Air_RPP2025_SurveryDataAnalysisLib_assignment
```

3. Create a virtual environment (recommended):
```bash
python -m venv .venv
source .venv/bin/activate  # On Windows: .venv\Scripts\activate
```

4. Install the package in development mode:
```bash
pip install -e .
```

### Option 2: Install Dependencies Only

If you prefer to run the library without installing it as a package:

```bash
pip install -r requirements.txt
```

## Quick Start

### Using the Command Line Interface

The library includes a command-line tool `so_surveyanalysis` for quick data exploration:

```bash
# Display survey structure (list all questions)
so_surveyanalysis data/so_2024_raw.xlsx --structure

# Search for questions or options containing "Python"
so_surveyanalysis data/so_2024_raw.xlsx --search "Python"

# Show answer distribution for a specific question
so_surveyanalysis data/so_2024_raw.xlsx --distribution "MainBranch"

# Create a respondent subset based on a question and option
so_surveyanalysis data/so_2024_raw.xlsx --subset "Country" "United States of America"
```

### Using the Python API

```python
from so_surveyanalysis import SurveyDataLoader, SurveyAnalyzer

# Load survey data
loader = SurveyDataLoader("data/so_2024_raw.xlsx")

# Get basic information
print(f"Total respondents: {len(loader.get_data())}")
print(f"Total questions: {len(loader.get_questions())}")

# Create analyzer
analyzer = SurveyAnalyzer(loader)

# Get answer distribution for a question
distribution = analyzer.get_answer_distribution("MainBranch")
print(f"Distribution: {distribution}")

# Search for questions
python_questions = loader.search_questions("Python")
print(f"Questions containing 'Python': {python_questions}")

# Get question options
options = loader.get_question_options("EdLevel")
print(f"Education level options: {options}")
```

## Detailed Usage

### SurveyDataLoader Class

The `SurveyDataLoader` class handles loading and parsing survey data:

```python
from so_surveyanalysis.loader import SurveyDataLoader

# Initialize loader
loader = SurveyDataLoader("path/to/survey.xlsx")

# Basic data access
data = loader.get_data()  # Returns pandas DataFrame
questions = loader.get_questions()  # Returns list of question names
question_type = loader.get_question_type("QuestionName")  # Returns "SC" or "MC"

# Search functionality
matching_questions = loader.search_questions("search_term")
matching_options = loader.search_options("search_term")

# Get unique options for a question
options = loader.get_question_options("QuestionName")

# Create respondent subset
subset = loader.get_respondent_subset("BaseQuestion", "SelectedOption")
```

### SurveyAnalyzer Class

The `SurveyAnalyzer` class provides analytical capabilities:

```python
from so_surveyanalysis.queries import SurveyAnalyzer

# Initialize analyzer (requires a loader)
analyzer = SurveyAnalyzer(loader)

# Get answer distribution
distribution = analyzer.get_answer_distribution("QuestionName")
# Returns: {
#   'total_respondents': int,
#   'valid_responses': int,
#   'missing_responses': int,
#   'distribution': {
#       'answer1': {'count': int, 'percentage': float},
#       'answer2': {'count': int, 'percentage': float},
#       ...
#   }
# }

# Get top N most common answers
top_answers = analyzer.get_answer_distribution("QuestionName", top_n=10)

# Cross-tabulation analysis
crosstab = analyzer.cross_tabulate("Question1", "Question2")

# Comparative analysis between groups
comparison = analyzer.compare_groups("BaseQuestion", "BaseOption", "TargetQuestion")
```

### Question Types

The library automatically detects two types of questions:

1. **Single Choice (SC)**: Questions where respondents select one option
2. **Multiple Choice (MC)**: Questions where respondents can select multiple options (identified by semicolon-separated values)

## Command Line Interface Reference

```bash
so_surveyanalysis <file_path> [options]

Arguments:
  file_path           Path to the survey data XLSX file

Options:
  --structure         Display the survey structure (list of questions)
  --search TERM       Search for questions or options containing TERM
  --subset Q OPTION   Create subset of respondents who selected OPTION for question Q
  --distribution Q    Display answer distribution for question Q
  -h, --help         Show help message
```

### CLI Examples

```bash
# Basic exploration
so_surveyanalysis data/so_2024_raw.xlsx --structure

# Search for technology-related questions
so_surveyanalysis data/so_2024_raw.xlsx --search "technology"

# Analyze programming language preferences
so_surveyanalysis data/so_2024_raw.xlsx --distribution "LanguageHaveWorkedWith"

# Create subset of US respondents and analyze their responses
so_surveyanalysis data/so_2024_raw.xlsx --subset "Country" "United States of America"
```

## Running Tests

The project includes comprehensive test coverage using pytest.

### Run All Tests

```bash
# From the project root directory
python -m pytest

# With verbose output
python -m pytest -v

# Run specific test file
python -m pytest tests/test_loader.py
python -m pytest tests/test_queries.py
```

### Test Coverage

The test suite covers:

- **Data Loading**: Testing XLSX file loading and parsing
- **Question Classification**: Verifying SC/MC question detection
- **Search Functionality**: Testing question and option search
- **Data Analysis**: Verifying distribution calculations and statistics
- **Error Handling**: Testing invalid inputs and edge cases


## Project Structure

```
Air_RPP2025_SurveryDataAnalysisLib_assignment/
├── so_surveyanalysis/           # Main library package
│   ├── __init__.py             # Package initialization
│   ├── loader.py               # SurveyDataLoader class
│   ├── queries.py              # SurveyAnalyzer class
│   └── cli.py                  # Command-line interface
├── tests/                      # Test suite
│   ├── __init__.py
│   ├── test_loader.py          # Tests for loader module
│   └── test_queries.py         # Tests for queries module
├── data/                       # Survey data files
│   └── so_2024_raw.xlsx       # Stack Overflow 2024 survey data
├── requirements.txt            # Project dependencies
├── setup.py                   # Package setup configuration
├── README.md                  # This file
└── .venv/                     # Virtual environment (created after setup)
```

## Dependencies

The library requires the following Python packages:

- **pandas**: Data manipulation and analysis
- **openpyxl**: Excel file reading/writing
- **argparse**: Command-line argument parsing
- **pytest**: Testing framework
- **tabulate**: Pretty table formatting for CLI output

## Data Format Requirements

The library expects survey data in XLSX format with the following characteristics:

- **First row**: Column headers (question names)
- **Subsequent rows**: Survey responses
- **Multiple choice questions**: Responses separated by semicolons (`;`)
- **Missing values**: Empty cells or NaN values are handled automatically

## Author

**Nikolaos Ntokos**
- Email: ndokos@hotmail.com
- GitHub: https://github.com/nntokos/so_surveyanalysis