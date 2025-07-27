.PHONY: help install install-dev test test-cov lint format type-check security-check clean docs

help: ## Show this help message
	@echo "Available commands:"
	@grep -E '^[a-zA-Z_-]+:.*?## .*$$' $(MAKEFILE_LIST) | sort | awk 'BEGIN {FS = ":.*?## "}; {printf "\033[36m%-20s\033[0m %s\n", $$1, $$2}'

install: ## Install the package in development mode
	pip install -e .

install-dev: ## Install development dependencies
	pip install -r requirements-dev.txt
	pip install -e .

test: ## Run tests
	pytest AsyncioPySide6/tests/ -v

test-cov: ## Run tests with coverage
	pytest AsyncioPySide6/tests/ -v --cov=AsyncioPySide6 --cov-report=html --cov-report=term-missing

lint: ## Run linting checks
	flake8 AsyncioPySide6/
	black --check AsyncioPySide6/
	isort --check-only AsyncioPySide6/

format: ## Format code
	black AsyncioPySide6/
	isort AsyncioPySide6/

type-check: ## Run type checking
	mypy AsyncioPySide6/ --ignore-missing-imports

security-check: ## Run security checks
	bandit -r AsyncioPySide6/ -c .bandit
	safety check

clean: ## Clean build artifacts
	rm -rf build/
	rm -rf dist/
	rm -rf *.egg-info/
	rm -rf .pytest_cache/
	rm -rf .mypy_cache/
	rm -rf htmlcov/
	find . -type d -name __pycache__ -exec rm -rf {} +
	find . -type f -name "*.pyc" -delete

docs: ## Build documentation
	mkdir -p docs
	sphinx-quickstart -q -p AsyncioPySide6 -a "AsyncioPySide6 Team" -v 2.1.0 -r 2.1.0 -l en -n docs
	sphinx-build -b html docs docs/_build/html

check: lint type-check security-check test ## Run all checks

ci: check ## Run CI pipeline locally

pre-commit: ## Install pre-commit hooks
	pre-commit install

pre-commit-run: ## Run pre-commit hooks on all files
	pre-commit run --all-files 