import sys
import ReadFile
import pickle
import World
import importlib.util

def module_from_file(module_name, file_path):
    spec = importlib.util.spec_from_file_location(module_name, file_path)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module

path=sys.argv[1]
if path[-1]!='/':
	path+='/'
config_filename=path+'config.txt'

interactions_files_list=None
events_files_list=None
locations_filename=None

config_obj=ReadFile.ReadConfiguration(config_filename)


agents_filename=path+config_obj.agents_filename
interactions_FilesList_filename=path+config_obj.interactions_files_list
if config_obj.locations_filename=="":
	locations_filename=None
else:
	locations_filename=path+config_obj.locations_filename
events_FilesList_filename=path+config_obj.events_files_list

if config_obj.interactions_files_list=='':
	print('No Interaction files uploaded!')
else:
	interactionFiles_obj=ReadFile.ReadFilesList(interactions_FilesList_filename)
	interactions_files_list=list(map(lambda x : path+x ,interactionFiles_obj.file_list))
	if interactions_files_list==[]:
		print('No Interactions inputted')

if config_obj.events_files_list=='':
	print('No Event files uploaded!')
else:
	eventFiles_obj=ReadFile.ReadFilesList(events_FilesList_filename)
	events_files_list=list(map(lambda x : path+x ,eventFiles_obj.file_list))
	if events_files_list==[]:
		print('No Events inputted')

'''Generate_model = module_from_file("Generate_model", path+'Generate_model.py')
model=Generate_model.generate_model()

'''
UserModel = module_from_file("Generate_model", path+'UserModel.py')
model = UserModel.UserModel()
Generate_policy = module_from_file("Generate_policy", path+'Generate_policy.py')
policy_list, event_restriction_fn=Generate_policy.generate_policy()

world_obj=World.World(config_obj,model,policy_list,event_restriction_fn,agents_filename,interactions_files_list,locations_filename,events_files_list)
world_obj.simulate_worlds()


