import copy
import functools
import os
import pickle
import pprint

from .arg_parser import parse_args
from .time import Time


def is_obj(obj):
    return hasattr(obj, '__dict__')


def is_iter(obj):
    return hasattr(obj, '__iter__')


def is_list(obj):
    return isinstance(obj, list)


def is_dict(obj):
    return isinstance(obj, dict)


def expand_obj(obj):
    return vars(obj)


class Stats():
    d = {}

    @staticmethod
    def add_content(key, content):
        world = Time.get_current_world()
        time_step = Time.get_current_time_step()
        if world not in Stats.d.keys():
            Stats.d[world] = {}

        if time_step not in Stats.d[world].keys():
            Stats.d[world][time_step] = {}

        if key not in Stats.d[world][time_step].keys():
            Stats.d[world][time_step][key] = []

        Stats.d[world][time_step][key].append(content)

    @staticmethod
    def get_dict():
        return Stats.d


def expand_levels_recursion(obj, levels, cur_level):

    if cur_level == levels:
        return obj

    stats_dict = {}
    if is_obj(obj):
        stats_dict[str(obj)] = expand_levels_recursion(expand_obj(obj), levels,
                                                       cur_level + 1)
    elif is_iter(obj):
        if is_list(obj):
            for obj_i in obj:
                if is_obj(obj_i):
                    stats_dict[str(obj_i)] = expand_levels_recursion(
                        expand_obj(obj_i), levels, cur_level + 1)
                elif is_iter(obj_i):
                    stats_dict[str(obj_i)] = expand_levels_recursion(
                        obj_i, levels, cur_level + 1)
                else:
                    return obj
        elif is_dict(obj):
            for obj_i in obj.keys():
                if is_obj(obj[obj_i]):
                    stats_dict[str(obj_i)] = expand_levels_recursion(
                        expand_obj(obj[obj_i]), levels, cur_level + 1)
                elif is_iter(obj[obj_i]):
                    stats_dict[str(obj_i)] = expand_levels_recursion(
                        obj[obj_i], levels, cur_level + 1)
                else:
                    stats_dict[str(obj_i)] = obj[obj_i]
    else:
        return obj

    return stats_dict


def expand_levels(obj, levels):
    return expand_levels_recursion(obj, levels, 0)


def process_dict_recursion(stats_dict, final_level_properties, levels,
                           cur_level):
    if cur_level == levels:
        for key in list(stats_dict):
            if key not in final_level_properties:
                del (stats_dict[key])
        return stats_dict

    for key in list(stats_dict):
        if is_dict(stats_dict[key]):
            ret_dict = process_dict_recursion(stats_dict[key],
                                              final_level_properties, levels,
                                              cur_level + 1)
            # If stats_dict is empty i.e. {}, delete key in higher stats_dict
            if not ret_dict:
                del (stats_dict[key])
            else:
                stats_dict[key] = ret_dict
    return stats_dict


def process_dict(stats_dict, final_level_properties, levels):
    if final_level_properties == 'All':
        return stats_dict
    elif not is_list(final_level_properties):
        raise Exception(
            "Final level properties must either be a list or contain value 'All'"
        )
    return process_dict_recursion(stats_dict, final_level_properties, levels,
                                  0)


def get_pretty_print_str(stats_dict):
    val_string = pprint.pformat(stats_dict, indent=0)
    val_string += '\n'
    return val_string


def save_pickle(example_path, pickle_file, final_dict):
    with open(os.path.join(example_path, 'results', pickle_file),
              'wb') as handle:
        pickle.dump(final_dict, handle, protocol=pickle.HIGHEST_PROTOCOL)


def save_to_text_file(example_path, string, text_filename):
    fp = open(os.path.join(example_path, 'results', text_filename), 'w')
    fp.write(string)
    fp.close()


def save_stats(obj_lev_tuples, key, final_level_properties='All'):
    def decorator(func):
        @functools.wraps(func)
        def wrapper(ref, *args, **kwargs):
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


def write_stats(pickle_file, text_file):
    def decorator(func):
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
