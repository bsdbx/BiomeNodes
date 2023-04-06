from pathlib import Path
from dataclasses import dataclass
from typing_extensions import Self

import bpy.types as bt

from ...util.core_utils import (get_classes,
                                get_class_attrs,
                                CONSTANTS)


class IconProperty():  # pylint: disable=too-few-public-methods
    def __init__(self: Self,
                 name: str,
                 path: str | Path) -> None:
        self.name = name
        self.path = path


@dataclass()
class IconGroup():
    bn_preview_collection: list[type[bt.ImagePreview]]


@dataclass()
class Icons(IconGroup):
    bn_preview_collection = []
    qqoqoqoq = str()
    icon1 = IconProperty("my_icon", ".")


class RegisterIcon():
    def __init__(self: Self,
                 modules: list[str]) -> None:
        self.icon_groups = [get_classes(mod, IconGroup) for mod in modules]

    def register(self: Self) -> None:
        for icon_groups in self.icon_groups:
            for icon_group in icon_groups:
                if hasattr(icon_group, "bn_preview_collection"):
                    try:
                        prev_col_type = getattr(IconGroup, "bn_preview_collection")
                    except AttributeError:
                        setattr(IconGroup, "bn_preview_collection", [])
                        prev_col_type = getattr(IconGroup, "bn_preview_collection")
                    if isinstance(ig_col := icon_group.bn_preview_collection, col_type := type(prev_col_type)):
                        print(get_class_attrs(icon_group, IconProperty))
                    else:
                        print(f"{CONSTANTS.BColors.WARNING}Warning: 'bn_preview_collection' attribute in object \
                              {icon_group} has invalid type. Get: {type(ig_col)}, Expected: \
                              {col_type}.{CONSTANTS.BColors.ENDC}")
                else:
                    print(f"{CONSTANTS.BColors.WARNING}Warning: \
                          {icon_group.__name__} object has no attribute 'bn_preview_collection', \
                          skipping register.{CONSTANTS.BColors.ENDC}")
