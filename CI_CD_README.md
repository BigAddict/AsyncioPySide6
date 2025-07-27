# CI/CD Pipeline Documentation

This document describes the CI/CD pipeline setup for the AsyncioPySide6 project.

## Overview

The CI/CD pipeline consists of GitHub Actions workflows that handle:

- **Continuous Integration (CI)** - Testing, linting, and code quality checks
- **Documentation** - Building and deploying documentation to GitHub Pages
- **Dependency Management** - Automated dependency updates with Dependabot

## Workflows

### 1. CI Workflow (`.github/workflows/ci.yml`)

**Triggers:**
- Push to `main` or `develop` branches
- Pull requests to `main` or `develop` branches

**Jobs:**

#### Test Job
- **Matrix Strategy:** Tests against Python 3.11, 3.12 and PySide6 6.9.1, 6.10.0
- **System Dependencies:** Installs OpenGL libraries for GUI testing
- **Caching:** Caches pip dependencies for faster builds
- **Code Quality Checks:**
  - Flake8 linting
  - Black code formatting check
  - isort import sorting check
  - MyPy type checking
- **Testing:** Runs pytest with coverage reporting
- **Coverage:** Uploads coverage reports to Codecov

#### Security Job
- **Bandit:** Security linting for Python code
- **Safety:** Checks for known security vulnerabilities in dependencies
- **Artifacts:** Uploads security reports as artifacts

### 2. Documentation Workflow (`.github/workflows/docs.yml`)

**Triggers:**
- Push to `main` branch
- Pull requests to `main` branch

**Jobs:**

#### Build Docs Job
- **Dependencies:** Sphinx and documentation tools
- **Documentation Building:** Generates HTML documentation
- **Artifacts:** Uploads built documentation as artifacts

#### Deploy Docs Job
- **GitHub Pages:** Deploys documentation to GitHub Pages
- **Condition:** Only runs on main branch pushes

### 3. Dependabot Workflow (`.github/workflows/dependabot.yml`)

**Triggers:**
- Pull requests from Dependabot

**Jobs:**

#### Dependabot Job
- **Condition:** Only runs for Dependabot PRs
- **Testing:** Runs full test suite on dependency updates
- **Code Quality:** Runs linting and type checking
- **Commenting:** Adds approval comment to PR

## Configuration Files

### 1. `pyproject.toml`

Modern Python packaging configuration with:

- **Build System:** setuptools with wheel
- **Project Metadata:** Name, version, description, authors, classifiers
- **Dependencies:** Runtime and development dependencies
- **Tool Configurations:**
  - Black code formatting
  - isort import sorting
  - MyPy type checking
  - pytest testing
  - Coverage reporting
  - Bandit security scanning

### 2. `.flake8`

Flake8 linting configuration:

- **Line Length:** 127 characters
- **Complexity:** Maximum 10
- **Exclusions:** Build artifacts, cache directories
- **Ignores:** Common false positives

### 3. `.pre-commit-config.yaml`

Pre-commit hooks for local development:

- **Basic Hooks:** Trailing whitespace, file endings, YAML validation
- **Code Formatting:** Black and isort
- **Linting:** Flake8
- **Type Checking:** MyPy
- **Security:** Bandit

### 4. `Makefile`

Development task automation:

- **Installation:** `make install`, `make install-dev`
- **Testing:** `make test`, `make test-cov`
- **Code Quality:** `make lint`, `make format`, `make type-check`
- **Security:** `make security-check`
- **Documentation:** `make docs`
- **Pre-commit:** `make pre-commit`, `make pre-commit-run`

### 5. `.github/dependabot.yml`

Dependabot configuration:

- **Python Dependencies:** Weekly updates on Mondays
- **GitHub Actions:** Weekly updates on Mondays
- **Security:** Ignores major version updates for critical dependencies
- **Automation:** Auto-assigns reviewers and labels

## Development Workflow

### Local Development

1. **Setup:**
   ```bash
   # Clone repository
   git clone https://github.com/your-username/AsyncioPySide6.git
   cd AsyncioPySide6
   
   # Create virtual environment
   python -m venv .venv
   source .venv/bin/activate  # On Windows: .venv\Scripts\activate
   
   # Install development dependencies
   make install-dev
   
   # Install pre-commit hooks
   make pre-commit
   ```

2. **Development:**
   ```bash
   # Run all checks
   make check
   
   # Run tests with coverage
   make test-cov
   
   # Format code
   make format
   
   # Run CI pipeline locally
   make ci
   ```

3. **Pre-commit:**
   ```bash
   # Run pre-commit hooks on all files
   make pre-commit-run
   ```

### Branch Strategy

- **`main`:** Production-ready code
- **`develop`:** Development branch for features
- **Feature branches:** `feature/description`
- **Bug fix branches:** `fix/description`

## Monitoring and Notifications

### Status Badges

Add these badges to your README.md:

```markdown
[![CI](https://github.com/your-username/AsyncioPySide6/workflows/CI/badge.svg)](https://github.com/your-username/AsyncioPySide6/actions?query=workflow%3ACI)
[![Documentation](https://github.com/your-username/AsyncioPySide6/workflows/Documentation/badge.svg)](https://github.com/your-username/AsyncioPySide6/actions?query=workflow%3ADocumentation)
[![Coverage](https://codecov.io/gh/your-username/AsyncioPySide6/branch/main/graph/badge.svg)](https://codecov.io/gh/your-username/AsyncioPySide6)
```

### Notifications

- **GitHub:** Built-in notifications for workflow failures
- **Email:** Configure in GitHub repository settings
- **Slack:** Can be added via webhook integration

## Troubleshooting

### Common Issues

1. **PySide6 Installation Failures:**
   - Ensure system dependencies are installed
   - Check Python version compatibility

2. **GUI Test Failures:**
   - Ensure X11 forwarding or virtual display
   - Install OpenGL libraries

3. **Coverage Upload Failures:**
   - Check Codecov token configuration
   - Verify coverage file generation

### Debugging

1. **Local Testing:**
   ```bash
   # Test CI workflow locally
   make ci
   
   # Test specific components
   make lint
   make test
   make type-check
   ```

2. **Workflow Debugging:**
   - Enable debug logging in workflows
   - Check workflow run logs

## Best Practices

### Code Quality

1. **Pre-commit Hooks:** Always run before committing
2. **Type Annotations:** Use MyPy for type safety
3. **Documentation:** Keep docstrings up to date
4. **Testing:** Maintain high test coverage

### Security

1. **Dependency Scanning:** Regular security audits
2. **Access Control:** Limit repository permissions

### Performance

1. **Caching:** Leverage GitHub Actions caching
2. **Parallel Jobs:** Use matrix strategies
3. **Artifacts:** Share data between jobs efficiently

## Future Enhancements

### Planned Improvements

1. **Multi-platform Testing:** Windows and macOS support
2. **Performance Benchmarking:** Automated performance tests
3. **Docker Integration:** Containerized testing
4. **Slack Notifications:** Real-time status updates

### Monitoring

1. **Workflow Analytics:** Track build times and success rates
2. **Dependency Health:** Monitor outdated dependencies
3. **Security Alerts:** Automated vulnerability scanning

## Support

For issues with the CI/CD pipeline:

1. **Check Workflow Logs:** Detailed error information
2. **Review Configuration:** Verify YAML syntax and settings
3. **Test Locally:** Use Makefile commands for local testing
4. **GitHub Issues:** Report bugs and feature requests

## Contributing

When contributing to the CI/CD pipeline:

1. **Test Changes:** Use local testing commands
2. **Update Documentation:** Keep this README current
3. **Follow Standards:** Use consistent formatting and naming
4. **Security Review:** Ensure no secrets are exposed 