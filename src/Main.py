import sys
import ReadFile
import pickle
import World
import importlib.util
import os.path as osp

def module_from_file(module_name, file_path):
    spec = importlib.util.spec_from_file_location(module_name, file_path)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module

def get_example_path():
    return sys.argv[1]


def get_config_path(path):
    config_filepath=osp.join(path,'config.txt')
    return config_filepath


def get_file_paths(example_path,config_obj):
    # File Names
    locations_filename=None
    agents_filename=osp.join(example_path,config_obj.agents_filename)
    interactions_FilesList_filename = [osp.join(example_path, interactions_files_list) for interactions_files_list in config_obj.interactions_files_list_list]
    events_FilesList_filename = [osp.join(example_path, events_files_list) for events_files_list in config_obj.events_files_list_list]
    if config_obj.locations_filename=="":
    	locations_filename=None
    else:
    	locations_filename=osp.join(example_path,config_obj.locations_filename)

    return agents_filename, interactions_FilesList_filename, events_FilesList_filename, locations_filename


def get_file_names_list(example_path,interactions_FilesList_filename,events_FilesList_filename,config_obj):
    # Reading through a file (for interactions/events) that contain file names which contain interactions and event details for a time step

    interactions_files_list=None
    events_files_list=None

    if config_obj.interactions_files_list_list==['']:
    	print('No Interaction files uploaded!')
    else:
    	interactionFiles_obj = [ReadFile.ReadFilesList(file) for file in interactions_FilesList_filename]
    	interactions_files_list = [list(map(lambda x: osp.join(example_path, x), obj.file_list)) for obj in interactionFiles_obj]
    	if interactions_files_list==[[]]:
    		print('No Interactions inputted')


    if config_obj.events_files_list_list==['']:
    	print('No Event files uploaded!')
    else:
    	eventFiles_obj = [ReadFile.ReadFilesList(file) for file in events_FilesList_filename]
    	events_files_list = [list(map(lambda x: osp.join(example_path, x), obj.file_list)) for obj in eventFiles_obj]
    	if events_files_list==[[]]:
    		print('No Events inputted')

    return interactions_files_list, events_files_list

def get_model(example_path):
    UserModel = module_from_file("Generate_model", osp.join(example_path,'UserModel.py'))
    model = UserModel.UserModel()
    return model

def get_policy(example_path):
    Generate_policy = module_from_file("Generate_policy", osp.join(example_path,'Generate_policy.py'))
    policy_list, event_restriction_fn=Generate_policy.generate_policy()
    return policy_list, event_restriction_fn

if __name__=="__main__":

    example_path = get_example_path()
    config_filename = get_config_path(example_path)

    # Read Config file using ReadFile.ReadConfiguration
    config_obj=ReadFile.ReadConfiguration(config_filename)

    agents_filename, interactions_FilesList_filename,\
    events_FilesList_filename, locations_filename = get_file_paths(example_path,config_obj)
    interactions_files_list, events_files_list = get_file_names_list(example_path,interactions_FilesList_filename,events_FilesList_filename,config_obj)

    # User Model and Policy
    model = get_model(example_path)
    policy_list, event_restriction_fn=get_policy(example_path)

    # Creation of World object
    world_obj=World.World(config_obj,model,policy_list,event_restriction_fn,agents_filename,interactions_files_list,locations_filename,events_files_list)
    world_obj.simulate_worlds()
