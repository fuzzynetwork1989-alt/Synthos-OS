.PHONY: help dev test lint format build docker-up docker-down clean install install-python install-node

help: ## Show this help message
	@echo 'Usage: make [target]'
	@echo ''
	@echo 'Available targets:'
	@awk 'BEGIN {FS = ":.*?## "} /^[a-zA-Z_-]+:.*?## / {printf "  %-20s %s\n", $$1, $$2}' $(MAKEFILE_LIST)

install: install-python install-node ## Install all dependencies

install-python: ## Install Python dependencies
	python -m pip install -e ".[dev]"

install-node: ## Install Node.js dependencies
	pnpm install

dev: ## Start development servers
	pnpm run dev

test: ## Run all tests
	pnpm run test
	python -m pytest tests/

lint: ## Run all linters
	pnpm run lint
	ruff check .
	black --check .
	mypy .

format: ## Format all code
	pnpm run format
	black .
	ruff check --fix .

build: ## Build all projects
	pnpm run build

docker-up: ## Start Docker services
	docker-compose up -d

docker-down: ## Stop Docker services
	docker-compose down

clean: ## Clean build artifacts
	find . -type d -name __pycache__ -exec rm -rf {} +
	find . -type d -name .pytest_cache -exec rm -rf {} +
	find . -type d -name node_modules -exec rm -rf {} +
	find . -type d -name dist -exec rm -rf {} +
	find . -type d -name .next -exec rm -rf {} +
