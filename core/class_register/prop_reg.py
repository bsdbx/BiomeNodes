from typing import List

import bpy.types as bt
import bpy.props as bp

from bpy.utils import register_class, unregister_class

from ...util.core_utils import get_classes, CONSTANTS


class RegisterPropertyGroups():
    """`RegisterPropertyGroups` provides functional to easily register `bpy.types.PropertyGroup` Classes,\n
    It has a useful decorator to wrap `bpt.types.PropertyGroup` Classes where user can specify `bpy_struct` object and property attribute,\n

    :param modules: Name of the module for registrator to parse,\n
    :type modules: `typing.List[str]`.
    """

    def __init__(self,
                 modules: List[str]) -> None:
        self.property_groups = [get_classes(mod, bt.PropertyGroup) for mod in modules]

    def warnings(self) -> None:
        """Called on register,\n
        Warns about not decorated `bpy.types.PropertyGroup` Classes,\n

        :rtype: `None`,\n
        :return: Nothing.
        """

        for list_of_pg in self.property_groups:
            for pr_group in list_of_pg:
                if not hasattr(pr_group, "property_group_type") and not hasattr(pr_group, "property_group_attribute"):
                    print(f"{CONSTANTS.BColors.WARNING}Warning:",
                        "skipping registering", pr_group.__name__, "Class", CONSTANTS.BColors.ENDC)

    def assign_attributes(self) -> None:
        """Called on register,\n
        Automatically sets an attribute(decorator property) to a `bpy_struct` object(decorator property),\n

        :rtype: `None`,\n
        :return: Nothing.
        """

        for list_of_pg in self.property_groups:
            for pr_group in list_of_pg:
                # If was decorated
                if hasattr(pr_group, "property_group_type"):
                    setattr(pr_group.property_group_type, str(
                            pr_group.property_group_attribute), bp.PointerProperty(type=pr_group))

    def register(self) -> None:
        """Automatically registers Classes from input module,\n 
        Outputs warnings,\n

        :rtype: `None`,\n
        :return: Nothing.
        """

        self.warnings()

        # Firstly register, then assign attributes
        for list_of_pg in self.property_groups:
            for pr_group in list_of_pg:
                register_class(pr_group)
                print("Registered Class:", pr_group.__name__)

        self.assign_attributes()

    def unregister(self) -> None:
        """Automatically unregisters Classes from input module,\n

        :rtype: `None`,\n
        :return: Nothing.
        """

        # Firstly unregister, then remove attributes
        for list_of_pg in self.property_groups:
            for pr_group in reversed(list_of_pg):
                unregister_class(pr_group)
                print("Unregistered Class:", pr_group.__name__)
