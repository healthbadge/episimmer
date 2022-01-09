import copy
import json
import os.path as osp
import random
import re
from csv import DictReader

from .agent import Agent
from .location import Location
from .utils.time import Time


class ReadConfiguration():
    def __init__(self, filename):
        self.worlds = None
        self.time_steps = None
        self.starting_exposed_percentage = None
        self.agent_info_keys = None
        self.interaction_info_keys = None
        self.example_path = osp.dirname(filename)

        f = open(filename, 'r')

        self.random_seed = (self.get_value_config(f.readline()))
        if (self.random_seed != ''):
            random.seed((int)(self.random_seed))

        self.worlds = (int)(self.get_value_config(f.readline()))
        self.time_steps = (int)(self.get_value_config(f.readline()))

        self.agent_info_keys = self.get_value_config(f.readline())
        self.agents_filename = self.get_value_config(f.readline())
        self.interaction_info_keys = self.get_value_config(f.readline())
        self.interactions_files_list_list = (self.get_value_config(
            f.readline())).split(',')
        self.probabilistic_interactions_files_list_list = (
            self.get_value_config(f.readline())).split(',')

        self.location_info_keys = self.get_value_config(f.readline())
        self.locations_filename = self.get_value_config(f.readline())
        self.event_info_keys = self.get_value_config(f.readline())
        self.events_files_list_list = (self.get_value_config(
            f.readline())).split(',')
        self.one_time_event_file = self.get_value_config(f.readline())
        f.close()

        if 'Agent Index' not in self.agent_info_keys.split(':'):
            raise Exception(
                "Error! Agent file  does not contain parameter \'Agent Index\'"
            )

        if self.interaction_info_keys.split(':') != ['']:
            if (self.probabilistic_interactions_files_list_list != [''] and self.interactions_files_list_list != ['']) or \
                self.interactions_files_list_list != ['']:
                if 'Agent Index' not in self.interaction_info_keys.split(':'):
                    raise Exception(
                        "Interaction definition does not contain parameter \'Agent Index\'"
                    )

                if 'Interacting Agent Index' not in self.interaction_info_keys.split(
                        ':'):
                    raise Exception(
                        "Interaction definition does not contain parameter \'Interacting Agent Index\'"
                    )

            elif self.probabilistic_interactions_files_list_list != ['']:
                if 'Agents' not in self.interaction_info_keys.split(':'):
                    raise Exception(
                        "Interaction definition does not contain parameter \'Agents\'"
                    )

                if 'Probability' not in self.interaction_info_keys.split(':'):
                    raise Exception(
                        "Interaction definition does not contain parameter \'Probability\'"
                    )

        if self.event_info_keys.split(':') != ['']:
            if 'Location Index' not in self.location_info_keys.split(':'):
                raise Exception(
                    'Location file does not contain parameter \'Location Index\''
                )

            if 'Location Index' not in self.event_info_keys.split(':'):
                raise Exception(
                    'Event definition does not contain parameter \'Location Index\''
                )

            if 'Agents' not in self.event_info_keys.split(':'):
                raise Exception(
                    'Event definition does not contain parameter \'Agents\'')

    def get_value_config(self, line):
        l = re.findall('\<.*?\>', line)
        if len(l) != 1:
            raise Exception('Error! Invalid entry in config.txt')
        value = (((l[0])[1:])[:-1])
        return value

    def get_file_paths(self, example_path):
        # File Names
        locations_filename = one_time_event_file = None
        events_FilesList_filename = interactions_FilesList_filename = []

        agents_filename = osp.join(example_path, self.agents_filename)

        if self.interactions_files_list_list != ['']:
            interactions_FilesList_filename = [
                osp.join(example_path, interactions_files_list) for
                interactions_files_list in self.interactions_files_list_list
            ]

        if self.events_files_list_list != ['']:
            events_FilesList_filename = [
                osp.join(example_path, events_files_list)
                for events_files_list in self.events_files_list_list
            ]

        if self.locations_filename != '':
            locations_filename = osp.join(example_path,
                                          self.locations_filename)

        if self.one_time_event_file != '':
            one_time_event_file = osp.join(example_path,
                                           self.one_time_event_file)

        if self.probabilistic_interactions_files_list_list != '':
            probabilistic_interactions_FilesList_filename = [
                osp.join(example_path, interactions_files_list)
                for interactions_files_list in
                self.probabilistic_interactions_files_list_list
            ]

        return agents_filename, interactions_FilesList_filename, events_FilesList_filename, locations_filename, one_time_event_file, probabilistic_interactions_FilesList_filename

    def get_file_names_list(self, example_path,
                            interactions_FilesList_filename,
                            events_FilesList_filename,
                            probabilistic_interactions_FilesList_filename):
        # Reading through a file (for interactions/events) that contain file names which contain interactions and event details for a time step

        interactions_files_list = events_files_list = probabilistic_interactions_files_list = []

        if self.interactions_files_list_list == ['']:
            print('No Interaction files uploaded!')
        else:
            interactionFiles_obj = [
                ReadFilesList(file) for file in interactions_FilesList_filename
            ]
            interactions_files_list = [
                list(map(lambda x: osp.join(example_path, x), obj.file_list))
                for obj in interactionFiles_obj
            ]

        if self.probabilistic_interactions_files_list_list == ['']:
            print('No Probabilistic Interaction files uploaded!')
        else:
            probabilistic_interactionFiles_obj = [
                ReadFilesList(file)
                for file in probabilistic_interactions_FilesList_filename
            ]
            probabilistic_interactions_files_list = [
                list(map(lambda x: osp.join(example_path, x), obj.file_list))
                for obj in probabilistic_interactionFiles_obj
            ]

        if self.events_files_list_list == ['']:
            print('No Event files uploaded!')
        else:
            eventFiles_obj = [
                ReadFilesList(file) for file in events_FilesList_filename
            ]
            events_files_list = [
                list(map(lambda x: osp.join(example_path, x), obj.file_list))
                for obj in eventFiles_obj
            ]

        return interactions_files_list, events_files_list, probabilistic_interactions_files_list


class ReadVDConfiguration():
    def __init__(self, filename):
        self.target = None
        self.algorithm = None
        self.parameter_dict = {}
        self.pre_process = None
        self.post_process = None
        self.output_mode = None
        self.example_path = osp.dirname(filename)

        f = open(filename, 'r')

        self.target = (self.get_value_config(f.readline()))
        self.algorithm = (self.get_value_config(f.readline()))
        self.read_parameter_file(self.get_value_config(f.readline()))
        self.pre_process = self.get_value_config(f.readline())
        self.post_process = self.get_value_config(f.readline())
        self.output_mode = self.get_value_config(f.readline())

        f.close()

        if (self.target == ''):
            raise Exception('Error! Target required in vd_config.txt')

        if (self.algorithm == ''):
            raise Exception('Error! Algorithm required in vd_config.txt')

        if (not self.parameter_dict):
            raise Warning(
                'No parameters provided in vd_config.txt. Using Defaults')

    def get_value_config(self, line):
        l = re.findall('\<.*?\>', line)
        if len(l) != 1:
            raise Exception('Error! Invalid entry in vd_config.txt')
        value = (((l[0])[1:])[:-1])
        return value

    def read_parameter_file(self, filename):
        f = open(osp.join(self.example_path, filename), 'r')
        data = json.load(f)
        self.parameter_dict = data
        f.close()


class ReadFilesList():
    def __init__(self, filename):
        self.file_list = []
        f = open(filename, 'r')
        lines = f.readlines()
        separator = ' '
        text = separator.join(lines)
        l = re.findall('\<.*?\>', text)
        for filename in l:
            self.file_list.append(((filename)[1:])[:-1])
        f.close()


class BaseReadFile():
    def __init__(self):
        pass

    def get_value(self, line):
        if line.endswith('\n'):
            line = line[:-1]
        return line


class ReadAgents(BaseReadFile):
    def __init__(self, filename, config_obj):
        super().__init__()

        if filename.endswith('.txt'):
            f = open(filename, 'r')
            self.n = int(self.get_value(f.readline()))
            agent_info_keys = self.get_value(f.readline())
            if agent_info_keys != config_obj.agent_info_keys:
                raise Exception(
                    'Error! Agent Information parameters do not match the config.txt file'
                )

            self.parameter_keys = agent_info_keys.split(':')
            self.agents = {}

            for i in range(self.n):
                info_dict = self.create_info_dict(
                    self.get_value(f.readline()).split(':'))
                state = None  #config_obj.default_state
                agent = Agent(state, info_dict)
                self.agents[agent.index] = agent
            f.close()

        elif filename.endswith('.csv'):
            with open(filename, 'r') as read_obj:
                csv_dict_reader = DictReader(read_obj)
                csv_list = list(csv_dict_reader)
                self.n = len(csv_list)

                # Assuming that we have a config file that is .txt file.
                agent_info_keys = ':'.join(csv_dict_reader.fieldnames)
                if agent_info_keys != config_obj.agent_info_keys:
                    raise Exception(
                        'Error! Agent Information parameters do not match the config.txt file'
                    )

                self.parameter_keys = csv_list
                self.agents = {}

                for i in range(self.n):
                    info_dict = csv_list[i]
                    state = None  #config_obj.default_state
                    agent = Agent(state, info_dict)
                    self.agents[agent.index] = agent

    def create_info_dict(self, info_list):
        info_dict = {}
        for i, key in enumerate(self.parameter_keys):
            info_dict[key] = info_list[i]

        return info_dict


class ReadInteractions(BaseReadFile):
    def __init__(self, filename, config_obj, agents_obj):
        super().__init__()
        self.config_obj = config_obj
        self.agents_obj = agents_obj
        if filename == '' or filename == None:
            return

        if filename.endswith('.txt'):
            f = open(filename, 'r')
            self.no_interactions = int(self.get_value(f.readline()))
            interaction_info_keys = self.get_value(f.readline())
            if interaction_info_keys != config_obj.interaction_info_keys:
                raise Exception(
                    'Error! Interaction parameters do not match the config.txt file'
                )
            self.parameter_keys = interaction_info_keys.split(':')

            for i in range(self.no_interactions):
                parameter_list = (self.get_value(f.readline())).split(':')
                agent_index, info_dict = self.get_interaction(parameter_list)
                if (agent_index is not None and info_dict is not None):
                    agents_obj.agents[agent_index].add_contact(info_dict)

            f.close()

        elif filename.endswith('.csv'):
            with open(filename, 'r') as read_obj:
                csv_dict_reader = DictReader(read_obj)
                csv_list = list(csv_dict_reader)
                self.n = len(csv_list)

                self.parameter_keys = ':'.join(csv_dict_reader.fieldnames)
                if self.parameter_keys != config_obj.interaction_info_keys:
                    raise Exception(
                        'Error! Interaction Information parameters do not match the config.txt file'
                    )

                for i in range(self.n):
                    info_dict = csv_list[i]
                    if (info_dict['Agent Index'] in set(self.agents_obj.agents)
                            and info_dict['Interacting Agent Index'] in set(
                                self.agents_obj.agents)):
                        agent_index = info_dict['Agent Index']
                        agents_obj.agents[agent_index].add_contact(info_dict)

    def get_interaction(self, parameter_list):
        info_dict = {}
        agent_index = None
        contact_agent_index = None
        for i, key in enumerate(self.parameter_keys):
            if key == 'Agent Index':
                agent_index = parameter_list[i]

            info_dict[key] = parameter_list[i]

        if (agent_index not in set(self.agents_obj.agents)
                or info_dict['Interacting Agent Index'] not in set(
                    self.agents_obj.agents)):
            agent_index, info_dict = None, None

        return agent_index, info_dict


class ReadProbabilisticInteractions(BaseReadFile):
    def __init__(self, filename, config_obj, agents_obj):
        super().__init__()
        self.config_obj = config_obj
        self.agents_obj = agents_obj
        if filename == '' or filename == None:
            return

        if filename.endswith('.txt'):
            f = open(filename, 'r')
            self.no_interaction_sets = int(self.get_value(f.readline()))
            self.parameter_keys = self.get_value(f.readline()).split(':')
            config_interaction_info_keys_list = config_obj.interaction_info_keys.split(
                ':')

            if self.parameter_keys != config_interaction_info_keys_list and self.parameter_keys[
                    2:] != config_interaction_info_keys_list and self.parameter_keys[
                        2:] != config_interaction_info_keys_list[2:]:
                raise Exception(
                    'Error! Probabilistic Interaction parameters do not match the config.txt file'
                )

            for i in range(self.no_interaction_sets):
                parameter_list = (self.get_value(f.readline())).split(':')
                interactions_list = self.get_interactions(parameter_list)
                for (agent_index, info_dict) in interactions_list:
                    agents_obj.agents[agent_index].add_contact(info_dict)

            f.close()

    def get_interactions(self, parameter_list):
        info_dict = {}
        agent_indexes = []
        interactions_list = []
        interaction_probability = 0

        for i, key in enumerate(self.parameter_keys):
            if key == 'Probability':
                try:
                    interaction_probability = float(parameter_list[i])
                    if interaction_probability < 0 or interaction_probability > 1:
                        return []
                except:
                    return []

            elif key == 'Agents':
                agent_indexes = list(set(parameter_list[i].split(',')))
                agent_indexes = list(
                    set(agent_indexes) & set(self.agents_obj.agents))

            else:
                info_dict[key] = parameter_list[i]

        for indx, agent_index1 in enumerate(agent_indexes):
            for agent_index2 in agent_indexes[indx + 1:]:
                if random.random() < interaction_probability:

                    temp_info_dict = copy.deepcopy(info_dict)
                    temp_info_dict['Agent Index'] = agent_index1
                    temp_info_dict['Interacting Agent Index'] = agent_index2
                    interactions_list.append((agent_index1, temp_info_dict))

                    temp_info_dict = copy.deepcopy(info_dict)
                    temp_info_dict['Agent Index'] = agent_index2
                    temp_info_dict['Interacting Agent Index'] = agent_index1
                    interactions_list.append((agent_index2, temp_info_dict))

        return interactions_list


class ReadLocations(BaseReadFile):
    def __init__(self, filename, config_obj):
        super().__init__()
        self.config_obj = config_obj
        self.locations = {}
        if filename == '' or filename == None:
            return
        f = open(filename, 'r')

        self.no_locations = int(self.get_value(f.readline()))
        location_info_keys = self.get_value(f.readline())
        if location_info_keys != config_obj.location_info_keys:
            raise Exception(
                'Error! Location parameters do not match the config.txt file')
        self.parameter_keys = location_info_keys.split(':')

        for i in range(self.no_locations):
            info_dict = self.create_info_dict(
                self.get_value(f.readline()).split(':'))
            location = Location(info_dict)
            self.locations[location.index] = location

        f.close()

    def create_info_dict(self, info_list):
        info_dict = {}
        for i, key in enumerate(self.parameter_keys):
            info_dict[key] = info_list[i]

        return info_dict


class ReadEvents(BaseReadFile):
    def __init__(self, filename, config_obj, locations_obj, agents_obj):
        super().__init__()
        self.config_obj = config_obj
        self.locations_obj = locations_obj
        self.agents_obj = agents_obj
        if filename == '' or filename == None:
            return
        f = open(filename, 'r')
        self.no_events = int(self.get_value(f.readline()))
        event_info_keys = self.get_value(f.readline())
        if event_info_keys != config_obj.event_info_keys:
            raise Exception(
                'Error! Event parameters do not match the config.txt file')

        self.parameter_keys = event_info_keys.split(':')

        for i in range(self.no_events):
            parameter_list = (self.get_value(f.readline())).split(':')
            location_index, info_dict = self.get_event(parameter_list)
            if (location_index is not None and info_dict is not None):
                self.locations_obj.locations[location_index].add_event(
                    info_dict)

        f.close()

    def get_event(self, parameter_list):
        info_dict = {}
        location_index = None
        for i, key in enumerate(self.parameter_keys):
            if key == 'Location Index':
                location_index = parameter_list[i]

            if key == 'Agents':
                info_dict[key] = list(set(parameter_list[i].split(',')))
                if info_dict[key][-1] == '':
                    info_dict[key] = info_dict[:-1]
            else:
                info_dict[key] = parameter_list[i]

        if (info_dict['Agents'] is None or self.agents_obj.agents is None):
            location_index, info_dict = None, None

        elif (set(info_dict['Agents']) - set(list(self.agents_obj.agents))):
            to_remove = set(info_dict['Agents']) - set(
                list(self.agents_obj.agents))
            info_dict['Agents'] = list(set(info_dict['Agents']) - to_remove)

        if location_index == None:
            raise Exception('Error! No event to read in the event file')
        return location_index, info_dict


class ReadOneTimeEvents(BaseReadFile):
    def __init__(self, filename):
        super().__init__()
        self.filename = filename
        if self.filename == '' or self.filename == None:
            return
        f = open(self.filename, 'r')
        self.no_events = int(self.get_value(f.readline()))
        self.event_info_keys = self.get_value(f.readline())
        self.one_time_parameter_keys = self.event_info_keys.split(':')
        self.parameter_keys = self.one_time_parameter_keys[1:]
        self.eventsAt = {}
        for i in range(self.no_events):
            line = (self.get_value(f.readline())).split(':')
            for time in line[0].split(','):
                self.eventsAt[int(time)] = self.eventsAt.get(
                    int(time), []) + [':'.join(line[1:])]
        f.close()

    def ReadOneTimeEvents(self, config_obj, locations_obj, agents_obj):
        if self.filename == '' or self.filename == None:
            return
        self.config_obj = config_obj
        self.locations_obj = locations_obj
        self.agents_obj = agents_obj
        if self.event_info_keys != 'Time Step:' + config_obj.event_info_keys:
            raise Exception(
                'Error! One Time Event parameters do not match the config.txt file'
            )
        for event in self.eventsAt.get(Time.get_current_time_step(), []):
            parameter_list = (self.get_value(event)).split(':')
            location_index, info_dict = self.get_event(parameter_list)
            self.locations_obj.locations[location_index].add_event(info_dict)

    def get_event(self, parameter_list):
        info_dict = {}
        location_index = None
        for i, key in enumerate(self.parameter_keys):
            if key == 'Location Index':
                location_index = parameter_list[i]

            if key == 'Agents':
                info_dict[key] = list(set(parameter_list[i].split(',')))
                if info_dict[key][-1] == '':
                    info_dict[key] = info_dict[:-1]
            else:
                info_dict[key] = parameter_list[i]

        if (info_dict['Agents'] is None or self.agents_obj.agents is None):
            location_index, info_dict = None, None

        elif (set(info_dict['Agents']) - set(list(self.agents_obj.agents))):
            to_remove = set(info_dict['Agents']) - set(
                list(self.agents_obj.agents))
            info_dict['Agents'] = list(set(info_dict['Agents']) - to_remove)

        if location_index == None:
            raise Exception(
                'Error! No event to read in the one time event file')
        return location_index, info_dict
