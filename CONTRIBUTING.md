# Contributing to the Flask Multi-Environment Template

Thank you for considering contributing to this template. This document provides guidelines and instructions for contributing.

## Code of Conduct

By participating in this project, you agree to abide by its Code of Conduct.

## How Can I Contribute?

### Reporting Bugs

- Check if the bug is already reported in the Issues
- Use the Bug Report template
- Provide detailed steps to reproduce the bug
- Include logs, screenshots, and environment information

### Suggesting Enhancements

- Check if the enhancement is already suggested in the Issues
- Use the Feature Request template
- Explain the rationale and benefits
- Provide implementation details if possible

### Pull Requests

1. Fork the repository
2. Create a branch (`git checkout -b feature/your-feature`)
3. Make your changes
4. Run tests
5. Submit a pull request

## Development Workflow

### Setup Development Environment

```bash
git clone https://github.com/yourusername/flask-multi-environment-template.git
cd flask-multi-environment-template
python -m venv venv
source venv/bin/activate
pip install -r requirements.txt -r requirements-dev.txt -r requirements-test.txt
```

### Run Tests

```bash
make test
```

### Coding Standards

This project follows PEP 8 style guidelines. Use flake8 and black for code formatting.

```bash
flake8 .
black .
```

## Template Structure

The template is organized to separate concerns and provide clarity:

- `app/`: The Flask application code
- `config/`: Configuration for different environments
- `tests/`: Test suites
- `scripts/`: Utility scripts for development

## Branch Strategy

- `main`: Stable, production-ready template
- `template`: For template development and enhancements
- `feature/*`: For new features
- `bugfix/*`: For bug fixes

## Commit Message Guidelines

Format: `type(scope): subject`

Types:
- feat: A new feature
- fix: A bug fix
- docs: Documentation changes
- style: Code style changes
- refactor: Code changes that neither fixes bugs nor adds features
- test: Adding or modifying tests
- chore: Changes to the build process or auxiliary tools

Example: `feat(auth): add OAuth support`

## Documentation

- Document new features and changes
- Update TEMPLATE.md with usage examples
- Add comments to complex code sections

## Release Process

1. Update CHANGELOG.md
2. Update version in metadata
3. Create a release on GitHub with release notes
4. Tag the release with a version number

Thank you for contributing! 