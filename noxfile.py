"""Configure nox."""
import pathlib

import nox

nox.options.default_venv_backend = "conda"
nox.options.reuse_existing_virtualenvs = True

PYTHON_DEFAULT_VERSION = "3.10"
PYTHON_VERSIONS = ["3.10", "3.11"]

SOURCE_DIRECTORY = pathlib.Path("src")
DIST_DIRECTORY = pathlib.Path("dist")
DOCS_DIRECTORY = pathlib.Path("docs")

PYTHON_SCRIPTS = SOURCE_DIRECTORY.glob("**/*.py")


@nox.session(python=PYTHON_DEFAULT_VERSION, tags=["format"])
def autoflake(session: nox.Session) -> None:
    """Run autoflake.

    Parameters
    ----------
    session : nox.Session
        nox Session object
    """
    session.install("autoflake")

    session.run(
        "autoflake",
        "--in-place",
        "--remove-all-unused-imports",
        "--expand-star-imports",
        "--ignore-init-module-imports",
        "--remove-duplicate-keys",
        "--remove-unused-variables",
        *PYTHON_SCRIPTS,
    )


@nox.session(python=PYTHON_DEFAULT_VERSION, tags=["lint"])
def bandit(session: nox.Session) -> None:
    """Run bandit.

    Parameters
    ----------
    session : nox.Session
        nox Session object
    """
    session.install("bandit")

    session.run(
        "bandit",
        "--recursive",
        "--severity-level",
        "high",
        "--confidence-level",
        "high",
        SOURCE_DIRECTORY,
    )


@nox.session(python=PYTHON_DEFAULT_VERSION, tags=["format"])
def black(session: nox.Session) -> None:
    """Run black.

    Parameters
    ----------
    session : nox.Session
        nox Session object
    """
    session.install("black")

    session.run("black", "--line-length", "99", "--safe", *PYTHON_SCRIPTS)


@nox.session(python=PYTHON_DEFAULT_VERSION, tags=["release"])
def build(session: nox.Session) -> None:
    """Run build."""
    session.install("build")

    session.run("python", "-m", "build", "--no-isolation")

    session.notify("twine")


@nox.session(python=PYTHON_DEFAULT_VERSION, tags=["test"])
def coverage(session: nox.Session) -> None:
    """Run coverage.

    Parameters
    ----------
    session : nox.Session
        nox Session object
    """
    session.install("coverage")

    session.run(
        "coverage",
        "report",
        "--fail-under",
        "80",
        "--include",
        f"{SOURCE_DIRECTORY.name}/**/*.py",
        "--omit",
        "**/tests/*.py",
        "--precision",
        "2",
    )


@nox.session(python=PYTHON_DEFAULT_VERSION, tags=["format"])
def docformatter(session: nox.Session) -> None:
    """Run docformatter.

    Parameters
    ----------
    session : nox.Session
        nox Session object
    """
    session.install("docformatter")

    session.run(
        "docformatter",
        "--in-place",
        "--wrap-summaries",
        "99",
        "--wrap-description",
        "99",
        *PYTHON_SCRIPTS,
    )


@nox.session(python=PYTHON_DEFAULT_VERSION, tags=["lint"])
def flake8(session: nox.Session) -> None:
    """Run flake8.

    Parameters
    ----------
    session : nox.Session
        nox Session object
    """
    session.install("flake8")

    session.run(
        "flake8",
        "--extend-ignore",
        "E203",
        "--per-file-ignores",
        "__init__.py:F401",
        "--max-line-length",
        "99",
        *PYTHON_SCRIPTS,
    )


@nox.session(python=PYTHON_DEFAULT_VERSION, tags=["format"])
def isort(session: nox.Session) -> None:
    """Run isort.

    Parameters
    ----------
    session : nox.Session
        nox Session object
    """
    session.install("isort")

    session.run(
        "isort",
        "--overwrite-in-place",
        "--profile",
        "black",
        "--atomic",
        "--float-to-top",
        "--line-length",
        "99",
        "--remove-redundant-aliases",
        *PYTHON_SCRIPTS,
    )


@nox.session(python=PYTHON_DEFAULT_VERSION, tags=["lint"])
def mypy(session: nox.Session) -> None:
    """Run mypy.

    Parameters
    ----------
    session : nox.Session
        nox Session object
    """
    session.install("mypy")

    session.run(
        "mypy",
        "--ignore-missing-imports",
        "--strict",
        "--exclude",
        "conftest",
        "--exclude",
        "test_",
        SOURCE_DIRECTORY,
    )


@nox.session(python=PYTHON_DEFAULT_VERSION, tags=["lint"])
def pydocstyle(session: nox.Session) -> None:
    """Run pydocstyle.

    Parameters
    ----------
    session : nox.Session
        nox Session object
    """
    session.install("pydocstyle")

    session.run("pydocstyle", "--convention", "numpy", SOURCE_DIRECTORY)


@nox.session(python=PYTHON_DEFAULT_VERSION, tags=["lint"])
def pylint(session: nox.Session) -> None:
    """Run pylint.

    Parameters
    ----------
    session : nox.Session
        nox Session object
    """
    session.install("pylint")

    session.run(
        "pylint",
        "--enable-all-extensions",
        "--persistent",
        "no",
        "--suggestion-mode",
        "yes",
        "--exit-zero",
        "no",
        "--recursive",
        "yes",
        "--output-format",
        "colorized",
        "--reports",
        "no",
        "--score",
        "yes",
        "--enable",
        "all",
        "--logging-format-style",
        "new",
        "--init-import",
        "no",
        "--allow-global-unused-variables",
        "yes",
        "--max-line-length",
        "99",
        "--ignore-comments",
        "yes",
        "--ignore-docstrings",
        "yes",
        "--ignore-imports",
        "yes",
        "--ignore-signatures",
        "yes",
        SOURCE_DIRECTORY,
    )


@nox.session(python=PYTHON_DEFAULT_VERSION, tags=["test"])
def pytest(session: nox.Session) -> None:
    """Run pytest.

    Parameters
    ----------
    session : nox.Session
        nox Session object
    """
    session.install("coverage", "pytest")

    session.run(
        "coverage",
        "run",
        "--branch",
        "--include",
        f"{SOURCE_DIRECTORY.name}/**/*.py",
        "--omit",
        "**/tests/*.py",
        "--module",
        "pytest",
        "--doctest-modules",
        "--doctest-ignore-import-errors",
        "--doctest-continue-on-failure",
    )

    session.notify("coverage")


@nox.session(python=PYTHON_DEFAULT_VERSION, tags=["format"])
def pyupgrade(session: nox.Session) -> None:
    """Run pyupgrade.

    Parameters
    ----------
    session : nox.Session
        nox Session object
    """
    session.install("pyupgrade")

    session.run("pyupgrade", "--py310-plus", *PYTHON_SCRIPTS)


@nox.session(python=PYTHON_DEFAULT_VERSION, tags=["doc"])
def sphinx(session: nox.Session) -> None:
    """Run sphinx.

    Parameters
    ----------
    session : nox.Session
        nox Session object
    """
    session.install("Sphinx", "sphinx-copybutton", "sphinx-rtd-theme")

    with session.chdir("docs"):
        session.run("sphinx-build", "-b", "html", "source", "build")


@nox.session(python=PYTHON_DEFAULT_VERSION, tags=["release"])
def twine(session: nox.Session) -> None:
    """Run twine."""
    session.install("twine")

    session.run("twine", "check", f"{DIST_DIRECTORY.name}/*")
    session.run(
        "twine", "upload", "--repository-url", "PACKAGE_REGISTRY", f"{DIST_DIRECTORY.name}/*"
    )


@nox.session(python=PYTHON_DEFAULT_VERSION, tags=["lint"])
def vulture(session: nox.Session) -> None:
    """Run vulture.

    Parameters
    ----------
    session : nox.Session
        nox Session object
    """
    session.install("vulture")

    session.run("vulture", "--min-confidence", "100", SOURCE_DIRECTORY)
