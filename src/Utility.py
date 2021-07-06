import matplotlib.pyplot as plt
import matplotlib.animation as ani
import importlib.util
import os.path as osp
import sys
import ReadFile

def average(tdict, number):
    for k in tdict.keys():
        l = tdict[k]
        for i in range(len(l)):
            tdict[k][i] /= number
    return tdict

def plotResults(model_name, tdict, plot):
    for state in tdict.keys():
        plt.plot(tdict[state])
    plt.title(model_name + ' Plot')
    plt.legend(list(tdict.keys()), loc='upper right', shadow=True)
    plt.ylabel('Population')
    plt.xlabel('Time Steps (in unit steps)')
    plt.grid(b=True, which='major', color='#666666', linestyle='-')
    plt.minorticks_on()
    plt.grid(b=True, which='minor', color='#999999',linestyle='-', alpha=0.2)
    fig = plt.gcf()
    if plot:
        plt.show()
    return fig

def animateResults(model_name, tdict):
    fig = plt.figure()
    def buildmebarchart(i=int):
        plt.clf()
        plt.title(model_name + ' Plot')
        plt.ylabel('Population')
        plt.xlabel('Time Steps (in unit steps)')
        plt.grid(b=True, which='major', color='#666666', linestyle='-')
        plt.minorticks_on()
        plt.grid(b=True, which='minor', color='#999999', linestyle='-', alpha=0.2)
        for state in tdict.keys():
            plt.plot(tdict[state][:i], label=state)
        plt.legend(loc='upper left', shadow=True)
    return ani.FuncAnimation(fig, buildmebarchart, interval=150)


def module_from_file(module_name, file_path):
    spec = importlib.util.spec_from_file_location(module_name, file_path)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def get_config_path(path):
    config_filepath = osp.join(path, 'config.txt')
    return config_filepath


def get_file_paths(example_path, config_obj):
    # File Names
    locations_filename = one_time_event_file = None
    events_FilesList_filename = interactions_FilesList_filename = []

    agents_filename = osp.join(example_path, config_obj.agents_filename)

    if config_obj.interactions_files_list_list != ['']:
        interactions_FilesList_filename = [osp.join(
            example_path, interactions_files_list) for interactions_files_list in config_obj.interactions_files_list_list]

    if config_obj.events_files_list_list != ['']:
        events_FilesList_filename = [osp.join(
            example_path, events_files_list) for events_files_list in config_obj.events_files_list_list]

    if config_obj.locations_filename != '':
    	locations_filename = osp.join(example_path, config_obj.locations_filename)

    if config_obj.one_time_event_file != '':
    	one_time_event_file = osp.join(
    	    example_path, config_obj.one_time_event_file)

    if config_obj.probabilistic_interactions_files_list_list != '':
    	probabilistic_interactions_FilesList_filename = [osp.join(
    	    example_path, interactions_files_list) for interactions_files_list in config_obj.probabilistic_interactions_files_list_list]

    return agents_filename, interactions_FilesList_filename, events_FilesList_filename, locations_filename, one_time_event_file, probabilistic_interactions_FilesList_filename


def get_file_names_list(example_path, interactions_FilesList_filename, events_FilesList_filename, probabilistic_interactions_FilesList_filename, config_obj):
    # Reading through a file (for interactions/events) that contain file names which contain interactions and event details for a time step

    interactions_files_list = events_files_list = probabilistic_interactions_files_list = []

    if config_obj.interactions_files_list_list == ['']:
    	print('No Interaction files uploaded!')
    else:
    	interactionFiles_obj = [ReadFile.ReadFilesList(
    	    file) for file in interactions_FilesList_filename]
    	interactions_files_list = [list(map(lambda x: osp.join(
    	    example_path, x), obj.file_list)) for obj in interactionFiles_obj]

    if config_obj.probabilistic_interactions_files_list_list == ['']:
    	print('No Probabilistic Interaction files uploaded!')
    else:
    	probabilistic_interactionFiles_obj = [ReadFile.ReadFilesList(
    	    file) for file in probabilistic_interactions_FilesList_filename]
    	probabilistic_interactions_files_list = [list(map(lambda x: osp.join(
    	    example_path, x), obj.file_list)) for obj in probabilistic_interactionFiles_obj]

    if config_obj.events_files_list_list == ['']:
    	print('No Event files uploaded!')
    else:
    	eventFiles_obj = [ReadFile.ReadFilesList(
    	    file) for file in events_FilesList_filename]
    	events_files_list = [list(map(lambda x: osp.join(
    	    example_path, x), obj.file_list)) for obj in eventFiles_obj]

    return interactions_files_list, events_files_list, probabilistic_interactions_files_list


def get_model(example_path):
    UserModel = module_from_file(
        "Generate_model", osp.join(example_path, 'UserModel.py'))
    model = UserModel.UserModel()
    return model


def get_policy(example_path):
    Generate_policy = module_from_file(
        "Generate_policy", osp.join(example_path, 'Generate_policy.py'))
    policy_list, event_restriction_fn = Generate_policy.generate_policy()
    return policy_list, event_restriction_fn
