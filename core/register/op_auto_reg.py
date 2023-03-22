import bpy.types as bt

import sys, inspect, re
from typing import Type, Callable, List

class AutoRegisterOperators():
    def __init__(self, module_name: str) -> None:
        self.operators: Type[bt.Operator]
        self.label:     str

        self.get_classes: Callable[[str, bt.bpy_struct], List[bt.bpy_struct]] = lambda module_name, type: list(filter(lambda obj: 
                                                                                                                            inspect.isclass(obj) and issubclass(obj, type), 
                                                                                                                            sys.modules[module_name].__dict__.values()))
        
        self.operators = self.get_classes(module_name, bt.Operator)


    class bcolors:
        WARNING = "\033[93m"
        ENDC    = "\033[0m"

    
    def warnings(self) -> None:
        """Called on register,\n
        Warns about missing description(bl_description and staticmethod one),\n
        Warns about missing OT prefix(see class naming convention: https://b3d.interplanety.org/en/class-naming-conventions-in-blender-2-8-python-api/).
        """

        for c in self.operators:
            if not hasattr(c, "bl_description") and not hasattr(c, "description"):
                print(f"{self.bcolors.WARNING}Warning:", "missing description in", c.__name__, self.bcolors.ENDC)
            if not c.__name__.startswith("OT"):
                print(f"{self.bcolors.WARNING}Warning:", c.__name__, "does not contain 'OT' with prefix", self.bcolors.ENDC)

    
    def generate_attributes(self) -> None:
        """Called on register.\n
        Generates bl_idname, bl_label and bl_options attributes.
        """

        for c in self.operators:
            if not hasattr(c, "bl_idname"):
                no_ot = c.__name__.replace('OT_', '') # Removing OT suffix

                # Idname
                id_end_index = no_ot.find('_')
                id_attr = no_ot[0 : id_end_index].lower()

                id_end = no_ot[id_end_index + 1 : len(no_ot)]

                # Label
                label = ' '.join(re.sub('([A-Z][a-z]+)', r' \1', re.sub('([A-Z]+)', r' \1', id_end)).split()) # Splitting PascalCase with spaces(e.g [Pascal, Case, Some, Other, Text])

                id_end = re.compile(r'(?<!^)(?=[A-Z])').sub('_', id_end).lower() # PascalCase to camel_case

                setattr(c, "bl_idname", ".".join([id_attr, id_end]))

            if not hasattr(c, "bl_label"):
                setattr(c, "bl_label", label)

            if getattr(c, "generate_bl_options", True) and not hasattr(c, "bl_options"):
                if hasattr(c, "bl_options_options"):
                    if (blo := getattr(c, "bl_options_options")).issubset({'REGISTER', 'UNDO', 'UNDO_GROUPED', 'BLOCKING', 'MACRO', 'GRAB_CURSOR', 'GRAB_CURSOR_X', 'GRAB_CURSOR_Y', 'DEPENDS_ON_CURSOR', 'PRESET', 'INTERNAL'}):
                        setattr(c, "bl_options", blo)
                    else:
                        print(f"{self.bcolors.WARNING}Warning: not valid 'bl_options' argument in", c.__name__, self.bcolors.ENDC)
                else:
                    setattr(c, "bl_options", {'REGISTER', 'UNDO'})


    def not_generate_bl_options(options: set[str] = {}) -> Type[bt.Operator]:
        """Decorates  'bpy.types.Operator' class,\n
        If class is decorated and 'options' argument is empty set - bl_options won't be generated,\n
        If class is not decorated - bl_options will be generated,\n
        'options' parameter is optional, specifies custom set for bl_options generation.
        """

        def decorator(cls: Type[bt.Operator]) -> Type[bt.Operator]:
            if options == {}:
                cls.generate_bl_options = False
            else:
                cls.generate_bl_options = True
                cls.bl_options_options  = options
            return cls
        return decorator     
                                                                                                                        
        
    def auto_register(self) -> None:
        """Automatically registers classes from input module,\n
        Outputs warnings and generates attributes.
        """

        from bpy.utils import register_class

        self.warnings()
        self.generate_attributes()

        for c in self.operators:
            register_class(c)
            print('Registered class:', c.__name__)

    def auto_unregister(self) -> None:
        """Automatically unregisters classes from input module"""

        from bpy.utils import unregister_class
        
        for c in reversed(self.operators):
            unregister_class(c)
            print('Unregistered class:', c.__name__)