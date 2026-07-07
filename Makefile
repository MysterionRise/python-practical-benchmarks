PYTHON ?= python3
VENV ?= .venv
VENV_PYTHON := $(VENV)/bin/python
OUTPUT_DIR ?= reports/output
QUICK_JSON ?= $(OUTPUT_DIR)/quick-results.json
QUICK_REPORT ?= $(OUTPUT_DIR)/quick-summary.md

.PHONY: setup verify bench-json bench-report clean-report

setup:
	$(PYTHON) -m venv $(VENV)
	$(VENV_PYTHON) -m pip install --upgrade pip
	$(VENV_PYTHON) -m pip install -e ".[dev,optional]"

verify:
	$(VENV_PYTHON) -m ruff check .
	$(VENV_PYTHON) -m ruff format --check .
	$(VENV_PYTHON) -m mypy .
	$(VENV_PYTHON) -m pytest tests/ -v
	$(VENV_PYTHON) run_all_tests.py --all --quick

bench-json:
	$(VENV_PYTHON) run_all_tests.py --all --quick --format json --output $(QUICK_JSON)

bench-report: bench-json
	$(VENV_PYTHON) scripts/render_report.py $(QUICK_JSON) --output $(QUICK_REPORT)

clean-report:
	rm -f $(QUICK_JSON) $(QUICK_REPORT)
