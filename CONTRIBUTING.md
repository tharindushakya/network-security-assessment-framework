# Contributing to Network Security Assessment Framework (NSAF)

We welcome contributions to NSAF! This document provides guidelines for contributing to the project.

## 🚀 Getting Started

### Prerequisites

- Python 3.7 or higher
- Git
- Basic understanding of network security concepts

### Development Setup

1. Fork the repository
2. Clone your fork:
   ```bash
   git clone https://github.com/yourusername/network-security-assessment-framework.git
   cd network-security-assessment-framework
   ```

3. Create a virtual environment:
   ```bash
   python -m venv .venv
   source .venv/bin/activate  # On Windows: .venv\Scripts\activate
   ```

4. Install development dependencies:
   ```bash
   pip install -e ".[dev]"
   ```

5. Run tests to ensure everything works:
   ```bash
   pytest
   ```

## 🛠️ Development Guidelines

### Code Style

- Follow PEP 8 Python style guidelines
- Use `black` for code formatting:
  ```bash
  black nsaf/
  ```
- Use `isort` for import sorting:
  ```bash
  isort nsaf/
  ```
- Use `flake8` for linting:
  ```bash
  flake8 nsaf/
  ```

### Type Hints

- Use type hints for all function parameters and return values
- Run `mypy` for type checking:
  ```bash
  mypy nsaf/
  ```

### Documentation

- Document all public functions and classes
- Use docstrings following Google style
- Update README.md for significant changes

### Testing

- Write tests for new functionality
- Maintain test coverage above 80%
- Run the full test suite:
  ```bash
  pytest --cov=nsaf tests/
  ```

## 🔄 Contribution Process

### 1. Choose an Issue

- Check the [Issues](https://github.com/yourusername/network-security-assessment-framework/issues) page
- Look for issues labeled `good first issue` or `help wanted`
- Comment on the issue to let others know you're working on it

### 2. Create a Branch

Create a new branch for your feature or fix:
```bash
git checkout -b feature/your-feature-name
```

Branch naming conventions:
- `feature/description` - for new features
- `fix/description` - for bug fixes
- `docs/description` - for documentation updates
- `refactor/description` - for code refactoring

### 3. Make Changes

- Make your changes in small, logical commits
- Write clear commit messages
- Follow the coding standards
- Add or update tests as needed

### 4. Test Your Changes

Run the full test suite and ensure all tests pass:
```bash
# Run tests
pytest

# Run with coverage
pytest --cov=nsaf

# Run type checking
mypy nsaf/

# Run linting
flake8 nsaf/

# Format code
black nsaf/
isort nsaf/
```

### 5. Submit a Pull Request

1. Push your branch to your fork:
   ```bash
   git push origin feature/your-feature-name
   ```

2. Create a Pull Request on GitHub
3. Fill out the PR template completely
4. Link any related issues
5. Wait for review and address feedback

## 📝 Pull Request Guidelines

### PR Title

Use clear, descriptive titles:
- `feat: add new vulnerability scanner for web applications`
- `fix: resolve timeout issue in port scanning`
- `docs: update installation instructions`

### PR Description

Include:
- Description of changes
- Motivation/reasoning
- Testing performed
- Screenshots (if applicable)
- Breaking changes (if any)

### Review Process

- All PRs require at least one review
- Address all review comments
- Keep PRs focused and small when possible
- Rebase or merge commits as requested

## 🎯 Types of Contributions

### New Features

- New vulnerability scanners
- Additional report formats
- Performance improvements
- New scanning techniques

### Bug Fixes

- Fix existing functionality
- Address edge cases
- Improve error handling

### Documentation

- API documentation
- Usage examples
- Tutorial improvements
- Wiki content

### Testing

- Unit tests
- Integration tests
- Performance tests
- Test data/fixtures

## 🔒 Security Considerations

### Responsible Development

- Never include real vulnerability data in tests
- Use only test/dummy data
- Don't commit sensitive information
- Follow secure coding practices

### Vulnerability Reporting

If you discover a security vulnerability:

1. **DO NOT** open a public issue
2. Email us privately at security@nsaf.project
3. Provide detailed description
4. Allow time for fix before disclosure

## 🏷️ Versioning

We use [Semantic Versioning](https://semver.org/):

- `MAJOR.MINOR.PATCH`
- Breaking changes increment MAJOR
- New features increment MINOR
- Bug fixes increment PATCH

## 📧 Communication

- **Issues**: Bug reports and feature requests
- **Discussions**: General questions and ideas
- **Email**: security@nsaf.project (security issues only)

## 🎉 Recognition

Contributors will be:
- Listed in CONTRIBUTORS.md
- Mentioned in release notes
- Credited in documentation

## ❓ Questions?

- Check existing issues and discussions
- Review documentation
- Ask in GitHub Discussions
- Contact maintainers

Thank you for contributing to NSAF! 🙏
