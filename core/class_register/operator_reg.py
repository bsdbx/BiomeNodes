# noqa: D100
import logging
import re
from typing import Any, NamedTuple

import bpy.types as bt  # noqa: WPS301
from bpy.utils import register_class, unregister_class
from typing_extensions import Self

from ...util.core_utils import CONSTANTS, get_classes


class RegisterOperators():  # noqa: WPS306
    """`RegisterOperators` Class provides functional to automatically register `Operator` Classes.

    It automatically generates `bl_idname`, `bl_description` and optionally `bl_options`.
    It also warns user about not missing Class description or improper Class naming convention.

    Args:
        modules (list[str]): List of module names. Those modules will be parsed for Classes of `Operator` type.
        logger (Logger | None): Logger object that is going to be used to raise warnings.
    """

    class Helpers(NamedTuple):
        """`Helpers` Class is a nested Class of the `RegisterOperators` Class and a Subclass of `NamedTuple` Class.

        It provides methods for automatic generation of `bl_idname`, 'bl_description` and `bl_options` \
        for `Operator` Classes.
        """

        @staticmethod
        def bl_idname_helper(class_obj: type[bt.Operator]) -> str | Any:
            """`bl_idname_helper` is a helper function that automatically generates `bl_idname` for Operator Class.

            Args:
                class_obj (type[Operator]): Class for which `bl_idname` is going to be generated.

            Returns:
                str | Any: Ending of an ID, that is going to be used in `bl_label` generation.
            """
            if not getattr(class_obj, 'bl_idname', None):
                no_ot = class_obj.__name__.replace('OT_', '')  # Removing OT prefix

                # Idname
                id_end_index = no_ot.find('_')
                id_attr = no_ot[:id_end_index].lower()

                id_end = no_ot[id_end_index + 1:len(no_ot)]

                # PascalCase to snake_case
                id_end_modified = re.compile('(?<!^)(?=[A-Z])').sub('_', id_end).lower()

                class_obj.bl_idname = '.'.join([id_attr, id_end_modified])
                return id_end
            return class_obj.bl_idname.split('.')[-1].capitalize()

        @staticmethod
        def bl_label_helper(
            class_obj: type[bt.Operator],
            id_end: str,
        ) -> None:
            """`bl_label_helper` is a helper function that automatically generates `bl_label` for Operator Class.

            Args:
                class_obj (type[Operator]): Class for which `bl_idname` is going to be generated.
                id_end (str): Ending of an ID from `bl_idname_helper` method.
            """
            if not getattr(class_obj, 'bl_label', None):
                # Splitting PascalCase with spaces(e.g [Pascal, Case, Some, Other, Text])
                label = ' '.join(
                    re.sub(
                        '([A-Z][a-z]+)', r' \1', re.sub('([A-Z]+)', r' \1', id_end),
                    ).split(),
                )
                class_obj.bl_label = label

        @staticmethod
        def bl_options_helpers(  # noqa: WPS231
            class_obj: type[bt.Operator],
            logger: logging.Logger,
            constants: CONSTANTS,
        ) -> None:
            """`bl_options_helpers` is a helper function that automatically generates `bl_options` for Operator Class.

            Args:
                class_obj (type[Operator]): Class for which `bl_idname` is going to be generated.
                logger (Logger | None): Logger object that is going to be used to raise warnings.
                constants (CONSTANTS): Dataclass of constants.
            """
            if not getattr(class_obj, 'bl_options', None):
                if getattr(class_obj, 'bl_options_options', None):
                    if class_obj.bl_options_options is not None:
                        if (blo := set(class_obj.bl_options_options)).issubset(constants.operator_flag_items):
                            class_obj.bl_options = blo
                        else:
                            logger.warning("{warning}Not valid 'bl_options' argument in {class_name}.{endc}".format(
                                warning=constants.BColors.warning,
                                class_name=class_obj.__name__,
                                endc=constants.BColors.endc,
                            ),
                            )
                else:
                    try:  # pylint: disable=too-many-try-statements
                        if not isinstance(class_obj.bl_options_options, dict):
                            class_obj.bl_options = constants.default_flag_items
                    except AttributeError:
                        class_obj.bl_options = constants.default_flag_items

    def __init__(
        self: Self,
        modules: list[str],
        logger: logging.Logger | None = None,
    ) -> None:
        if logger is None:
            self.logger = logging.getLogger(__name__)
        else:
            self.logger = logger

        self.operators = [get_classes(mod, bt.Operator) for mod in modules]
        self.constants = CONSTANTS()

    def warnings(self: Self) -> None:
        """`warnings` function is used to warn user about missing description or 'OT' prefix in `Operator` Classes."""
        warning = self.constants.BColors.warning
        endc = self.constants.BColors.endc

        for list_of_operators in self.operators:
            for class_obj in list_of_operators:
                bl_description = getattr(class_obj, 'bl_description', '')
                description = getattr(class_obj, 'description', None)
                class_name = class_obj.__name__

                # If Operator is missing description
                if not any([bl_description, description]):
                    self.logger.warning('{warning}Missing description in {class_name} Operator.{endc}'.format(
                        warning=warning,
                        class_name=class_name,
                        endc=endc,
                    ),
                    )

                # If Operator's Class name doesn't start with OT
                if not class_name.startswith('OT'):
                    self.logger.warning("{warning}{class_name} does not contain 'OT' with prefix.{endc}".format(
                        warning=warning,
                        class_name=class_name,
                        endc=endc,
                    ),
                    )

    def generate_attributes(self: Self) -> None:
        """`generate_attributes` function generates `bl_idname`, `bl_label` and `bl_options` attributes."""
        helpers = self.Helpers

        for list_of_operators in self.operators:
            for class_obj in list_of_operators:
                # bl_idname attribute generation
                id_end = helpers.bl_idname_helper(class_obj)

                # bl_label attribute generation
                helpers.bl_label_helper(class_obj, id_end)

                # bl_options attribute generation
                helpers.bl_options_helpers(class_obj, self.logger, self.constants)

    def register(self: Self) -> None:
        """`register` function automatically registers `Operator` Classes, warns and generates attributes."""
        self.warnings()
        self.generate_attributes()

        for list_of_operators in self.operators:
            for class_obj in list_of_operators:
                register_class(class_obj)
                self.logger.info('{info}Registered Operator: {class_name}.{endc}'.format(
                    info=self.constants.BColors.info,
                    class_name=class_obj.__name__,
                    endc=self.constants.BColors.endc,
                ),
                )

    def unregister(self: Self) -> None:
        """`unregister` function automatically unregisters `Operator` Classes."""
        for list_of_operators in self.operators:
            for class_obj in reversed(list_of_operators):
                unregister_class(class_obj)
                self.logger.info('{info}Unregistered Operator: {class_name}.{endc}'.format(
                    info=self.constants.BColors.info,
                    class_name=class_obj.__name__,
                    endc=self.constants.BColors.endc,
                ),
                )
