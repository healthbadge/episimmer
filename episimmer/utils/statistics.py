import copy
import functools
import os
import pickle
import pprint
from typing import TYPE_CHECKING, Callable, Dict, List, Tuple, Union

from .arg_parser import parse_args
from .time import Time

if TYPE_CHECKING:
    from episimmer.simulate import Simulate


class Stats():
    """
    Class to handle variable statistics in Episimmer
    """
    stats_dict = {}

    @staticmethod
    def add_content(key: str, content: Dict[str, Dict]) -> None:
        """
        Adds content to the statistics dictionary into a list.

        Args:
            key: Key to be added to dictionary
            content: Content to be added as value to the key in dictionary
        """
        world = Time.get_current_world()
        time_step = Time.get_current_time_step()
        if world not in Stats.stats_dict.keys():
            Stats.stats_dict[world] = {}

        if time_step not in Stats.stats_dict[world].keys():
            Stats.stats_dict[world][time_step] = {}

        if key not in Stats.stats_dict[world][time_step].keys():
            Stats.stats_dict[world][time_step][key] = []

        Stats.stats_dict[world][time_step][key].append(content)

    @staticmethod
    def get_dict() -> Dict[str, Dict]:
        """
        Returns the statistics dictionary

        Returns:
            the statistics dictionary
        """
        return Stats.stats_dict


def expand_levels_recursion(obj: object, levels: int,
                            cur_level: int) -> Union[Dict[str, Dict], object]:
    """
    This function is a recursive function which expands the current object's variables
    to a given number of levels. If the object is a dictionary or an iterable,only then
    will the object be expanded. Other objects are returned as is.

    Args:
        obj: Object to be expanded
        levels: Number of levels to expand the object
        cur_level: Current level expanded

    Returns:
        An expanded object
    """

    if cur_level == levels:
        return obj

    stats_dict = {}
    if hasattr(obj, '__dict__'):
        stats_dict[str(obj)] = expand_levels_recursion(vars(obj), levels,
                                                       cur_level + 1)
    elif hasattr(obj, '__iter__'):
        if isinstance(obj, list):
            for obj_i in obj:
                if hasattr(obj_i, '__dict__'):
                    stats_dict[str(obj_i)] = expand_levels_recursion(
                        vars(obj_i), levels, cur_level + 1)
                elif hasattr(obj_i, '__iter__'):
                    stats_dict[str(obj_i)] = expand_levels_recursion(
                        obj_i, levels, cur_level + 1)
                else:
                    return obj
        elif isinstance(obj, dict):
            for obj_i in obj.keys():
                if hasattr(obj[obj_i], '__dict__'):
                    stats_dict[str(obj_i)] = expand_levels_recursion(
                        vars(obj[obj_i]), levels, cur_level + 1)
                elif hasattr(obj[obj_i], '__iter__'):
                    stats_dict[str(obj_i)] = expand_levels_recursion(
                        obj[obj_i], levels, cur_level + 1)
                else:
                    stats_dict[str(obj_i)] = obj[obj_i]
    else:
        return obj

    return stats_dict


def expand_levels(obj: object, levels: int) -> Union[Dict[str, Dict], object]:
    """
    Expands the object by expanding the members of the object such as dictionaries and iterables. Calls the
    expand_levels_recursion method for expansion of object.

    Args:
        obj: Object to be expanded
        levels: Number of levels to expand the object

    Returns:
        An expanded object
    """
    return expand_levels_recursion(obj, levels, 0)


def process_dict_recursion(stats_dict: Dict[str, Dict],
                           final_level_properties: Union[str, List[str]],
                           levels: int, cur_level: int) -> Dict[str, Dict]:
    """
    This function is a recursive function which selects the variables of the dictionary to be saved.

    Args:
        stats_dict: Dictionary containing an object's expanded members
        final_level_properties: Properties required to be saved
        levels: NNumber of levels the object was expanded
        cur_level: Current level of dictionary

    Returns:
        Processed dictionary
    """
    if cur_level == levels:
        for key in list(stats_dict):
            if key not in final_level_properties:
                del (stats_dict[key])
        return stats_dict

    for key in list(stats_dict):
        if isinstance(stats_dict[key], dict):
            ret_dict = process_dict_recursion(stats_dict[key],
                                              final_level_properties, levels,
                                              cur_level + 1)
            # If stats_dict is empty i.e. {}, delete key in higher stats_dict
            if not ret_dict:
                del (stats_dict[key])
            else:
                stats_dict[key] = ret_dict
    return stats_dict


def process_dict(stats_dict: Dict[str, Dict],
                 final_level_properties: Union[str, List[str]],
                 levels: int) -> Dict[str, Dict]:
    """
    Processes the expanded object as a dictionary by choosing to save only required properties.
    Calls the process_dict_recursion method.

    Args:
        stats_dict: Dictionary containing an object's expanded members
        final_level_properties: Properties required to be saved
        levels: NNumber of levels the object was expanded

    Returns:
        Processed dictionary

    """
    if final_level_properties == 'All':
        return stats_dict
    elif not isinstance(final_level_properties, list):
        raise Exception(
            "Final level properties must either be a list or contain value 'All'"
        )
    return process_dict_recursion(stats_dict, final_level_properties, levels,
                                  0)


def get_pretty_print_str(stats_dict: Dict[str, Dict]) -> str:
    """
    Returns the dictionary as a string in pretty print format

    Args:
        stats_dict: Dictionary to be converted to pretty print string

    Returns:
        String representing dictionary in pretty print format

    """
    val_string = pprint.pformat(stats_dict, indent=0)
    val_string += '\n'
    return val_string


def save_pickle(example_path: str, pickle_file: str,
                final_dict: Dict[str, Dict]) -> None:
    """
    Saves the dictionary into a pickle file

    Args:
        example_path: Path to directory containing simulation files.
        pickle_file: Name of pickle file
        final_dict: Dictionary to be saved
    """
    with open(os.path.join(example_path, 'results', pickle_file),
              'wb') as handle:
        pickle.dump(final_dict, handle, protocol=pickle.HIGHEST_PROTOCOL)


def save_to_text_file(example_path: str, string: str,
                      text_filename: str) -> None:
    """
    Saves the string to a text file.

    Args:
        example_path: Path to directory containing simulation files.
        string: String to be saved
        text_filename: Name of text file
    """
    fp = open(os.path.join(example_path, 'results', text_filename), 'w')
    fp.write(string)
    fp.close()


def save_stats(
        obj_lev_tuples: List[Tuple[str, int]],
        key: str,
        final_level_properties: Union[str, List[str]] = 'All') -> Callable:
    """
    Decorator to save statistics (object members) into a dictionary

    Args:
        obj_lev_tuples: List of tuples containing the object to be saved (as a string) and the number of levels
        key: Key to use while saving the content in the statistics dictionary
        final_level_properties: Properties to save. Can be a list of properties/members of the object or 'All'

    Returns:
        Callable function
    """
    def decorator(func: Callable) -> Callable:
        @functools.wraps(func)
        def wrapper(ref: 'Simulate', *args, **kwargs) -> None:
            func(ref, *args, **kwargs)
            args = parse_args()
            stats = args.stats
            if stats:
                for obj_str, levels in obj_lev_tuples:
                    obj = getattr(ref, obj_str)
                    stats_dict = expand_levels(obj,
                                               levels)  # Generate nested dict
                    stats_dict = copy.deepcopy(stats_dict)
                    stats_dict = process_dict(
                        stats_dict, final_level_properties,
                        levels)  # Process dict based on desired properties
                    Stats.add_content(key, stats_dict)

        return wrapper

    return decorator


def write_stats(pickle_file: str, text_file: str) -> Callable:
    """
    Decorator to write statistics (object members) into a file

    Args:
        pickle_file: Name of pickle file
        text_file: Name of text file

    Returns:
        Callable function
    """
    def decorator(func: Callable) -> Callable:
        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            func(*args, **kwargs)
            args = parse_args()
            stats = args.stats
            if stats:
                example_path = args.example_path
                final_dict = Stats.get_dict()
                save_pickle(example_path, pickle_file, final_dict)
                stats_str = get_pretty_print_str(final_dict)
                save_to_text_file(example_path, stats_str, text_file)

        return wrapper

    return decorator
