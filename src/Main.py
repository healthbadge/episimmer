import ReadFile
import World
import argparse
from Utility import *

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
        events_FilesList_filename, locations_filename, one_time_event_file, probabilistic_interactions_FilesList_filename = get_file_paths(example_path, config_obj)
    interactions_files_list, events_files_list, probabilistic_interactions_files_list = get_file_names_list(example_path,interactions_FilesList_filename,events_FilesList_filename,probabilistic_interactions_FilesList_filename,config_obj)

    # User Model and Policy
    model = get_model(example_path)
    policy_list, event_restriction_fn=get_policy(example_path)

    # Creation of World object
    world_obj = World.World(config_obj, model, policy_list, event_restriction_fn, agents_filename, interactions_files_list,probabilistic_interactions_files_list, locations_filename, events_files_list, one_time_event_file)
    world_obj.simulate_worlds(plot, anim)
