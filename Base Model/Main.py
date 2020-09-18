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
agents_filename=path+'agents.txt'
model_filename=path+'example_model'
interactionFilesList_filename=path+'interaction_files_list.txt'

config_obj=ReadFile.ReadConfiguration(config_filename)
#agents_obj=ReadFile.ReadAgents(agents_filename,config_obj)
interactionFiles_obj=ReadFile.ReadInteractionFilesList(interactionFilesList_filename)
interactionFiles_list=list(map(lambda x : path+x ,interactionFiles_obj.file_list))

#model=pickle.load(open(model_filename, "rb"))
Generate_model = module_from_file("Generate_model", path+'Generate_model.py')
model=Generate_model.generate_model()

world_obj=World.World(config_obj,agents_filename,model,interactionFiles_list)
world_obj.simulate_worlds()


