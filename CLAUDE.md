# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

This is a Python library called `airtableformulahelpers` that provides utilities for generating Airtable formulas programmatically. It uses a fluent API with typed field classes to build complex Airtable formulas.

## Development Commands

### Testing
```bash
# Run all tests
pytest

# Run tests with coverage
pytest --cov=airtableformulahelpers

# Run specific test file
pytest tests/test_main.py

# Run tests in specific test class
pytest tests/test_main.py::TestLogicFunctions
```

### Code Quality
```bash
# Format code
ruff format

# Run linting
ruff check

# Run linting with auto-fix
ruff check --fix
```

### Running the CLI
```bash
# Run the example CLI
python cli.py
```

### Package Management
This project uses `uv` for dependency management with virtual environments managed through `ty`.

## Architecture

### Core Components

1. **Field Classes** (`src/airtableformulahelpers/__init__.py`):
   - `Field`: Base class for all field types
   - `TextField`: String field operations (equals, contains, starts_with, ends_with, regex_match)
   - `NumberField`: Numeric comparisons (equals, greater_than, less_than, etc.)
   - `BooleanField`: Boolean operations (is_true, is_false, equals)
   - `DateField`: Date/time comparisons with relative time support
   - `AttachmentsField`: Attachment field operations
   - `TextListField`: Operations on text lists

2. **Logic Functions**:
   - `AND()`, `OR()`, `XOR()`, `NOT()`: Logical operators
   - `IF()`: Conditional logic with fluent THEN/ELSE API

3. **Fluent API Pattern**:
   - `IF(condition).THEN(value).ELSE(value)` creates conditional formulas
   - Field methods return strings that can be combined with logic functions

### Key Design Patterns

- **Fluent Interface**: The IF/THEN/ELSE pattern uses method chaining for readable conditional logic
- **Type Safety**: Field classes provide type-specific methods preventing invalid operations
- **String Templates**: All methods generate Airtable formula strings with proper escaping and formatting
- **Case Sensitivity Options**: Text operations support case-sensitive/insensitive modes
- **Trim Options**: String operations can optionally trim whitespace

### String Handling

The library handles complex string operations with options for:
- Case sensitivity (`case_sensitive=True/False`)
- Trimming (`trim=True/False`, with `no_trim=True` for inverted logic)
- Proper escaping of quotes and special characters in generated formulas

### Date Handling

Uses `dateparser` library for flexible date parsing, supporting both datetime objects and string dates. Provides relative time comparisons (days_ago, hours_ago, etc.).

## Testing

The project has comprehensive test coverage using pytest. Tests are organized by feature classes and cover:
- All field type operations
- Logic function combinations
- Edge cases and error conditions
- String escaping and formatting
- Date parsing and comparisons