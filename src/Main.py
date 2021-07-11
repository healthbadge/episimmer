import ReadFile
import World
import argparse
import Utility
import os.path as osp

def get_model(example_path):
    UserModel = Utility.module_from_file("Generate_model", osp.join(example_path, 'UserModel.py'))
    model = UserModel.UserModel()
    return model

def get_policy(example_path):
    Generate_policy = Utility.module_from_file("Generate_policy", osp.join(example_path, 'Generate_policy.py'))
    policy_list, event_restriction_fn = Generate_policy.generate_policy()
    return policy_list, event_restriction_fn

def get_config_path(path):
    config_filepath = osp.join(path, 'config.txt')
    return config_filepath

if __name__=="__main__":

    arg_parser = argparse.ArgumentParser(prog='Main.py', usage='%(prog)s example_path [options]')

    # input argument options
    arg_parser.add_argument("example_path")
    arg_parser.add_argument("-np", "--noplot", help="doesn't show plot after simulation", required=False, action="store_true")
    arg_parser.add_argument("-an", "--animate", help="creates gif animation in the example folder", required=False, action="store_true")
    args = arg_parser.parse_args()

    plot = not args.noplot
    anim = args.animate

    example_path = args.example_path
    config_filename = get_config_path(example_path)

    # Read Config file using ReadFile.ReadConfiguration
    config_obj=ReadFile.ReadConfiguration(config_filename)

    agents_filename, interactions_FilesList_filename,\
        events_FilesList_filename, locations_filename, one_time_event_file, probabilistic_interactions_FilesList_filename = config_obj.get_file_paths(example_path)
    interactions_files_list, events_files_list, probabilistic_interactions_files_list = config_obj.get_file_names_list(
        example_path, interactions_FilesList_filename, events_FilesList_filename, probabilistic_interactions_FilesList_filename)

    # User Model and Policy
    model = get_model(example_path)
    policy_list, event_restriction_fn=get_policy(example_path)

    # Creation of World object
    world_obj = World.World(config_obj, model, policy_list, event_restriction_fn, agents_filename, interactions_files_list,probabilistic_interactions_files_list, locations_filename, events_files_list, one_time_event_file)
    world_obj.simulate_worlds(plot, anim)
