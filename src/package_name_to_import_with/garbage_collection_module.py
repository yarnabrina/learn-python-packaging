"""Define package contents."""
import functools
import gc
import typing


def define_garbage_collection_decorator(
    function_to_be_decorated: typing.Callable[..., typing.Any]
) -> typing.Callable[..., typing.Any]:
    """Perform forcefully garbage collection after execution of provided function.

    Parameters
    ----------
    function_to_be_decorated : typing.Callable[..., typing.Any]
        function whose execution may require forceful garbage collection

    Returns
    -------
    typing.Callable[..., typing.Any]
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