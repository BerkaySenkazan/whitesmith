.DEFAULT_GOAL:=help

.EXPORT_ALL_VARIABLES:

ifndef VERBOSE
.SILENT:
endif

# set default shell
SHELL=/usr/bin/env bash -o pipefail -o errexit

TAG ?= $(shell cat TAG)
POETRY_HOME ?= ${HOME}/.local/share/pypoetry
POETRY_BINARY ?= ${POETRY_HOME}/venv/bin/poetry
POETRY_VERSION ?= 1.3.2

help:  ## Display this help
	@awk 'BEGIN {FS = ":.*##"; printf "\nUsage:\n  make \033[36m<target>\033[0m\n"} /^[a-zA-Z0-9_-]+:.*?##/ { printf "  \033[36m%-15s\033[0m %s\n", $$1, $$2 } /^##@/ { printf "\n\033[1m%s\033[0m\n", substr($$0, 5) } ' $(MAKEFILE_LIST)

.PHONY: show-version
show-version:  ## Display version
	echo -n "${TAG}"

.PHONY: build
build: ## Build whitesmith package
	echo "[build] Build whitesmith package."
	${POETRY_BINARY} build

.PHONY: install
install:  ## Install whitesmith with poetry
	@build/install.sh

.PHONY: image
image:  ## Build whitesmith image
	@build/image.sh

.PHONY: metrics
metrics: install ## Run whitesmith metrics checks
	echo "[metrics] Run whitesmith PEP 8 checks."
	${POETRY_BINARY} run flake8 --select=E,W,I --max-line-length 88 --import-order-style pep8 --statistics --count whitesmith
	echo "[metrics] Run whitesmith PEP 257 checks."
	${POETRY_BINARY} run flake8 --select=D --ignore D301 --statistics --count whitesmith
	echo "[metrics] Run whitesmith pyflakes checks."
	${POETRY_BINARY} run flake8 --select=F --statistics --count whitesmith
	echo "[metrics] Run whitesmith code complexity checks."
	${POETRY_BINARY} run flake8 --select=C901 --statistics --count whitesmith
	echo "[metrics] Run whitesmith open TODO checks."
	${POETRY_BINARY} run flake8 --select=T --statistics --count whitesmith tests
	echo "[metrics] Run whitesmith black checks."
	${POETRY_BINARY} run black --check whitesmith

.PHONY: unit-test
unit-test: install ## Run whitesmith unit tests
	echo "[unit-test] Run whitesmith unit tests."
	${POETRY_BINARY} run pytest tests/unit

.PHONY: integration-test
integration-test: install ## Run whitesmith integration tests
	echo "[unit-test] Run whitesmith integration tests."
	${POETRY_BINARY} run pytest tests/integration

.PHONY: coverage
coverage: install  ## Run whitesmith tests coverage
	echo "[coverage] Run whitesmith tests coverage."
	${POETRY_BINARY} run pytest --cov=whitesmith --cov-fail-under=90 --cov-report=xml --cov-report=term-missing tests

.PHONY: test
test: unit-test integration-test  ## Run whitesmith tests

.PHONY: docs
docs: install ## Build whitesmith documentation
	echo "[docs] Build whitesmith documentation."
	${POETRY_BINARY} run sphinx-build docs site

.PHONY: mypy
mypy: install  ## Run whitesmith mypy checks
	echo "[mypy] Run whitesmith mypy checks."
	${POETRY_BINARY} run mypy whitesmith
