import collections.abc
import typing

def define_garbage_collection_decorator(function_to_be_decorated: collections.abc.Callable[..., typing.Any]) -> collections.abc.Callable[..., typing.Any]: ...
