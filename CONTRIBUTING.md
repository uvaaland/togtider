# Contributing to Togtider

Thank you for your interest in contributing to Togtider! This document provides guidelines and instructions for contributing.

## Code of Conduct

By participating in this project, you are expected to uphold a respectful and collaborative environment.

## How to Contribute

### Reporting Bugs

If you find a bug, please create an issue with the following information:

1. A clear, descriptive title
2. Steps to reproduce the issue
3. Expected behavior
4. Actual behavior
5. Screenshots (if applicable)
6. Environment details (OS, Python version, etc.)

### Suggesting Enhancements

We welcome suggestions for enhancements! Please create an issue with:

1. A clear, descriptive title
2. A detailed description of the proposed enhancement
3. Potential implementation approach (if you have ideas)
4. Why this enhancement would be useful

### Pull Requests

1. Fork the repository
2. Create a new branch for your feature or bugfix
3. Make your changes
4. Add or update tests as necessary
5. Run tests to ensure they pass
6. Submit a pull request with a clear description of the changes

## Development Setup

1. Clone the repository:
```bash
git clone https://github.com/uvaaland/togtider.git
cd togtider
```

2. Create a virtual environment:
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

3. Install dependencies:
```bash
pip install -r requirements.txt
```

4. Configure your API credentials:
```bash
cp jattavagen_departures/config.py.example jattavagen_departures/config.py
# Edit config.py with your Bane NOR API key
```

## Running Tests

Run the tests with:
```bash
python -m unittest discover tests
```

## Code Style

- Follow PEP 8 guidelines
- Include docstrings for all functions, classes, and modules
- Use meaningful variable and function names
- Keep functions focused on a single responsibility
- Add appropriate logging

## Commit Messages

- Use clear, descriptive commit messages
- Start with a short summary (50 chars or less)
- Add more detailed explanation if necessary, separated by a blank line

## Adding New Features

If you're adding a new feature:

1. Ensure it's well-documented
2. Add appropriate tests
3. Update the README if necessary
4. Consider backward compatibility

## License

By contributing to Togtider, you agree that your contributions will be licensed under the project's MIT License.
