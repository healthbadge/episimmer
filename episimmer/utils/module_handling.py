import importlib.util
import os.path as osp
from types import ModuleType
from typing import TYPE_CHECKING, List

if TYPE_CHECKING:
    from episimmer.model import BaseModel
    from episimmer.policy.base import Policy


def module_from_file(module_name: str, file_path: str) -> ModuleType:
    """
    Returns the module from the file passed

    Args:
        module_name: Name of module
        file_path: Path to file used to create module

    Returns:
        Module of file

    """
    spec = importlib.util.spec_from_file_location(module_name, file_path)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def get_model(example_path: str) -> 'BaseModel':
    """
    Instantiates and returns the disease model object created in the UserModel.py file

    Args:
        example_path: Path to directory containing simulation files

    Returns:
        Disease Model object
    """
    user_model = module_from_file('Generate_model',
                                  osp.join(example_path, 'UserModel.py'))
    model = user_model.UserModel()
    return model


def get_policy(example_path: str) -> List['Policy']:
    """
    Returns the policy list created in the Generate_policy.py file

    Args:
        example_path: Path to directory containing simulation files

    Returns:
       Policy list to be run during simulation
    """
    generate_policy = module_from_file(
        'Generate_policy', osp.join(example_path, 'Generate_policy.py'))
    policy_list = generate_policy.generate_policy()
    return policy_list
