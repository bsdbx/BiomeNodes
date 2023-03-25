""" Main registration point for builtin bpy Classes """

from ..util.core_utils import import_all_modules

from .class_register.prop_reg import RegisterPropertyGroups as RPG
from .class_register.op_auto_reg import RegisterOperators as RO

modules = import_all_modules()

# Initialise register classes instances
ro = RO(modules)
rpg = RPG(modules)


def reg() -> None:
    """1. Registers Operator Classes,\n
    2. Registers PropertyGroup Classes,\n

    :rtype: None,\n
    :return: Nothing.
    """

    ro.register()
    rpg.register()


def unreg() -> None:
    """1. Unregisters PropertyGroup Classes,\n
    2. Unregisters Operator Classes.
    
    :rtype: None,\n
    :return: Nothing.
    """

    rpg.unregister()
    ro.unregister()
