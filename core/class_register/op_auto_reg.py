from typing import List

import re

import bpy.types as bt
from bpy.utils import register_class, unregister_class

from ...util.core_utils import get_classes, CONSTANTS

class RegisterOperators():
    """`RegisterOperators` Class provides functional to automatically register `bpy.types.Operator` Classes,\n
    It automatically generates `bl_idname`, `bl_description` and optionally `bl_options` using decorator,\n
    It also warns user about not missing Class description or improper Class naming convention,\n

    :param modules: Name of the module for registrator to parse,\n
    :type modules: `typing.List[str]`.
    """

    def __init__(self,
                 modules: List[str]) -> None:
        self.operators = [get_classes(mod, bt.Operator) for mod in modules]

    def warnings(self) -> None:
        """Called on register,\n
        Warns about missing description(`bl_description` and `description` staticmethod),\n
        Warns about missing OT prefix(see Class naming convention: https://b3d.interplanety.org/en/class-naming-conventions-in-blender-2-8-python-api/),\n

        :rtype: `None`,\n
        :return: Nothing.
        """

        for list_of_operators in self.operators:
            for class_obj in list_of_operators:
                # If operator is missing description
                if not hasattr(class_obj, "bl_description") and not hasattr(class_obj, "description"):
                    print(f"{CONSTANTS.BColors.WARNING}Warning:",
                        "missing description in", class_obj.__name__, CONSTANTS.BColors.ENDC)
                # If operator doesn't start with OT
                if not class_obj.__name__.startswith("OT"):
                    print(f"{CONSTANTS.BColors.WARNING}Warning:", class_obj.__name__,
                        "does not contain 'OT' with prefix", CONSTANTS.BColors.ENDC)

    def generate_attributes(self) -> None:
        """Called on register,\n
        Generates `bl_idname`, `bl_label` and `bl_options` attributes,\n

        :rtype: `None`,\n
        :return: Nothing.
        """

        _CONSTANTS = CONSTANTS()

        for list_of_operators in self.operators:
            for class_obj in list_of_operators:
                # bl_idname attribute generation
                if not hasattr(class_obj, "bl_idname"):
                    no_ot = class_obj.__name__.replace(
                        'OT_', '')  # Removing OT suffix

                    # Idname
                    id_end_index = no_ot.find("_")
                    id_attr = no_ot[:id_end_index].lower()

                    id_end = no_ot[id_end_index + 1:len(no_ot)]

                    # Label
                    # Splitting PascalCase with spaces(e.g [Pascal, Case, Some, Other, Text])
                    label = " ".join(
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
                        if (blo := getattr(class_obj, "bl_options_options")).issubset(_CONSTANTS.OPERATOR_FLAG_ITEMS):
                            setattr(class_obj, "bl_options", blo)
                        else:  # Do not generate and print warning
                            print(f"{CONSTANTS.BColors.WARNING}Warning: not valid 'bl_options' argument in",
                                class_obj.__name__, CONSTANTS.BColors.ENDC)
                    else:  # If no parameters - generate default bl_options attribute
                        setattr(class_obj, "bl_options", CONSTANTS.DEFAULT_FLAG_ITEMS)

    def register(self) -> None:
        """Automatically registers Classes from input module,\n
        Outputs warnings and generates attributes,\n

        :rtype: `None`,\n
        :return: Nothing.
        """

        self.warnings()
        self.generate_attributes()

        # Register all classes
        for list_of_operators in self.operators:
            for class_obj in list_of_operators:
                register_class(class_obj)
                print("Registered Class:", class_obj.__name__)

    def unregister(self) -> None:
        """Automatically unregisters Classes from input module,\n

        :rtype: `None`,\n
        :return: Nothing.
        """

        # Unregister all classes
        for list_of_operators in self.operators:
            for class_obj in reversed(list_of_operators):
                unregister_class(class_obj)
                print("Unregistered Class:", class_obj.__name__)
