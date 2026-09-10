.PHONY: setup test lint format migrate run clean help

PYTHON := .venv/bin/python
PIP := .venv/bin/pip
PYTEST := .venv/bin/pytest
RUFF := .venv/bin/ruff

help: ## Tampilkan daftar perintah
	@grep -E '^[a-zA-Z_-]+:.*?## .*$$' $(MAKEFILE_LIST) | \
		awk 'BEGIN {FS = ":.*?## "}; {printf "  \033[36m%-15s\033[0m %s\n", $$1, $$2}'

setup: ## Setup virtual environment dan install dependencies
	python3 -m venv .venv
	$(PIP) install --upgrade pip
	$(PIP) install -e ".[dev]"

test: ## Jalankan seluruh unit test
	$(PYTEST) tests/ -v --tb=short

lint: ## Jalankan linter Ruff
	$(RUFF) check src/ tests/ scripts/

format: ## Format kode dengan Ruff
	$(RUFF) format src/ tests/ scripts/

migrate: ## Migrasi dataset CSV ke PostgreSQL
	$(PYTHON) scripts/migrate_csv_to_postgres.py

db-up: ## Jalankan container PostgreSQL
	docker-compose up -d

db-down: ## Hentikan container PostgreSQL
	docker-compose down

run: ## Jalankan pipeline utama (all stages)
	$(PYTHON) main.py --stage all

run-app: ## Jalankan Streamlit prototype
	$(PYTHON) -m streamlit run app/streamlit_app.py

clean: ## Bersihkan cache dan artefak sementara
	find . -type d -name __pycache__ -not -path './.venv/*' -exec rm -rf {} + 2>/dev/null || true
	find . -type d -name .pytest_cache -exec rm -rf {} + 2>/dev/null || true
	find . -type f -name '*.pyc' -not -path './.venv/*' -delete 2>/dev/null || true
