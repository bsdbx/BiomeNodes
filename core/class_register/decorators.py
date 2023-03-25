from typing import Type, Callable, Set

import bpy.types as bt


def register_property_group(bpy_struct: Type[bt.bpy_struct],
                            attribute: str) -> Callable[[Type[bt.PropertyGroup]], Type[bt.PropertyGroup]]:
    """Decorates `bpy.types.PropertyGroup` Class,\n
    If Class is decorated - it is going to be registered, otherwise - not(generated warning),\n

    :param bpy_struct: Subclass of `bpy.types.bpy_struct`,\n
    :type bpy_struct: `typing.Type[bpy.types.bpy_struct]`,\n

    :param attribute: Name of property that is going to be setted to `bpy_struct` param,\n
    :type attribute: `str`,\n

    :rtype: `typing.Callable[[typing.Type[bpy.types.PropertyGroup]], typing.Type[bpy.types.PropertyGroup]]`,\n
    :return: Wrapper function.
    """

    def decorator(cls: Type[bt.PropertyGroup]) -> Type[bt.PropertyGroup]:
        cls.property_group_type = bpy_struct
        cls.property_group_attribute = attribute
        return cls
    
    return decorator


def bl_options(options: Set[str] | None = None) -> Callable[[Type[bt.Operator]], Type[bt.Operator]]:
    """Decorates  `bpy.types.Operator` Class,\n
    If Class is decorated and 'options' argument is empty set - bl_options won't be generated,\n
    If Class is not decorated - bl_options will be generated,\n
    'options' parameter is optional, specifies custom set for bl_options generation,\n

    :param options: Set of `Operator Type Flag Items`: https://docs.blender.org/api/current/bpy_types_enum_items/operator_type_flag_items.html#rna-enum-operator-type-flag-items,\n
    :type options: `typing.Optional[typing.Set[str]]`,\n

    :rtype: `typing.Callable[[typing.Type[bpy.types.Operator]], typing.Type[bpy.types.Operator]]`,\n
    :return: Wrapper function.
    """

    def decorator(cls: Type[bt.Operator]) -> Type[bt.Operator]:
        if options == set() or options is None:
            cls.generate_bl_options = False
        else:
            cls.generate_bl_options = True
            cls.bl_options_options = options
        return cls
    
    return decorator
