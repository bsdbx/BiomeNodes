# noqa: D100
from collections.abc import Callable

import bpy.types as bt  # noqa: WPS301


def register_property_group(
    bpy_struct: type[bt.bpy_struct],
    attribute: str,
) -> Callable[[type[bt.PropertyGroup]], type[bt.PropertyGroup]]:
    """`register_property_group` decorator is used to decorate `PropertyGroup` Classes.

    If Class is decorated - it is going to be registered, otherwise - not.

    Args:
        bpy_struct (type[bpy_struct]): Subclass of `bpy_struct` Class.
        attribute: (type[PropertyGroup]): Name of attribute(Property Group).

    Returns:
        Callable[type[PropertyGroup], type[PropertyGroup]]: Wrapper function with generated attributes.
    """

    def decorator(cls: type[bt.PropertyGroup]) -> type[bt.PropertyGroup]:
        cls.property_group_type = bpy_struct
        cls.property_group_attribute = attribute
        return cls

    return decorator


def bl_options(
    options: set[str] | dict[str, None] | None = None,
) -> Callable[[type[bt.Operator]], type[bt.Operator]]:
    """`bl_options` decorator is used to decorate `Operator` Classes.

    If Class is decorated and 'options' argument is empty set - `bl_options` won't be generated.
    If Class is not decorated or no parameters are specified - `bl_options` will be generated.

    Args:
        options (set[str] | dict[str, None] | None): Set of `Operator Type Flag Items`.

    Returns:
        Callable[[type[Operator]], type[Operator]]: Wrapper function.
    """

    def decorator(cls: type[bt.Operator]) -> type[bt.Operator]:
        cls.bl_options_options = options
        return cls

    return decorator
