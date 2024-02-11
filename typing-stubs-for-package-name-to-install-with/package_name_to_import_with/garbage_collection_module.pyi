import typing

__all__ = ["FunctionType", "define_garbage_collection_decorator"]

FunctionType: typing.TypeAlias

def define_garbage_collection_decorator(
    function_to_be_decorated: FunctionType,
) -> FunctionType: ...
