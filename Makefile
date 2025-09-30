#* Variables
PYTHON := python3
PYTHONPATH := `pwd`

#* Installation
.PHONY: install
install:
	uv sync

.PHONY: install-dev-deps
install-dev-deps:
	uv sync --all-groups --all-extras


.PHONY: build
build:
	uv build

.PHONY: install-pre-commit
pre-commit-install:
	pre-commit install

#* Formatters
.PHONY: black
black:
	uv run black --version
	uv run black --config pyproject.toml src tests examples

.PHONY: black-check
black-check:
	uv run black --version
	uv run black --diff --check --config pyproject.toml src tests examples

.PHONY: flake8
flake8:
	uv run flake8 --version
	uv run flake8 src tests examples

.PHONY: autoflake-check
autoflake-check:
	uv run autoflake --version
	uv run autoflake --check -r src tests examples

.PHONY: autoflake-format
autoflake-format:
	uv run autoflake --version
	uv run autoflake --in-place -r src tests examples
	uv run autoflake --in-place --remove-all-unused-imports -r src tests examples

.PHONY: format-codestyle
format-codestyle: black autoflake-format

.PHONY: mypy
mypy:
	uv run mypy --config-file pyproject.toml src tests examples  # Main

.PHONY: test
test:
	uv run pytest -c pyproject.toml

.PHONY: test_coverage
test_coverage:
	NUMBA_DISABLE_JIT=1 uv run pytest --cov=src -c pyproject.toml

.PHONY: test_coverage_xml
test_coverage_xml:
	NUMBA_DISABLE_JIT=1 uv run pytest --cov=src --cov-report=xml -c pyproject.toml

.PHONY: check-codestyle
check-codestyle: black-check flake8 autoflake-check

.PHONY: formatting
formatting: format-codestyle

#* Cleaning
.PHONY: pycache-remove
pycache-remove:
	find . | grep -E "(__pycache__|\.pyc|\.pyo$$)" | xargs rm -rf

.PHONY: dsstore-remove
dsstore-remove:
	find . | grep -E ".DS_Store" | xargs rm -rf

.PHONY: mypycache-remove
mypycache-remove:
	find . | grep -E ".mypy_cache" | xargs rm -rf

.PHONY: ipynbcheckpoints-remove
ipynbcheckpoints-remove:
	find . | grep -E ".ipynb_checkpoints" | xargs rm -rf

.PHONY: pytestcache-remove
pytestcache-remove:
	find . | grep -E ".pytest_cache" | xargs rm -rf

.PHONY: build-remove
build-remove:
	rm -rf build/ dist/

.PHONY: cleanup
cleanup: pycache-remove dsstore-remove ipynbcheckpoints-remove pytestcache-remove mypycache-remove build-remove

all: format-codestyle cleanup test

ci: check-codestyle