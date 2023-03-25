from typing import Callable, Type, List, Iterator, FrozenSet
from types import ModuleType

from dataclasses import dataclass, field

import importlib
import pkgutil
import sys
import inspect

import bpy.types as bt

get_classes: Callable[[str, Type[bt.bpy_struct]],
                      List[Type[bt.bpy_struct]]] = lambda module_name, \
                                                           _type: list(filter(lambda obj: inspect.isclass(obj)
                                                                             and issubclass(obj, _type)
                                                                             and obj.__module__ == module_name,
                                                                             sys.modules[module_name].__dict__.values()))
get_classes.__doc__ = """Used to get all classes of a specific type,\n
                      
                      :param module_name: The name of the module,\n
                      :type module_name: `str`,\n

                      :param _type: The type of the class to get,\n
                      :type _type: `typing.Type[bpy.types.bpy_struct]`,\n

                      :rtype: `typing.List[Type[bpy.types.bpy_struct]]`,\n
                      :return List of classes of a specific type.
                      """


def import_all_modules() -> List[str]:
    """Imports all necessary modules to prevent errors,\n
    
    :rtype: `typing.List[str]`, \n
    :return List of package's modules.
    """

    # Finding all modules from a package recursively
    list_all_modules: Callable[
        [str, Callable[[str], Iterator[ModuleType]]], List[str]
    ] = lambda package, modules: \
    [
        package + "." + module_info.name
        for module_info in (modules(package))
        if not module_info.ispkg
    ] + \
    [
        module for sub_package_name in 
        [
            package + "." + module_info.name
            for module_info in modules(package)
            if module_info.ispkg
        ]
        for module in list_all_modules(sub_package_name, modules)
    ]

    modules = list_all_modules(__name__.split(".", maxsplit=1)[0], 
                               lambda _package: pkgutil.walk_packages([__import__(_package, fromlist=["dummy"]).__path__[0]]))
    
    [importlib.import_module(module) for module in modules]  # Importing the modules, some may be repeated but it's not a big problem

    return modules


@dataclass(frozen=True)
class CONSTANTS:
    OPERATOR_FLAG_ITEMS: FrozenSet[str] = field(default_factory=lambda: frozenset({"REGISTER", 
                                                                                   "UNDO", 
                                                                                   "UNDO_GROUPED", 
                                                                                   "BLOCKING", 
                                                                                   "MACRO", 
                                                                                   "GRAB_CURSOR", 
                                                                                   "GRAB_CURSOR_X", 
                                                                                   "GRAB_CURSOR_Y",
                                                                                   "DEPENDS_ON_CURSOR", 
                                                                                   "PRESET", 
                                                                                   "INTERNAL"}))
    
    DEFAULT_FLAG_ITEMS: FrozenSet[str] = field(default_factory=lambda: frozenset({"REGISTER",
                                                                                  "UNDO"}))

    @dataclass(frozen=True)
    class BColors:
        """Constant warning variables for colored warning output,\n
        see this thread: https://stackoverflow.com/questions/287871/how-do-i-print-colored-text-to-the-terminal?page=1&tab=scoredesc#tab-top.
        """

        WARNING = "\033[93m"
        ENDC = "\033[0m"
