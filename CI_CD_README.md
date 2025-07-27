# CI/CD Pipeline Documentation

This project uses GitHub Actions for continuous integration and deployment. The pipelines are designed to ensure code quality, security, and automated releases.

## Workflows

### 1. CI (`ci.yml`)
**Triggers**: Push to main/develop, Pull requests to main/develop

**Jobs**:
- **Test**: Runs on Python 3.11/3.12 with PySide6 6.9.1/6.10.0
  - Linting (flake8, black, isort)
  - Type checking (mypy)
  - Tests with coverage
  - Uploads coverage to Codecov
- **Security**: Security checks with bandit and safety

### 2. Test (`test.yml`)
**Triggers**: Push to main/develop, Pull requests to main/develop

**Jobs**:
- **Test**: Comprehensive testing with multiple Python versions
- **Security**: Security vulnerability scanning
- **Documentation**: Builds and validates documentation

### 3. Documentation (`docs.yml`)
**Triggers**: Push to main, Pull requests to main

**Jobs**:
- **Build Docs**: Builds Sphinx documentation
- **Deploy Docs**: Deploys to GitHub Pages (main branch only)

### 4. Pre-commit (`pre-commit.yml`)
**Triggers**: Pull requests to main/develop

**Jobs**:
- **Pre-commit**: Runs pre-commit hooks on all files

### 5. Release (`release.yml`)
**Triggers**: Push tags starting with 'v'

**Jobs**:
- **Release**: Automated release process
  - Runs all checks and tests
  - Builds documentation
  - Builds and publishes to PyPI
  - Creates GitHub release

## Makefile Integration

All workflows use the project's Makefile targets for consistency:

```bash
make check          # Run linting, type checking, and security checks
make test           # Run tests
make test-cov       # Run tests with coverage
make security-check # Run security checks
make docs           # Build documentation
make docs-linkcheck # Check documentation links
```

## Cache Strategy

The workflows use intelligent caching for:
- pip dependencies (based on requirements files)
- Python version and PySide6 version combinations
- Documentation build artifacts

## Security

- **Bandit**: Static security analysis
- **Safety**: Dependency vulnerability scanning
- **Type checking**: Mypy for type safety
- **Linting**: Flake8, Black, isort for code quality

## Documentation

- **Sphinx**: Automated documentation building
- **GitHub Pages**: Automatic deployment
- **Link checking**: Validates external links
- **Cross-references**: Links to Python and PySide6 docs

## Release Process

1. Create and push a tag: `git tag v2.1.1 && git push origin v2.1.1`
2. The release workflow automatically:
   - Runs all checks and tests
   - Builds documentation
   - Publishes to PyPI
   - Creates a GitHub release

## Environment Variables

Required secrets:
- `PYPI_API_TOKEN`: For PyPI publishing
- `GITHUB_TOKEN`: For GitHub releases (automatically provided)

## Local Development

To run the same checks locally:

```bash
# Install dependencies
pip install -r requirements-dev.txt
pip install -e .

# Run all checks
make check

# Run tests with coverage
make test-cov

# Build documentation
make docs

# Run security checks
make security-check
```

## Troubleshooting

### Common Issues

1. **Cache misses**: Clear GitHub Actions cache or update cache keys
2. **PySide6 installation**: Ensure system dependencies are installed
3. **Documentation build**: Check Sphinx configuration and dependencies
4. **Security failures**: Review bandit and safety reports

### Debugging

- Check workflow logs in GitHub Actions
- Run commands locally to reproduce issues
- Use `make docs-clean` to reset documentation build
- Use `make clean` to reset all build artifacts 