"""Configure nox."""
import functools
import pathlib

import nox

PYTHON_DEFAULT_VERSION = "3.10"
PYTHON_VERSIONS = ["3.10", "3.11"]

SOURCE_DIRECTORY = pathlib.Path("src")
DIST_DIRECTORY = pathlib.Path("dist")
DOCS_DIRECTORY = pathlib.Path("docs")

PYTHON_SCRIPT_PATHS = SOURCE_DIRECTORY.glob("**/*.py")
PYTHON_SCRIPTS = [str(SCRIPT_PATH) for SCRIPT_PATH in PYTHON_SCRIPT_PATHS]

GENERAL_SESSION_DECORATOR = functools.partial(nox.session, venv_backend="conda", reuse_venv=True)

FORMAT_SESSION_DECORATOR = functools.partial(
    GENERAL_SESSION_DECORATOR, python=PYTHON_DEFAULT_VERSION, tags=["format"]
)
LINT_SESSION_DECORATOR = functools.partial(
    GENERAL_SESSION_DECORATOR, python=PYTHON_VERSIONS, tags=["lint"]
)
RELEASE_SESSION_DECORATOR = functools.partial(
    GENERAL_SESSION_DECORATOR, python=PYTHON_DEFAULT_VERSION, tags=["release"]
)


@FORMAT_SESSION_DECORATOR
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


@LINT_SESSION_DECORATOR
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


@FORMAT_SESSION_DECORATOR
def black(session: nox.Session) -> None:
    """Run black.

    Parameters
    ----------
    session : nox.Session
        nox Session object
    """
    session.install("black")

    session.run("black", "--line-length", "99", "--safe", *PYTHON_SCRIPTS)


@RELEASE_SESSION_DECORATOR
def build(session: nox.Session) -> None:
    """Run build."""
    session.install("build")

    session.run("python", "-m", "build", "--no-isolation")

    session.notify("twine")


@GENERAL_SESSION_DECORATOR(python=PYTHON_DEFAULT_VERSION, tags=["test"])
def coverage(session: nox.Session) -> None:
    """Run coverage.

    Parameters
    ----------
    session : nox.Session
        nox Session object
    """
    session.install("coverage[toml]")

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


@FORMAT_SESSION_DECORATOR
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


@LINT_SESSION_DECORATOR
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


@FORMAT_SESSION_DECORATOR
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


@LINT_SESSION_DECORATOR
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


@LINT_SESSION_DECORATOR
def pydocstyle(session: nox.Session) -> None:
    """Run pydocstyle.

    Parameters
    ----------
    session : nox.Session
        nox Session object
    """
    session.install("pydocstyle")

    session.run("pydocstyle", "--convention", "numpy", SOURCE_DIRECTORY)


@LINT_SESSION_DECORATOR
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
        "--disable",
        "import-error",
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


@GENERAL_SESSION_DECORATOR(python=PYTHON_VERSIONS, tags=["test"])
def pytest(session: nox.Session) -> None:
    """Run pytest.

    Parameters
    ----------
    session : nox.Session
        nox Session object
    """
    session.install("coverage[toml]", "pytest")

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


@FORMAT_SESSION_DECORATOR
def pyupgrade(session: nox.Session) -> None:
    """Run pyupgrade.

    Parameters
    ----------
    session : nox.Session
        nox Session object
    """
    session.install("pyupgrade")

    session.run("pyupgrade", "--py310-plus", *PYTHON_SCRIPTS)


@GENERAL_SESSION_DECORATOR(python=PYTHON_DEFAULT_VERSION, tags=["doc"])
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


@RELEASE_SESSION_DECORATOR
def twine(session: nox.Session) -> None:
    """Run twine."""
    session.install("twine")

    session.run("twine", "check", f"{DIST_DIRECTORY.name}/*")
    session.run(
        "twine", "upload", "--repository-url", "PACKAGE_REGISTRY", f"{DIST_DIRECTORY.name}/*"
    )


@LINT_SESSION_DECORATOR
def vulture(session: nox.Session) -> None:
    """Run vulture.

    Parameters
    ----------
    session : nox.Session
        nox Session object
    """
    session.install("vulture")

    session.run("vulture", "--min-confidence", "100", SOURCE_DIRECTORY)
