# Contributing to Mektabati

Thank you for your interest in contributing to Mektabati! This document provides guidelines for contributing to the project.

## Getting Started

1. Fork the repository
2. Clone your fork locally
3. Create a virtual environment
4. Install dependencies: `pip install -r requirements.txt`
5. Create a new branch for your feature: `git checkout -b feature/your-feature-name`

## Development Setup

```bash
# Clone the repository
git clone https://github.com/yourusername/mektabati.git
cd mektabati

# Create virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\\Scripts\\activate

# Install dependencies
pip install -r requirements.txt

# Run the application
python app.py
```

## Code Style

- Follow PEP 8 Python style guide
- Use meaningful variable and function names
- Add docstrings to functions and classes
- Write tests for new features

## Testing

Run tests before submitting your pull request:

```bash
python -m pytest tests/
```

## Submitting Changes

1. Make sure all tests pass
2. Update documentation if needed
3. Commit your changes with clear commit messages
4. Push to your fork
5. Submit a pull request

## Pull Request Guidelines

- Include a clear description of the changes
- Reference any related issues
- Make sure tests pass
- Update documentation if necessary

## Issues

- Use GitHub issues to report bugs or request features
- Provide clear reproduction steps for bugs
- Include relevant system information

## Questions?

Feel free to open an issue if you have questions about contributing!
