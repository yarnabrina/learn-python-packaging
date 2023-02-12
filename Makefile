MAKEFLAGS += --silent

SHELL := /usr/bin/env
.SHELLFLAGS := bash -c -e +x

.DEFAULT_GOAL := help

PYTHON_DEPENDENCIES_DIRECTORY := ./requirements

PYTHON_SOURCE_DIRECTORY := ./src
PYTHON_DOCS_DIRECTORY := ./docs
PYTHON_DIST_DIRECTORY := ./dist

PYTHON_SOURCE_SCRIPTS_PATTERN := "${PYTHON_SOURCE_DIRECTORY}/**/*.py"
PYTHON_TEST_SCRIPTS_PATTERN := "**/tests/*.py"

PYTHON_SOURCE_SCRIPTS := $(shell find ${PYTHON_SOURCE_DIRECTORY} -type f -name "*.py")

define check_install_status =
	$(shell python3 -m pip show ${1} > /dev/null 2>&1)
	if [ ${.SHELLSTATUS} -eq 1 ]; then
		python3 -m pip install --upgrade ${1}
	fi
endef

.ONESHELL:
.PHONY: autoflake-formatter
autoflake-formatter: venv
	source venv/bin/activate
	$(call check_install_status,autoflake)
	autoflake $(PYTHON_SOURCE_SCRIPTS)

.ONESHELL:
.PHONY: bandit-linter
bandit-linter: venv
	source venv/bin/activate
	$(call check_install_status,bandit)
	bandit \
    --recursive \
	--severity-level high \
	--confidence-level high \
	${PYTHON_SOURCE_DIRECTORY}

.ONESHELL:
.PHONY: black-formatter
black-formatter: venv
	source venv/bin/activate
	$(call check_install_status,black)
	black ${PYTHON_SOURCE_DIRECTORY}

.ONESHELL:
.PHONY: build-distribution
build-distribution: venv
	source venv/bin/activate
	$(call check_install_status,build)
	python3 -m build --outdir ${PYTHON_DIST_DIRECTORY}

.PHONY: clean-coverage
clean-coverage:
	find . \
	-type f -name .coverage -delete \
	-o \
	-type d -name htmlcov \
	-exec rm -r "{}" +

.PHONY: clean-mypy_cache
clean-mypy_cache:
	find . \
	-type d -name .mypy_cache \
	-exec rm -r "{}" +

.PHONY: clean-pycache
clean-pycache:
	find . \
	-type f -name '*.py[co]' -delete \
	-o \
	-type d -name __pycache__ -delete

.PHONY: clean-pytest_cache
clean-pytest_cache:
	find . \
	-type d -name .pytest_cache \
	-exec rm -r "{}" +

.ONESHELL:
.PHONY: coverage-run
coverage-run: venv
	source venv/bin/activate
	$(call check_install_status,coverage)
	$(call check_install_status,pytest)
	coverage run

.ONESHELL:
.PHONY: coverage-html
coverage-html: venv
	source venv/bin/activate
	$(call check_install_status,coverage)
	coverage html

.ONESHELL:
.PHONY: docformatter-formatter
docformatter-formatter: venv
	source venv/bin/activate
	$(call check_install_status,docformatter)
	docformatter $(PYTHON_SOURCE_SCRIPTS)

.ONESHELL:
.PHONY: flake8-linter
flake8-linter: venv
	source venv/bin/activate
	$(call check_install_status,flake8)
	flake8 \
	--extend-ignore E203 \
	--per-file-ignores __init__.py:F401 \
	--max-line-length 99 \
	${PYTHON_SOURCE_DIRECTORY}

.ONESHELL:
.PHONY: interrogate-linter
interrogate-linter: venv
	source venv/bin/activate
	$(call check_install_status,interrogate)
	interrogate ${PYTHON_SOURCE_DIRECTORY}

.ONESHELL:
.PHONY: isort-formatter
isort-formatter: venv
	source venv/bin/activate
	$(call check_install_status,isort)
	isort ${PYTHON_SOURCE_DIRECTORY}

.ONESHELL:
.PHONY: mypy-linter
mypy-linter: venv
	source venv/bin/activate
	$(call check_install_status,mypy)
	mypy ${PYTHON_SOURCE_DIRECTORY}

.ONESHELL:
.PHONY: pre-commit-install
pre-commit-install: venv
	source venv/bin/activate
	$(call check_install_status,pre-commit)
	pre-commit install

.ONESHELL:
.PHONY: pre-commit-autoupdate
pre-commit-autoupdate: venv
	source venv/bin/activate
	pre-commit autoupdate

.ONESHELL:
.PHONY: pre-commit-run
pre-commit-run: venv
	source venv/bin/activate
	pre-commit run --all-files

.ONESHELL:
.PHONY: pydocstyle-linter
pydocstyle-linter: venv
	source venv/bin/activate
	$(call check_install_status,pydocstyle)
	pydocstyle ${PYTHON_SOURCE_DIRECTORY}

.ONESHELL:
.PHONY: pylint-linter
pylint-linter: venv
	source venv/bin/activate
	$(call check_install_status,pylint)
	pylint ${PYTHON_SOURCE_DIRECTORY}

.ONESHELL:
.PHONY: pyright-linter
pyright-linter: venv
	source venv/bin/activate
	$(call check_install_status,pyright)
	pyright ${PYTHON_SOURCE_DIRECTORY}

.ONESHELL:
.PHONY: pyupgrade-formatter
pyupgrade-formatter: venv
	source venv/bin/activate
	$(call check_install_status,pyupgrade)
	pyupgrade --py310-plus $(PYTHON_SOURCE_SCRIPTS)

.ONESHELL:
.PHONY: pytest-doctest
pytest-doctest: venv
	source venv/bin/activate
	$(call check_install_status,pytest)
	pytest -k "not test_"

.ONESHELL:
.PHONY: pytest-failure
pytest-failure: venv
	source venv/bin/activate
	$(call check_install_status,pytest)
	pytest -k "failure"

.ONESHELL:
.PHONY: pytest-others
pytest-others: venv
	source venv/bin/activate
	$(call check_install_status,pytest)
	pytest -k "test and not failure and not successful"

.ONESHELL:
.PHONY: pytest-successful
pytest-successful: venv
	source venv/bin/activate
	$(call check_install_status,pytest)
	pytest -k "successful"

.ONESHELL:
.PHONY: sphinx-source
sphinx-source: venv
	source venv/bin/activate
	$(call check_install_status,Sphinx)
	sphinx-apidoc \
	--output-dir ${PYTHON_DOCS_DIRECTORY}/source \
	--maxdepth 3 \
	--force \
	--follow-links \
	--separate \
	${PYTHON_SOURCE_DIRECTORY}

.ONESHELL:
.PHONY: sphinx-build
sphinx-build: venv
	source venv/bin/activate
	$(call check_install_status,Sphinx)
	$(call check_install_status,sphinx-copybutton)
	$(call check_install_status,sphinx-rtd-theme)
	sphinx-build \
	-b html \
	${PYTHON_DOCS_DIRECTORY}/source \
	${PYTHON_DOCS_DIRECTORY}/build

.ONESHELL:
.PHONY: twine-check
twine-check: venv
	source venv/bin/activate
	$(call check_install_status,twine)
	twine check --strict ${PYTHON_DIST_DIRECTORY}/*

.ONESHELL:
.PHONY: twine-upload
twine-upload: venv
	source venv/bin/activate
	$(call check_install_status,twine)
	twine upload ${PYTHON_DIST_DIRECTORY}/*

.ONESHELL:
venv:
	python3 -m venv venv
	echo "*" > venv/.gitignore
	source venv/bin/activate
	python3 -m pip install --upgrade pip setuptools wheel
	python3 -m pip install --editable ".[all]"

.ONESHELL:
venv-upgrade: venv
	source venv/bin/activate
	python3 -m pip install --upgrade pip setuptools wheel
	python3 -m pip install --upgrade \
	--requirement ${PYTHON_DEPENDENCIES_DIRECTORY}/requirements.txt \
	--requirement ${PYTHON_DEPENDENCIES_DIRECTORY}/requirements.dev.txt \
	--requirement ${PYTHON_DEPENDENCIES_DIRECTORY}/requirements.doc.txt \
	--requirement ${PYTHON_DEPENDENCIES_DIRECTORY}/requirements.format.txt \
	--requirement ${PYTHON_DEPENDENCIES_DIRECTORY}/requirements.lint.txt \
	--requirement ${PYTHON_DEPENDENCIES_DIRECTORY}/requirements.release.txt \
	--requirement ${PYTHON_DEPENDENCIES_DIRECTORY}/requirements.test.txt

.ONESHELL:
.PHONY: vulture-linter
vulture-linter: venv
	source venv/bin/activate
	$(call check_install_status,vulture)
	vulture ${PYTHON_SOURCE_DIRECTORY}

## help
##     list all wrapper targets
##     show documentaions of wrapper targets
.PHONY: help
help: Makefile
	@sed -n 's/^## //p' $<

## setup
##     create isolated environment with editable package and dependencies (venv)
##     add pre-commit to git hooks (pre-commit-install)
.PHONY: setup
setup: venv pre-commit-install

## update
##     upgrade isolated environment to latest package and dependencies (venv-upgrade)
##     update versions of pre-commit hooks (pre-commit-autoupdate)
.PHONY: update
update: venv-upgrade pre-commit-autoupdate

## format
##     change codes for older versions (pyupgrade-formatter)
##     remove pyflake detected issues (autoflake-formatter)
##     sort imports (isort-formatter)
##     format docstrings (docformatter-formatter)
##     format code style (black-formatter)
.PHONY: format
format: pyupgrade-formatter autoflake-formatter isort-formatter docformatter-formatter black-formatter

## lint
##     find security issues (bandit-linter)
##     lint all python scripts (flake8-linter)
##     check docstring coverage (interrogate-linter)
##     check types (mypy-linter)
##     check docstring presence and formats (pydocstyle-linter)
##     lint all python scripts (pylint-linter)
##     check types (pyright-linter)
##     find dead code (vulture-linter)
.PHONY: lint
lint: bandit-linter flake8-linter interrogate-linter mypy-linter pydocstyle-linter pylint-linter pyright-linter vulture-linter

## test
##     test doctests (pytest-doctest)
##     test successful operations (pytest-successful)
##     test failed operations (pytest-failure)
##     test other unit tests (pytest-others)
.PHONY: test
test: pytest-doctest pytest-successful pytest-failure pytest-others

## coverage
##     test all doctests and unit tests (coverage-run)
##     create test coverage report (coverage-html)
.PHONY: coverage
coverage: coverage-run coverage-html

## docs
##     prepare documentation sources with directives (sphinx-source)
##     create HTML documentation from source files (sphinx-build)
.PHONY: docs
docs: sphinx-source sphinx-build

## release
##     prepare documentation sources with directives (sphinx-source)
##     create HTML documentation from source files (sphinx-build)
.PHONY: release
release: build-distribution twine-check twine-upload

## cleanup
##     delete all pycache directories and other cache files (clean-pycache)
##     delete all mypy cache (clean-mypy_cache)
##     delete all unit test cache (clean-pytest_cache)
##     delete all coverage results (clean-coverage)
.PHONY: cleanup
cleanup: clean-pycache clean-mypy_cache clean-pytest_cache clean-coverage
