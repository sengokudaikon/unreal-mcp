.PHONY: help install install-dev test lint format type-check clean security

# Default target
help:
	@echo "Available commands:"
	@echo "  install      Install package"
	@echo "  install-dev  Install package with development dependencies"
	@echo "  test         Run tests"
	@echo "  test-cov     Run tests with coverage"
	@echo "  lint         Run linting"
	@echo "  format       Format code"
	@echo "  type-check   Run type checking"
	@echo "  security     Run security checks"
	@echo "  clean        Clean cache files"

# Installation
install:
	pip install -e .

install-dev:
	pip install -e .[dev]

# Testing
test:
	python -m pytest tests/ -v

test-cov:
	python -m pytest tests/ -v --cov=core --cov=services --cov=tools --cov-report=term-missing --cov-report=html

test-integration:
	python -m pytest tests/test_mcp_integration.py -v -m integration

test-all: test test-integration

# Code quality
lint:
	python -m flake8 core/ services/ tools/ tests/
	@echo "Linting completed"

format:
	python -m black core/ services/ tools/ tests/
	python -m isort core/ services/ tools/ tests/
	@echo "Code formatted"

format-check:
	python -m black --check core/ services/ tools/ tests/
	python -m isort --check-only core/ services/ tools/ tests/

type-check:
	python -m mypy core/ services/ tools/
	@echo "Type checking completed"

# Security
security:
	bandit -r core/ services/ tools/
	safety check
	@echo "Security checks completed"

# Cleanup
clean:
	find . -type d -name "__pycache__" -exec rm -rf {} +
	find . -type d -name "*.egg-info" -exec rm -rf {} +
	find . -type f -name "*.pyc" -delete
	rm -rf .coverage htmlcov/ .pytest_cache/ .mypy_cache/
	@echo "Cleaned cache files"

# Pre-commit hook
pre-commit: format-check lint type-check test
	@echo "Pre-commit checks completed"

# Development setup
dev-setup: install-dev
	@echo "Development environment setup completed"