import copy
import functools
import os
import pickle
import pprint

from .arg_parser import parse_args
from .time import Time

is_obj = lambda obj: hasattr(obj, '__dict__')
is_iter = lambda obj: hasattr(obj, '__iter__')
is_list = lambda obj: isinstance(obj, list)
is_dict = lambda obj: isinstance(obj, dict)

expand_obj = lambda obj: vars(obj)


class Stats():
    d = {}

    @staticmethod
    def add_content(K, C):
        W = Time.get_current_world()
        T = Time.get_current_time_step()
        if (W not in Stats.d.keys()):
            Stats.d[W] = {}

        if (T not in Stats.d[W].keys()):
            Stats.d[W][T] = {}

        if (K not in Stats.d[W][T].keys()):
            Stats.d[W][T][K] = []

        Stats.d[W][T][K].append(C)

    @staticmethod
    def get_dict():
        return Stats.d


def expand_levels_recursion(obj, levels, cur_level):

    if cur_level == levels:
        return obj

    dict = {}
    if is_obj(obj):
        dict[str(obj)] = expand_levels_recursion(expand_obj(obj), levels,
                                                 cur_level + 1)
    elif is_iter(obj):
        if is_list(obj):
            for obj_i in obj:
                if is_obj(obj_i):
                    dict[str(obj_i)] = expand_levels_recursion(
                        expand_obj(obj_i), levels, cur_level + 1)
                elif is_iter(obj_i):
                    dict[str(obj_i)] = expand_levels_recursion(
                        obj_i, levels, cur_level + 1)
                else:
                    return obj
        elif is_dict(obj):
            for obj_i in obj.keys():
                if is_obj(obj[obj_i]):
                    dict[str(obj_i)] = expand_levels_recursion(
                        expand_obj(obj[obj_i]), levels, cur_level + 1)
                elif is_iter(obj[obj_i]):
                    dict[str(obj_i)] = expand_levels_recursion(
                        obj[obj_i], levels, cur_level + 1)
                else:
                    dict[str(obj_i)] = obj[obj_i]
    else:
        return obj

    return dict


def expand_levels(obj, levels):
    return expand_levels_recursion(obj, levels, 0)


def process_dict_recursion(dict, final_level_properties, levels, cur_level):
    if (cur_level == levels):
        for key in list(dict):
            if (key not in final_level_properties):
                del (dict[key])
        return dict

    for key in list(dict):
        if (is_dict(dict[key])):
            ret_dict = process_dict_recursion(dict[key],
                                              final_level_properties, levels,
                                              cur_level + 1)
            if (not ret_dict
                ):  # If dict is empty i.e. {}, delete key in higher dict
                del (dict[key])
            else:
                dict[key] = ret_dict
    return dict


def process_dict(dict, final_level_properties, levels):
    if (final_level_properties == 'All'):
        return dict
    elif (not is_list(final_level_properties)):
        raise Exception(
            "Final level properties must either be a list or contain value 'All'"
        )
    return process_dict_recursion(dict, final_level_properties, levels, 0)


def get_pretty_print_str(dict):
    val_string = pprint.pformat(dict, indent=0)
    val_string += '\n'
    return val_string


def save_pickle(example_path, pickle_file, final_dict):
    with open(os.path.join(example_path, 'results', pickle_file),
              'wb') as handle:
        pickle.dump(final_dict, handle, protocol=pickle.HIGHEST_PROTOCOL)


def save_to_text_file(example_path, str, text_filename):
    fp = open(os.path.join(example_path, 'results', text_filename), 'w')
    fp.write(str)
    fp.close()


def save_stats(obj_lev_tuples, key, final_level_properties='All'):
    def decorator(func):
        @functools.wraps(func)
        def wrapper(ref, *args, **kwargs):
            func(ref, *args, **kwargs)
            args = parse_args()
            stats = args.stats
            if (stats):
                for obj_str, levels in obj_lev_tuples:
                    obj = getattr(ref, obj_str)
                    dict = expand_levels(obj, levels)  # Generate nested dict
                    dict = copy.deepcopy(dict)
                    dict = process_dict(
                        dict, final_level_properties,
                        levels)  # Process dict based on desired properties
                    Stats.add_content(key, dict)

        return wrapper

    return decorator


def write_stats(pickle_file, text_file):
    def decorator(func):
        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            func(*args, **kwargs)
            args = parse_args()
            stats = args.stats
            if (stats):
                example_path = args.example_path
                final_dict = Stats.get_dict()
                save_pickle(example_path, pickle_file, final_dict)
                str = get_pretty_print_str(final_dict)
                save_to_text_file(example_path, str, text_file)

        return wrapper

    return decorator
