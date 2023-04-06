# noqa: D100
import importlib
import inspect
import pkgutil
import sys
from abc import ABC  # noqa: H306
from collections.abc import Callable
from dataclasses import dataclass, field
from typing import TypeVar

_T = TypeVar('_T')  # noqa: WPS111


def get_classes(module_name: str, class_type: type[_T]) -> list[type[_T]]:
    """`get_classes` function returns the list of Classes of a specific type.

    Args:
        module_name (str): The name of the module.
        class_type (type[T]): The type of the class to get.

    Returns:
        list[type[T]]: List of classes of a specified type.
    """
    classes = sys.modules[module_name].__dict__.values()
    return [
        class_obj for class_obj in classes if inspect.isclass(class_obj) and class_type in class_obj.__bases__
    ]


def get_class_attrs(
    class_object: object,
    attribute_type: type[_T],
    predicate: Callable[[type[_T]], bool] | None = None,
) -> list[tuple[str, type[_T]]]:
    """`get_class_attrs` function returns the list of Class attributes of a specific type.

    Args:
        class_object (object): Class object to get attributes from.
        attribute_type (ClassAny): The type of the attribute to find.
        predicate (Callable[[ClassAny], bool] | None): Lambda function that supplied, \
        only members for which the predicate returns a true value are included.

    Returns:
        list[tuple[str, ClassAny]]: List of attributes of specified type of specified class.
    """
    members = inspect.getmembers(class_object, predicate)
    return [
        (name, attr) for name, attr in members if isinstance(getattr(class_object, name), attribute_type)
    ]


def list_all_modules_helper(package_name: str | None = None) -> list[str]:
    """`list_all_modules_helper` is a helper function that returns the list of module names of a specified package.

    Args:
        package_name (typing.Optional[str]): The name of the package, \
        if not specified will be extracted from the module name.

    Returns:
        list[str]: List of module names of a specified package.
    """
    if package_name is None:
        package_name = __name__.split('.', maxsplit=1)[0]

    module_names = []
    for module_info in pkgutil.walk_packages(importlib.import_module(package_name).__path__):
        # pylint: disable=consider-using-f-string
        module_name = '{package_name}.{module_name}'.format(
            package_name=package_name,
            module_name=module_info.name,
        )

        if module_info.ispkg:
            module_names += list_all_modules_helper(module_name)
        else:
            module_names.append(module_name)
    return module_names


def import_all_modules() -> list[str]:
    """`import_all_modules` function imports all necessary modules to prevent errors.

    Returns:
        list[str]: List of package's modules.
    """
    modules = list_all_modules_helper()

    # Importing the modules, some may be repeated but it's not a big problem
    _ = [importlib.import_module(module) for module in modules]

    return modules


@dataclass(frozen=True)
class CONSTANTS(ABC):
    """Dataclass that contains other dataclasses and constants."""

    # pylint: disable=invalid-name
    operator_flag_items: frozenset[str] = field(
        default_factory=lambda: frozenset(
            (
                'REGISTER',
                'UNDO',
                'UNDO_GROUPED',
                'BLOCKING',
                'MACRO',
                'GRAB_CURSOR',
                'GRAB_CURSOR_X',
                'GRAB_CURSOR_Y',
                'DEPENDS_ON_CURSOR',
                'PRESET',
                'INTERNAL',
            ),
        ),
    )

    # pylint: disable=invalid-name
    default_flag_items: set[int] | set[str] = field(
        default_factory=lambda: set(
            {
                'REGISTER',
                'UNDO',
            },
        ),
    )

    @dataclass(frozen=True)
    class BColors(ABC):
        """`BColors` class is a dataclass that stores terminal color codes.

        see this thread: \
        https://stackoverflow.com/questions/287871/how-do-i-print-colored-text-to-the-terminal?page=1&tab=scoredesc#tab-top.
        """

        warning = '\033[93m'
        info = '\033[34m'
        endc = '\033[0m'
