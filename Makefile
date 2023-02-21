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

## help
##     list all wrapper targets
##     show documentaions of wrapper targets
.PHONY: help
help: Makefile
	@sed -n 's/^## //p' $<

.ONESHELL:
venv:
	python3 -m venv venv
	echo "*" > venv/.gitignore
	source venv/bin/activate
	python3 -m pip install --upgrade pip setuptools wheel
	python3 -m pip install --editable ".[all]"

.ONESHELL:
.PHONY: pre-commit-install
pre-commit-install: venv
	source venv/bin/activate
	$(call check_install_status,pre-commit)
	pre-commit install

## setup
##     create isolated environment with editable package and dependencies (venv)
##     add pre-commit to git hooks (pre-commit-install)
.PHONY: setup
setup: venv pre-commit-install

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
.PHONY: pre-commit-autoupdate
pre-commit-autoupdate: venv
	source venv/bin/activate
	pre-commit autoupdate

## update
##     upgrade isolated environment to latest package and dependencies (venv-upgrade)
##     update versions of pre-commit hooks (pre-commit-autoupdate)
.PHONY: update
update: venv-upgrade pre-commit-autoupdate

.ONESHELL:
.PHONY: autoflake
autoflake: venv
	source venv/bin/activate
	$(call check_install_status,autoflake)
	autoflake $(PYTHON_SOURCE_SCRIPTS)

.ONESHELL:
.PHONY: black
black: venv
	source venv/bin/activate
	$(call check_install_status,black)
	black ${PYTHON_SOURCE_DIRECTORY}

.ONESHELL:
.PHONY: blacken-docs
blacken-docs: venv
	source venv/bin/activate
	$(call check_install_status,blacken-docs)
	blacken-docs \
	--line-length 87 \
	--target-version py310 \
	$(PYTHON_SOURCE_SCRIPTS)

.ONESHELL:
.PHONY: docformatter
docformatter: venv
	source venv/bin/activate
	$(call check_install_status,docformatter)
	docformatter ${PYTHON_SOURCE_DIRECTORY}

.ONESHELL:
.PHONY: isort
isort: venv
	source venv/bin/activate
	$(call check_install_status,isort)
	isort ${PYTHON_SOURCE_DIRECTORY}

.ONESHELL:
.PHONY: pyupgrade
pyupgrade: venv
	source venv/bin/activate
	$(call check_install_status,pyupgrade)
	pyupgrade --py310-plus $(PYTHON_SOURCE_SCRIPTS)

## format
##     change codes for older versions (pyupgrade)
##     remove pyflake detected issues (autoflake)
##     sort imports (isort)
##     format docstrings (docformatter)
##     format code style (black)
.PHONY: format
format: pyupgrade autoflake isort docformatter blacken-docs black

.ONESHELL:
.PHONY: bandit
bandit: venv
	source venv/bin/activate
	$(call check_install_status,bandit)
	bandit \
    --recursive \
	--severity-level high \
	--confidence-level high \
	${PYTHON_SOURCE_DIRECTORY}

.ONESHELL:
.PHONY: flake8
flake8: venv
	source venv/bin/activate
	$(call check_install_status,flake8)
	flake8 \
	--extend-ignore E203 \
	--per-file-ignores __init__.py:F401 \
	--max-line-length 99 \
	${PYTHON_SOURCE_DIRECTORY}

.ONESHELL:
.PHONY: interrogate
interrogate: venv
	source venv/bin/activate
	$(call check_install_status,interrogate)
	interrogate ${PYTHON_SOURCE_DIRECTORY}

.ONESHELL:
.PHONY: pydocstyle
pydocstyle: venv
	source venv/bin/activate
	$(call check_install_status,pydocstyle)
	pydocstyle ${PYTHON_SOURCE_DIRECTORY}

.ONESHELL:
.PHONY: pylint
pylint: venv
	source venv/bin/activate
	$(call check_install_status,pylint)
	pylint ${PYTHON_SOURCE_DIRECTORY}

.ONESHELL:
.PHONY: vulture
vulture: venv
	source venv/bin/activate
	$(call check_install_status,vulture)
	vulture

## lint
##     find security issues (bandit)
##     lint all python scripts (flake8)
##     check docstring coverage (interrogate)
##     check docstring presence and formats (pydocstyle)
##     lint all python scripts (pylint)
##     find dead code (vulture)
.PHONY: lint
lint: bandit flake8 interrogate pydocstyle pylint vulture

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

## test
##     test doctests (pytest-doctest)
##     test successful operations (pytest-successful)
##     test failed operations (pytest-failure)
##     test other unit tests (pytest-others)
.PHONY: test
test: pytest-doctest pytest-successful pytest-failure pytest-others

.ONESHELL:
.PHONY: coverage-erase
coverage-erase: venv
	source venv/bin/activate
	$(call check_install_status,coverage)
	coverage erase

.ONESHELL:
.PHONY: coverage-html
coverage-html: venv
	source venv/bin/activate
	$(call check_install_status,coverage)
	coverage html

.ONESHELL:
.PHONY: coverage-report
coverage-report: venv
	source venv/bin/activate
	$(call check_install_status,coverage)
	coverage report

.ONESHELL:
.PHONY: coverage-run
coverage-run: venv
	source venv/bin/activate
	$(call check_install_status,coverage)
	$(call check_install_status,pytest)
	coverage run

.ONESHELL:
.PHONY: coverage-xml
coverage-xml: venv
	source venv/bin/activate
	$(call check_install_status,coverage)
	coverage xml

## coverage
##     test all doctests and unit tests (coverage-run)
##     create test coverage report (coverage-html)
##     delete collected coverage data (coverage-erase)
.PHONY: coverage
coverage: coverage-run coverage-report coverage-html coverage-xml coverage-erase

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
	$(call check_install_status,furo)
	$(call check_install_status,Sphinx)
	$(call check_install_status,sphinx-copybutton)
	sphinx-build \
	-b html \
	${PYTHON_DOCS_DIRECTORY}/source \
	${PYTHON_DOCS_DIRECTORY}/build

## docs
##     prepare documentation sources with directives (sphinx-source)
##     create HTML documentation from source files (sphinx-build)
.PHONY: docs
docs: sphinx-source sphinx-build

.ONESHELL:
.PHONY: build
build: venv
	source venv/bin/activate
	$(call check_install_status,build)
	python3 -m build --outdir ${PYTHON_DIST_DIRECTORY}

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

## release
##     create distribution files (build)
##     check package description (twine-check)
##     upload distribution files (twine-upload)
.PHONY: release
release: build twine-check twine-upload

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

## cleanup
##     delete all pycache directories and other cache files (clean-pycache)
##     delete all mypy cache (clean-mypy_cache)
##     delete all unit test cache (clean-pytest_cache)
##     delete all coverage results (clean-coverage)
.PHONY: cleanup
cleanup: clean-pycache clean-mypy_cache clean-pytest_cache clean-coverage

.ONESHELL:
.PHONY: mypy
mypy: venv
	source venv/bin/activate
	$(call check_install_status,mypy)
	mypy

.ONESHELL:
.PHONY: mypy-stubgen
mypy-stubgen: venv
	source venv/bin/activate
	$(call check_install_status,mypy)
	stubgen \
	--output typing-stubs-for-package-name-to-install-with \
	--package package_name_to_import_with \
	--module module_that_can_be_imported_directly \
	--module module_that_can_be_invoked_from_cli \
	--module module_that_can_invoke_gui_from_cli

.ONESHELL:
.PHONY: pyright
pyright: venv
	source venv/bin/activate
	$(call check_install_status,pyright)
	pyright

.ONESHELL:
.PHONY: pyright-stubs
pyright-stubs: venv
	source venv/bin/activate
	$(call check_install_status,pyright)
	pyright --createstub package_name_to_import_with
	pyright --createstub module_that_can_be_imported_directly
	pyright --createstub module_that_can_be_invoked_from_cli
	pyright --createstub module_that_can_invoke_gui_from_cli
