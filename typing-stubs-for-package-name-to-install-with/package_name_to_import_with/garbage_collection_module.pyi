import typing

FunctionType: typing.TypeAlias

def define_garbage_collection_decorator(
    function_to_be_decorated: FunctionType,
) -> FunctionType: ...
