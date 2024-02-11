"""Configure nox."""
import functools
import pathlib

import nox

PYTHON_DEFAULT_VERSION = "3.10"
PYTHON_VERSIONS = ["3.10", "3.11", "3.12"]

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
TEST_SESSION_DECORATOR = functools.partial(
    GENERAL_SESSION_DECORATOR, python=PYTHON_VERSIONS, tags=["test"]
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

    session.run("autoflake", *PYTHON_SCRIPTS)


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
        str(SOURCE_DIRECTORY),
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

    session.run("black", *PYTHON_SCRIPTS)


@FORMAT_SESSION_DECORATOR
def blacken_docs(session: nox.Session) -> None:
    """Run blacken-docs.

    Parameters
    ----------
    session : nox.Session
        nox Session object
    """
    session.install("blacken-docs")

    session.run("blacken-docs", *PYTHON_SCRIPTS)


@RELEASE_SESSION_DECORATOR
def build(session: nox.Session) -> None:
    """Run build.

    Parameters
    ----------
    session : nox.Session
        nox Session object
    """
    session.install("build", "wheel")

    session.run("python3", "-m", "build", "--outdir", f"{DIST_DIRECTORY.name}")

    session.notify("twine")


@TEST_SESSION_DECORATOR
def coverage(session: nox.Session) -> None:
    """Run coverage.

    Parameters
    ----------
    session : nox.Session
        nox Session object
    """
    session.install("coverage[toml]")

    session.run("coverage", "report")
    session.run("coverage", "html")
    session.run("coverage", "xml")


@FORMAT_SESSION_DECORATOR
def docformatter(session: nox.Session) -> None:
    """Run docformatter.

    Parameters
    ----------
    session : nox.Session
        nox Session object
    """
    session.install("docformatter[tomli]")

    session.run("docformatter", *PYTHON_SCRIPTS)


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

    session.run("isort", *PYTHON_SCRIPTS)


@LINT_SESSION_DECORATOR
def mypy(session: nox.Session) -> None:
    """Run mypy.

    Parameters
    ----------
    session : nox.Session
        nox Session object
    """
    session.install("mypy", "pydantic")

    session.run("mypy")


@GENERAL_SESSION_DECORATOR(python=PYTHON_DEFAULT_VERSION)
def pre_commit(session: nox.Session) -> None:
    """Run pre-commit.

    Parameters
    ----------
    session : nox.Session
        nox Session object
    """
    session.install("pre-commit")

    session.run(
        "pre-commit",
        "run",
        "--color",
        "always",
        "--verbose",
        "--all-files",
        "--hook-stage",
        "manual",
    )


@LINT_SESSION_DECORATOR
def pylint(session: nox.Session) -> None:
    """Run pylint.

    Parameters
    ----------
    session : nox.Session
        nox Session object
    """
    session.install("pylint")

    session.run("pylint", "--disable", "import-error", str(SOURCE_DIRECTORY))


@LINT_SESSION_DECORATOR
def pyright(session: nox.Session) -> None:
    """Run pyright.

    Parameters
    ----------
    session : nox.Session
        nox Session object
    """
    session.install("pyright")

    session.run("pyright")


@TEST_SESSION_DECORATOR
def pytest(session: nox.Session) -> None:
    """Run pytest.

    Parameters
    ----------
    session : nox.Session
        nox Session object
    """
    session.install("-e", ".[test]")

    session.run("coverage", "run")

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


@GENERAL_SESSION_DECORATOR(python=PYTHON_DEFAULT_VERSION)
def sphinx(session: nox.Session) -> None:
    """Run sphinx.

    Parameters
    ----------
    session : nox.Session
        nox Session object
    """
    session.install("-e", ".[doc]")

    with session.chdir("docs"):
        session.run("sphinx-build", "-b", "html", "source", "build")


@RELEASE_SESSION_DECORATOR
def twine(session: nox.Session) -> None:
    """Run twine.

    Parameters
    ----------
    session : nox.Session
        nox Session object
    """
    session.install("twine")

    session.run("twine", "check", f"{DIST_DIRECTORY.name}/*")
    session.run("twine", "upload", f"{DIST_DIRECTORY.name}/*")


@LINT_SESSION_DECORATOR
def vulture(session: nox.Session) -> None:
    """Run vulture.

    Parameters
    ----------
    session : nox.Session
        nox Session object
    """
    session.install("vulture")

    session.run("vulture")
