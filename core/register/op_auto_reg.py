"""'op_auto_reg' is a Python module for auto registration of Operator Class,\n
It provides user with handy 'AutoRegisterOperators' Class.
"""

from typing import Type, Callable, List, Set
from dataclasses import dataclass

import sys
import inspect
import re

import bpy.types as bt
from bpy.utils import register_class, unregister_class


class AutoRegisterOperators():
    """AutoRegisterOperators class provides functional to automatically register Operator classes,\n
    It automatically generates 'bl_idname', 'bl_description' and optionally 'bl_options' using decorator,\n
    It also warns user about not missing class description or proper Class naming convention.
    """

    def __init__(self,
                 module_name: str) -> None:
        self.operators: List[Type[bt.bpy_struct]]
        self.get_classes: Callable[[str, Type[bt.bpy_struct]], List[Type[bt.bpy_struct]]] = lambda module_name, type: list(filter(lambda obj: inspect.isclass(obj)
                                                                                                                                  and issubclass(obj, type),
                                                                                                                                  sys.modules[module_name].__dict__.values()))

        self.operators = self.get_classes(module_name, bt.Operator)

    @dataclass(frozen=True)
    class BColors:
        """Constant warning variables for colored warning output,\n
        see this thread: https://stackoverflow.com/questions/287871/how-do-i-print-colored-text-to-the-terminal?page=1&tab=scoredesc#tab-top 
        """
        WARNING = "\033[93m"
        ENDC = "\033[0m"

    def warnings(self) -> None:
        """Called on register,\n
        Warns about missing description(bl_description and staticmethod one),\n
        Warns about missing OT prefix(see Class naming convention: https://b3d.interplanety.org/en/class-naming-conventions-in-blender-2-8-python-api/).
        """

        for class_obj in self.operators:
            # If operator is missing description
            if not hasattr(class_obj, "bl_description") and not hasattr(class_obj, "description"):
                print(f"{self.BColors.WARNING}Warning:",
                      "missing description in", class_obj.__name__, self.BColors.ENDC)
            # If operator doesn't start with OT
            if not class_obj.__name__.startswith("OT"):
                print(f"{self.BColors.WARNING}Warning:", class_obj.__name__,
                      "does not contain 'OT' with prefix", self.BColors.ENDC)

    def generate_attributes(self) -> None:
        """Called on register,\n
        Generates bl_idname, bl_label and bl_options attributes.
        """

        for class_obj in self.operators:
            # bl_idname attribute generation
            if not hasattr(class_obj, "bl_idname"):
                no_ot = class_obj.__name__.replace(
                    'OT_', '')  # Removing OT suffix

                # Idname
                id_end_index = no_ot.find('_')
                id_attr = no_ot[0:id_end_index].lower()

                id_end = no_ot[id_end_index + 1:len(no_ot)]

                # Label
                # Splitting PascalCase with spaces(e.g [Pascal, Case, Some, Other, Text])
                label = ' '.join(
                    re.sub("([A-Z][a-z]+)", r" \1", re.sub("([A-Z]+)", r" \1", id_end)).split())

                # PascalCase to camel_case
                id_end = re.compile(
                    r"(?<!^)(?=[A-Z])").sub("_", id_end).lower()

                setattr(class_obj, "bl_idname", ".".join([id_attr, id_end]))

            # bl_label attribute generation
            if not hasattr(class_obj, "bl_label"):
                setattr(class_obj, "bl_label", label)

            # bl_options attribute generation
            # If function is not decorated
            if getattr(class_obj, "generate_bl_options", True) and not hasattr(class_obj, "bl_options"):
                # If function is decorated and has parameters
                if hasattr(class_obj, "bl_options_options"):
                    # If bl_options parameter is not valid
                    if (blo := getattr(class_obj, "bl_options_options")).issubset({'REGISTER', 'UNDO', 'UNDO_GROUPED', 'BLOCKING', 'MACRO', 'GRAB_CURSOR', 'GRAB_CURSOR_X', 'GRAB_CURSOR_Y', 'DEPENDS_ON_CURSOR', 'PRESET', 'INTERNAL'}):
                        setattr(class_obj, "bl_options", blo)
                    else:  # Do not generate and print warning
                        print(f"{self.BColors.WARNING}Warning: not valid 'bl_options' argument in",
                              class_obj.__name__, self.BColors.ENDC)
                else:  # If no parameters - generate default bl_options attribute
                    setattr(class_obj, "bl_options", {'REGISTER', 'UNDO'})

    @staticmethod
    def not_generate_bl_options(options: Set[str] | None = None) -> Callable[[Type[bt.Operator]], Type[bt.Operator]]:
        """Decorates  'bpy.types.Operator' class,\n
        If class is decorated and 'options' argument is empty set - bl_options won't be generated,\n
        If class is not decorated - bl_options will be generated,\n
        'options' parameter is optional, specifies custom set for bl_options generation.
        """

        def decorator(cls: Type[bt.Operator]) -> Type[bt.Operator]:
            if options == set() or options == None:
                cls.generate_bl_options = False
            else:
                cls.generate_bl_options = True
                cls.bl_options_options = options
            return cls
        return decorator

    def auto_register(self) -> None:
        """Automatically registers classes from input module,\n
        Outputs warnings and generates attributes.
        """

        self.warnings()
        self.generate_attributes()

        # Register all classes
        for class_obj in self.operators:
            register_class(class_obj)
            print('Registered class:', class_obj.__name__)

    def auto_unregister(self) -> None:
        """Automatically unregisters classes from input module"""

        # Unregister all classes
        for class_obj in reversed(self.operators):
            unregister_class(class_obj)
            print('Unregistered class:', class_obj.__name__)
