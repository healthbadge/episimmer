import importlib.util
from typing import Callable, Dict, List, Tuple, Union, ValuesView,ModuleType
from xmlrpc.client import Boolean

def module_from_file(module_name: Union[str, None], file_path: Union[str, None]) -> ModuleType:
    """
    This function creates a ModuleSpec instance based on the path to a file and obtains a module from the instance. This module is
    then loaded and returned.

    Args:
        module_name: Name of the module to be loaded.
        file_path: Location of the module.

    Returns:
        Loaded module.
    """
    spec = importlib.util.spec_from_file_location(module_name, file_path)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module
