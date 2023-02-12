"""Define package contents."""
import functools
import gc
import typing

if typing.TYPE_CHECKING:
    import collections.abc


def define_garbage_collection_decorator(
    function_to_be_decorated: "collections.abc.Callable[..., typing.Any]",
) -> "collections.abc.Callable[..., typing.Any]":  # pragma: no cover
    """Perform forcefully garbage collection after execution of provided function.

    Parameters
    ----------
    function_to_be_decorated : collections.abc.Callable[..., typing.Any]
        function whose execution may require forceful garbage collection

    Returns
    -------
    collections.abc.Callable[..., typing.Any]
        decorated function
    """

    @functools.wraps(function_to_be_decorated)
    def wrapper_function(*args: typing.Any, **kwargs: typing.Any) -> typing.Any:
        """Execute provided function with forceful garbage collection afterwards.

        Returns
        -------
        typing.Any
            output of the provided function with provided arguments
        """
        result = function_to_be_decorated(*args, **kwargs)
        _ = gc.collect()

        return result

    return wrapper_function
