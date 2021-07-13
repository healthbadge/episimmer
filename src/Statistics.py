import functools
import pprint
import copy
import Utility
import os
import Time
import pickle

is_obj = lambda obj : hasattr(obj, '__dict__')
is_iter = lambda obj : hasattr(obj, '__iter__')
is_list = lambda obj : isinstance(obj, list)
is_dict = lambda obj : isinstance(obj, dict)

expand_obj = lambda obj : vars(obj)

def expand_levels_recursion(obj, levels, cur_level):

    if cur_level==levels:
        return obj

    dict = {}
    if is_obj(obj):
        dict[str(obj)] = expand_levels_recursion(expand_obj(obj), levels, cur_level+1)
    elif is_iter(obj):
        if is_list(obj):
            for obj_i in obj:
                if is_obj(obj_i):
                    dict[str(obj_i)] = expand_levels_recursion(expand_obj(obj_i), levels, cur_level+1)
                elif is_iter(obj_i):
                    dict[str(obj_i)] = expand_levels_recursion(obj_i, levels, cur_level+1)
                else:
                    return obj
        elif is_dict(obj):
            for obj_i in obj.keys():
                if is_obj(obj[obj_i]):
                    dict[str(obj_i)] = expand_levels_recursion(expand_obj(obj[obj_i]), levels, cur_level+1)
                elif is_iter(obj[obj_i]):
                    dict[str(obj_i)] = expand_levels_recursion(obj[obj_i], levels, cur_level+1)
                else:
                    dict[str(obj_i)] = obj[obj_i]
    else:
        return obj

    return dict

def expand_levels(obj, levels):
    return expand_levels_recursion(obj, levels, 0)

def process_dict_recursion(dict, final_level_properties, levels, cur_level):
    if(cur_level == levels):
        for key in list(dict):
            if(key not in final_level_properties):
                del(dict[key])
        return dict

    for key in list(dict):
        if(is_dict(dict[key])):
            ret_dict = process_dict_recursion(dict[key], final_level_properties, levels, cur_level+1)
            if(not ret_dict): # If dict is empty i.e. {}, delete key in higher dict
                del(dict[key])
            else:
                dict[key] = ret_dict
    return dict

def process_dict(dict, final_level_properties, levels):
    if(final_level_properties == "All"):
        return dict
    elif(not is_list(final_level_properties)):
        raise Exception("Final level properties must either be a list or contain value 'All'")
    return process_dict_recursion(dict, final_level_properties, levels, 0)

def get_pretty_print_str(dict):
    val_string = pprint.pformat(dict, indent=0)
    val_string += "\n"
    return val_string

def save_to_csv():
    pass

def save_pickle(example_path,obj_str,levels,dict):
    filename = obj_str+str(levels)+".pickle"
    with open(os.path.join(example_path,'results', filename), 'wb') as handle:
        pickle.dump(dict, handle, protocol=pickle.HIGHEST_PROTOCOL)

def save_to_text_file(str, example_path, text_filename):
    fp = open(os.path.join(example_path,'results', text_filename), "a")
    fp.write(str)
    fp.close()

def save_stats(obj_lev_tuples, group, text_filename, final_level_properties = "All"):
    def decorator(func):
        @functools.wraps(func)
        def wrapper(ref, *args,**kwargs) :
            func(ref, *args, **kwargs)
            args = Utility.parse_args()
            stats = args.stats
            example_path = args.example_path
            if(stats):
                str = ""
                for obj_str,levels in obj_lev_tuples:
                    obj = getattr(ref, obj_str)
                    dict = expand_levels(obj, levels) # Generate nested dict
                    dict = copy.deepcopy(dict)
                    dict = process_dict(dict, final_level_properties, levels) # Process dict based on desired properties
                    final_dict = {"World" : Time.Time.get_current_world(), "Timestep" : Time.Time.get_current_time_step(), "Contents" : dict}
                    # save_pickle(example_path,obj_str,levels,final_dict)
                    str += get_pretty_print_str(final_dict) # Pretty printing
                save_to_text_file(str, example_path, text_filename)

        return wrapper

    return decorator


if __name__ == "__main__":
    class A():
        def __init__(self):
            self.a = 0
            self.ls = [1,2,3,4]
            self.b = None

    class B():
        def __init__(self):
            self.b0 = 0
            self.bls = [1,2,3,4]
            self.c = None

    a = A()
    b = B()
    a.b = b
    a0 = A()
    a1 = A()
    a2 = A()
    b.c = {'1':a0, '2':a1, '3':a2}

    print(expand_levels(a,4))
