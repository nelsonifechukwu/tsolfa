.PHONY: help install install-dev test test-cov lint format type-check clean docs
.DEFAULT_GOAL := help

help: ## Show this help message
	@echo "Available commands:"
	@grep -E '^[a-zA-Z_-]+:.*?## .*$$' $(MAKEFILE_LIST) | sort | awk 'BEGIN {FS = ":.*?## "}; {printf "  \033[36m%-15s\033[0m %s\n", $$1, $$2}'

install: ## Install package
	pip install -e .

install-dev: ## Install package with development dependencies
	pip install -e ".[dev,ml]"
	pre-commit install

test: ## Run tests
	pytest

test-cov: ## Run tests with coverage
	pytest --cov=tsolfa --cov-report=html --cov-report=term-missing

lint: ## Run linting checks
	flake8 tsolfa
	black --check tsolfa
	isort --check-only tsolfa

format: ## Format code
	black tsolfa
	isort tsolfa

type-check: ## Run type checking
	mypy tsolfa

clean: ## Clean build artifacts
	rm -rf build/
	rm -rf dist/
	rm -rf *.egg-info/
	rm -rf .pytest_cache/
	rm -rf htmlcov/
	find . -type f -name "*.pyc" -delete
	find . -type d -name "__pycache__" -delete

docs: ## Generate documentation
	@echo "Documentation generation not yet implemented"

benchmark: ## Run performance benchmarks
	@echo "Benchmarks not yet implemented"

profile: ## Profile the transcription pipeline
	@echo "Profiling not yet implemented"