# noqa: D100
import logging

import bpy.props as bp  # noqa: WPS301
import bpy.types as bt  # noqa: WPS301
from bpy.utils import register_class, unregister_class
from typing_extensions import Self

from ...util.core_utils import CONSTANTS, get_classes


class RegisterPropertyGroups():  # noqa: WPS306
    """`RegisterPropertyGroups` provides functional to easily register `PropertyGroup` Classes.

    It has a useful decorator to wrap `PropertyGroup` Classes,
    where user can specify `bpy_struct` object and property attribute.

    Args:
        modules (list[str]): list of names of modules to take in account when registering.
        logger (Logger | None): Logger object to use for Info and Warnings output.
    """

    def __init__(
        self: Self,
        modules: list[str],
        logger: logging.Logger | None = None,
    ) -> None:
        if logger is None:
            self.logger = logging.getLogger(__name__)
        else:
            self.logger = logger

        self.property_groups = [get_classes(mod, bt.PropertyGroup) for mod in modules]
        self.constants = CONSTANTS()

    def warnings(self: Self) -> None:
        """`warnings` function is used to warn user about not decorated `PropertyGroup` Classes."""
        for list_of_pg in self.property_groups:
            for pr_group in list_of_pg:
                property_group_type = getattr(pr_group, 'property_group_type', None)
                property_group_attribute = getattr(pr_group, 'property_group_attribute', None)

                if not all([property_group_type, property_group_attribute]):
                    self.logger.warning('{warning}Skipping registering {class_name} Class.{endc}'.format(
                        warning=self.constants.BColors.warning,
                        class_name=pr_group.__name__,
                        endc=self.constants.BColors.endc,
                    ),
                    )

    def assign_attributes(self: Self) -> None:
        """`assign_attributes` is called on register.

        Automatically sets an attribute(decorator property) to a `bpy_struct` object(decorator property).
        """
        for list_of_pg in self.property_groups:
            for pr_group in list_of_pg:
                property_group_attribute = getattr(pr_group, 'property_group_attribute', None)
                property_group_type = getattr(pr_group, 'property_group_type', None)

                if all([property_group_attribute, property_group_type]):
                    setattr(
                        pr_group.property_group_type,
                        str(pr_group.property_group_attribute),
                        bp.PointerProperty(type=pr_group),
                    )

    def register(self: Self) -> None:
        """`register` function automatically registers `PropertyGroups` Classes."""
        self.warnings()

        for list_of_pg in self.property_groups:
            for pr_group in list_of_pg:
                register_class(pr_group)
                self.logger.info('{info}Registered Property Group: {class_name}.{endc}'.format(
                    info=self.constants.BColors.info,
                    class_name=pr_group.__name__,
                    endc=self.constants.BColors.endc,
                ),
                )

        self.assign_attributes()

    def unregister(self: Self) -> None:
        """`unregister` function automatically unregisters `PropertyGroups` Classes."""
        for list_of_pg in self.property_groups:
            for pr_group in reversed(list_of_pg):
                unregister_class(pr_group)
                self.logger.info('{info}Unregistered Property Group: {class_name}.{endc}'.format(
                    info=self.constants.BColors.info,
                    class_name=pr_group.__name__,
                    endc=self.constants.BColors.endc,
                ),
                )
