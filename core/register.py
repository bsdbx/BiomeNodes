"""Main registration point for builtin bpy Classes."""
from ..util.core_utils import import_all_modules
from .class_register.icon_reg import RegisterIcon
from .class_register.operator_reg import RegisterOperators
from .class_register.prop_reg import RegisterPropertyGroups

modules = import_all_modules()

# Initialise register classes instances
register_operators = RegisterOperators(modules)
register_pgroups = RegisterPropertyGroups(modules)
register_icons = RegisterIcon(modules)


def reg() -> None:
    """1. Registers Operator Classes.

    2. Registers PropertyGroup Classes.
    """
    register_icons.register()
    register_operators.register()
    register_pgroups.register()


def unreg() -> None:
    """1. Unregisters PropertyGroup Classes.

    2. Unregisters Operator Classes.
    """
    register_pgroups.unregister()
    register_operators.unregister()
