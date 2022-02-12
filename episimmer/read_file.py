import copy
import json
import os.path as osp
import random
import re
from csv import DictReader
from typing import Dict, List, Tuple, Union

import numpy as np

from .agent import Agent
from .location import Location


class ReadConfiguration():
    """
    Class for reading the simulation configuration file

    Args:
        filename: Name of the directory containing simulation files
    """
    def __init__(self, filename: str):

        self.filename: str = filename
        self.example_path: str = osp.dirname(filename)
        self.random_seed: str = ''
        self.worlds: int = 0
        self.time_steps: int = 0
        self.agent_info_keys: str = ''
        self.agents_filename: str = ''
        self.interaction_info_keys: str = ''
        self.interactions_files_list_list: List[str] = []
        self.probabilistic_interactions_files_list_list: List[str] = []
        self.location_info_keys: str = ''
        self.locations_filename: str = ''
        self.event_info_keys: str = ''
        self.events_files_list_list: List[str] = []
        self.one_time_event_file: str = ''

        self.read_config_file()

    def read_config_file(self) -> None:
        """
        Reads the config.txt file and populates the class with the parameters passed
        """
        f = open(self.filename, 'r')

        self.random_seed = (self.get_value_config(f.readline()))
        if self.random_seed != '':
            random.seed(int(self.random_seed))
            np.random.seed(int(self.random_seed))

        self.worlds = int(self.get_value_config(f.readline()))
        self.time_steps = int(self.get_value_config(f.readline()))

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
                "Error! Agent file does not contain parameter \'Agent Index\'")

        if self.interaction_info_keys.split(':') != ['']:
            if (self.probabilistic_interactions_files_list_list != [''] and self.interactions_files_list_list != ['']) \
                    or self.interactions_files_list_list != ['']:
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

    def get_value_config(self, line: str) -> str:
        """
        Gets the value between the brackets <> in a line of the config file.

        Args:
            line: A single line of string

        Returns:
            Value of the entry in the config file.
        """
        elements = re.findall('<.*?>', line)
        if len(elements) != 1:
            raise Exception('Error! Invalid entry in config.txt')
        value = (((elements[0])[1:])[:-1])
        return value

    def get_file_paths(
        self, example_path: str
    ) -> Tuple[str, List[str], List[str], str, str, List[str]]:
        """
        Gets the paths of the agents file, interactions files, events files, locations file, one time event file, and
        probabilistic interactions files from the config file.

        Args:
            example_path: Path of the directory containing the simulation files.

        Returns:
            Tuple containing paths of the agents file, interactions files, events files, locations file, one time
            event file and probabilistic interactions files.
        """
        # File Names
        locations_filename = one_time_event_file = None
        events_files_list_filename = interactions_files_list_filename = []
        probabilistic_interactions_files_list_filename = []

        agents_filename = osp.join(example_path, self.agents_filename)

        if self.interactions_files_list_list != ['']:
            interactions_files_list_filename = [
                osp.join(example_path, interactions_files_list) for
                interactions_files_list in self.interactions_files_list_list
            ]

        if self.events_files_list_list != ['']:
            events_files_list_filename = [
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
            probabilistic_interactions_files_list_filename = [
                osp.join(example_path, interactions_files_list)
                for interactions_files_list in
                self.probabilistic_interactions_files_list_list
            ]

        return agents_filename, interactions_files_list_filename, events_files_list_filename, \
               locations_filename, one_time_event_file, probabilistic_interactions_files_list_filename

    def get_file_names_list(self, example_path: str, interactions_files_list_filename: List[str],
                            events_files_list_filename: List[str],
                            probabilistic_interactions_files_list_filename: List[str]) -> \
                            Tuple[List[List[str]], List[List[str]], List[List[str]]]:
        """
        Gets the lists of all the paths to the interaction files, events files and probabilistic interaction files.

        Args:
            example_path: Path of the directory containing simulation files
            interactions_files_list_filename: List of path names of all the interactions files
            events_files_list_filename: List of path names of all the events files
            probabilistic_interactions_files_list_filename: List of path names of all the probabilistic interactions
                                                            files

        Returns:
            Tuple containing list of interaction files, list of events files, and list of probabilistic interaction
            files.
        """

        interactions_files_list = events_files_list = probabilistic_interactions_files_list = []

        if self.interactions_files_list_list == ['']:
            pass
        else:
            interaction_files_obj = [
                ReadFilesList(file)
                for file in interactions_files_list_filename
            ]
            interactions_files_list = [
                list(map(lambda x: osp.join(example_path, x), obj.file_list))
                for obj in interaction_files_obj
            ]

        if self.probabilistic_interactions_files_list_list == ['']:
            pass
        else:
            probabilistic_interaction_files_obj = [
                ReadFilesList(file)
                for file in probabilistic_interactions_files_list_filename
            ]
            probabilistic_interactions_files_list = [
                list(map(lambda x: osp.join(example_path, x), obj.file_list))
                for obj in probabilistic_interaction_files_obj
            ]

        if self.events_files_list_list == ['']:
            pass
        else:
            event_files_obj = [
                ReadFilesList(file) for file in events_files_list_filename
            ]
            events_files_list = [
                list(map(lambda x: osp.join(example_path, x), obj.file_list))
                for obj in event_files_obj
            ]

        return interactions_files_list, events_files_list, probabilistic_interactions_files_list


class ReadVDConfiguration():
    """
    Class for reading the Vulnerability Detection configuration file

    Args:
        filename: Name of the directory containing simulation files
    """
    def __init__(self, filename: str):
        self.filename: str = filename
        self.example_path: str = osp.dirname(filename)
        self.target: str = ''
        self.algorithm: str = ''
        self.parameter_dict: Dict[str, Union[List[str], int, List[int]]] = {}
        self.pre_process: str = ''
        self.post_process: str = ''
        self.output_mode: str = ''

        self.read_vd_config_file()

    def read_vd_config_file(self) -> None:
        """
        Reads the vd_config.txt file and populates the class with the parameters passed
        """

        f = open(self.filename, 'r')

        self.target = self.get_value_config(f.readline())
        self.algorithm = self.get_value_config(f.readline())
        self.read_parameter_file(self.get_value_config(f.readline()))
        self.pre_process = self.get_value_config(f.readline())
        self.post_process = self.get_value_config(f.readline())
        self.output_mode = self.get_value_config(f.readline())

        f.close()

        if self.target == '':
            raise Exception('Error! Target required in vd_config.txt')

        if self.algorithm == '':
            raise Exception('Error! Algorithm required in vd_config.txt')

        if not self.parameter_dict:
            raise Warning(
                'No parameters provided in vd_config.txt. Using Defaults')

    def get_value_config(self, line: str) -> str:
        """
        Gets the value between the brackets <> in a line of the vd config file.

        Args:
            line: A single line of string

        Returns:
            Value of the entry in the config file.
        """
        elements = re.findall('<.*?>', line)
        if len(elements) != 1:
            raise Exception('Error! Invalid entry in vd_config.txt')
        value = (((elements[0])[1:])[:-1])
        return value

    def read_parameter_file(self, filename: str) -> None:
        """
        Reads and saves the parameters from the parameters.json file.

        Args:
            filename: Name of the json file containing the parameters
        """
        f = open(osp.join(self.example_path, filename), 'r')
        data = json.load(f)
        self.parameter_dict = data
        f.close()


class ReadFilesList():
    """
    Reads and saves the list of file names from the files list file

    Args:
        filename: Name of the files list file
    """
    def __init__(self, filename: str):
        self.filename: str = filename
        self.file_list: List[str] = []

        self.read_files_list()

    def read_files_list(self) -> None:
        """
        Reads the files list file and generates a list containing all the files
        """

        f = open(self.filename, 'r')
        lines = f.readlines()
        separator = ' '
        text = separator.join(lines)
        elements = re.findall('<.*?>', text)
        for filename in elements:
            self.file_list.append((filename[1:])[:-1])
        f.close()


class BaseReadFile():
    """
    Base class for reading agents, locations, interactions and events from a file.
    """
    def __init__(self):
        pass

    def get_value(self, line) -> str:
        """
        Takes a single line and clips the backslash n element

        Args:
            line: A string line

        Returns:
            A string line without the backslash n  element

        """
        if line.endswith('\n'):
            line = line[:-1]
        return line


class ReadAgents(BaseReadFile):
    """
    Class for reading and storing agent information from the agents file.
    Inherits :class:`BaseReadFile` class.

    Args:
        filename: Name of the file containing agent information.
        config_obj: An object of class :class:`~episimmer.read_file.ReadConfiguration` containing the simulation
                    configurations.
    """
    def __init__(self, filename: str, config_obj: ReadConfiguration):
        super().__init__()
        self.filename: str = filename
        self.config_obj: ReadConfiguration = config_obj
        self.n: Union[int, None] = None
        self.parameter_keys: List[str] = []
        self.agents: Dict[str, Agent] = {}

        self.read_agents_file()

    def read_agents_file(self) -> None:
        """
        Reads the agents file (either a txt or csv file) and generates a dictionary mapping agent indices to
        :class:`~episimmer.agent.Agent` objects with the information from the file.
        """
        if self.filename.endswith('.txt'):
            f = open(self.filename, 'r')
            self.n = int(self.get_value(f.readline()))
            agent_info_keys = self.get_value(f.readline())
            if agent_info_keys != self.config_obj.agent_info_keys:
                raise Exception(
                    'Error! Agent Information parameters do not match the config.txt file'
                )

            self.parameter_keys = agent_info_keys.split(':')

            for i in range(self.n):
                info_dict = self.create_info_dict(
                    self.get_value(f.readline()).split(':'))
                state = None  # config_obj.default_state
                agent = Agent(state, info_dict)
                self.agents[agent.index] = agent
            f.close()

        elif self.filename.endswith('.csv'):
            with open(self.filename, 'r') as read_obj:
                csv_dict_reader = DictReader(read_obj)
                csv_list = list(csv_dict_reader)
                self.n = len(csv_list)

                # Assuming that we have a config file that is .txt file.
                agent_info_keys = ':'.join(csv_dict_reader.fieldnames)
                if agent_info_keys != self.config_obj.agent_info_keys:
                    raise Exception(
                        'Error! Agent Information parameters do not match the config.txt file'
                    )

                self.parameter_keys = csv_dict_reader.fieldnames

                for i in range(self.n):
                    info_dict = dict(csv_list[i])
                    state = None  # config_obj.default_state
                    agent = Agent(state, info_dict)
                    self.agents[agent.index] = agent

    def create_info_dict(self, info_list: List[str]) -> Dict[str, str]:
        """
        Creates a dictionary of information regarding an agent.

        Args:
            info_list: List of values for all the parameter keys of an agent.

        Returns:
            Information dictionary of the agent.
        """
        info_dict = {}
        for i, key in enumerate(self.parameter_keys):
            info_dict[key] = info_list[i]

        return info_dict


class ReadInteractions(BaseReadFile):
    """
    Class for reading and storing individual interaction information from the interactions file.
    Inherits :class:`BaseReadFile` class.

    Args:
        filename: Name of the file containing individual interaction information.
        config_obj: An object of class :class:`ReadConfiguration` containing the simulation
                    configurations.
        agents_obj: An object of class :class:`ReadAgents` containing agent information
    """
    def __init__(self, filename: str, config_obj: ReadConfiguration,
                 agents_obj: ReadAgents):
        super().__init__()
        self.filename: str = filename
        self.config_obj: ReadConfiguration = config_obj
        self.agents_obj: ReadAgents = agents_obj
        self.no_interactions: int = 0
        self.parameter_keys: List[str] = []

        self.read_interactions_file()

    def read_interactions_file(self) -> None:
        """
        Reads the interaction file (either a txt or csv file) and adds contact information from the interactions file
        to the :class:`~episimmer.agent.Agent` objects.
        """
        if self.filename == '' or self.filename is None:
            return

        if self.filename.endswith('.txt'):
            f = open(self.filename, 'r')
            self.no_interactions = int(self.get_value(f.readline()))
            interaction_info_keys = self.get_value(f.readline())
            if interaction_info_keys != self.config_obj.interaction_info_keys:
                raise Exception(
                    'Error! Interaction parameters do not match the config.txt file'
                )
            self.parameter_keys = interaction_info_keys.split(':')

            for i in range(self.no_interactions):
                parameter_list = (self.get_value(f.readline())).split(':')
                agent_index, info_dict = self.get_interaction(parameter_list)
                if agent_index is not None and info_dict is not None:
                    self.agents_obj.agents[agent_index].add_contact(info_dict)

            f.close()

        elif self.filename.endswith('.csv'):
            with open(self.filename, 'r') as read_obj:
                csv_dict_reader = DictReader(read_obj)
                csv_list = list(csv_dict_reader)
                self.no_interactions = len(csv_list)

                interaction_info_keys = ':'.join(csv_dict_reader.fieldnames)
                if interaction_info_keys != self.config_obj.interaction_info_keys:
                    raise Exception(
                        'Error! Interaction Information parameters do not match the config.txt file'
                    )
                self.parameter_keys = csv_dict_reader.fieldnames

                for i in range(self.no_interactions):
                    info_dict = dict(csv_list[i])
                    if (info_dict['Agent Index']
                            in self.agents_obj.agents.keys()
                            and info_dict['Interacting Agent Index']
                            in self.agents_obj.agents):
                        agent_index = info_dict['Agent Index']
                        self.agents_obj.agents[agent_index].add_contact(
                            info_dict)

    def get_interaction(
        self, parameter_list: List[str]
    ) -> Tuple[Union[str, None], Union[Dict[str, str], None]]:
        """
         Creates a dictionary containing information of a single interaction.

        Args:
            parameter_list: List of values for all the parameter keys of an interaction.

        Returns:
            Information dictionary of the interaction.
        """
        info_dict = {}
        agent_index = None
        for i, key in enumerate(self.parameter_keys):
            if key == 'Agent Index':
                agent_index = parameter_list[i]

            info_dict[key] = parameter_list[i]

        if (agent_index not in self.agents_obj.agents.keys()
                or info_dict['Interacting Agent Index']
                not in self.agents_obj.agents.keys()):
            agent_index, info_dict = None, None

        return agent_index, info_dict


class ReadProbabilisticInteractions(BaseReadFile):
    """
    Class for reading and storing probabilistic interaction information from the probabilistic interactions file.
    Inherits :class:`BaseReadFile` class.

    Args:
        filename: Name of the file containing probabilistic interaction information.
        config_obj: An object of class :class:`ReadConfiguration` containing the simulation
                    configurations.
        agents_obj: An object of class :class:`ReadAgents` containing agent information
    """
    def __init__(self, filename: str, config_obj: ReadConfiguration,
                 agents_obj: ReadAgents):
        super().__init__()
        self.filename: str = filename
        self.config_obj: ReadConfiguration = config_obj
        self.agents_obj: ReadAgents = agents_obj
        self.no_interaction_sets: int = 0
        self.parameter_keys: List[str] = []

        self.read_prob_interactions_file()

    def read_prob_interactions_file(self) -> None:
        """
        Reads the probabilistic interaction file (a txt file) and adds contact information from the file
        to the :class:`~episimmer.agent.Agent` objects.
        """
        if self.filename == '' or self.filename is None:
            return

        if self.filename.endswith('.txt'):
            f = open(self.filename, 'r')
            self.no_interaction_sets = int(self.get_value(f.readline()))
            self.parameter_keys = self.get_value(f.readline()).split(':')
            config_interaction_info_keys_list = self.config_obj.interaction_info_keys.split(
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
                    self.agents_obj.agents[agent_index].add_contact(info_dict)

            f.close()

    def get_interactions(
            self,
            parameter_list: List[str]) -> List[Tuple[str, Dict[str, str]]]:
        """
         Generates the interactions using probability values and agent indices given in the probabilistic
         interactions file.

        Args:
            parameter_list: List containing probability of interaction and agent indices associated with
                            that probability.

        Returns:
            Interaction list consisting of tuples of agent index and interaction information (as a dictionary).
        """
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
                agent_indexes = parameter_list[i].split(',')
                agent_indexes = list(dict.fromkeys(
                    agent_indexes))  # Convert to unique list (with same order)
                agent_indexes = [
                    index for index in agent_indexes
                    if index in self.agents_obj.agents.keys()
                ]

            else:
                info_dict[key] = parameter_list[i]

        for index, agent_index1 in enumerate(agent_indexes):
            for agent_index2 in agent_indexes[index + 1:]:
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
    """
    Class for reading and storing location information from the locations file.
    Inherits :class:`BaseReadFile` class.

    Args:
        filename: Name of the file containing location information.
        config_obj: An object of class :class:`ReadConfiguration` containing the simulation
                    configurations.
    """
    def __init__(self, filename: str, config_obj: ReadConfiguration):
        super().__init__()
        self.filename: str = filename
        self.config_obj: ReadConfiguration = config_obj
        self.locations: Dict[str, Location] = {}
        self.no_locations: int = 0
        self.parameter_keys: List[str] = []

        self.read_locations_file()

    def read_locations_file(self) -> None:
        """
        Reads the locations file (a txt file) and adds the information from the file
        to the :class:`~episimmer.agent.Agent` objects.
        """
        if self.filename == '' or self.filename is None:
            return
        f = open(self.filename, 'r')

        self.no_locations = int(self.get_value(f.readline()))
        location_info_keys = self.get_value(f.readline())
        if location_info_keys != self.config_obj.location_info_keys:
            raise Exception(
                'Error! Location parameters do not match the config.txt file')
        self.parameter_keys = location_info_keys.split(':')

        for i in range(self.no_locations):
            info_dict = self.create_info_dict(
                self.get_value(f.readline()).split(':'))
            location = Location(info_dict)
            self.locations[location.index] = location

        f.close()

    def create_info_dict(self, info_list: List[str]) -> Dict[str, str]:
        """
         Creates a dictionary containing information of a single location.

        Args:
            info_list: List of values for all the parameter keys of a location.

        Returns:
            Information dictionary of the location.
        """
        info_dict = {}
        for i, key in enumerate(self.parameter_keys):
            info_dict[key] = info_list[i]

        return info_dict


class ReadEvents(BaseReadFile):
    """
    Class for reading and storing simple event information from the events file.
    Inherits :class:`BaseReadFile` class.

    Args:
        filename: Name of the file containing event information.
        config_obj: An object of class :class:`ReadConfiguration` containing the simulation
                    configurations.
        locations_obj: An object of class :class:`ReadLocations` containing location information
        agents_obj: An object of class :class:`ReadAgents` containing agent information
    """
    def __init__(self,
                 filename: str,
                 config_obj: Union[ReadConfiguration, None] = None,
                 locations_obj: Union[ReadLocations, None] = None,
                 agents_obj: Union[ReadAgents, None] = None):
        super().__init__()
        self.filename: str = filename
        self.config_obj: Union[ReadConfiguration, None] = config_obj
        self.locations_obj: Union[ReadLocations, None] = locations_obj
        self.agents_obj: Union[ReadAgents, None] = agents_obj
        self.no_events: int = 0
        self.parameter_keys: List[str] = []

        if config_obj:
            self.read_events_file()

    def read_events_file(self) -> None:
        """
        Reads the events file (a txt file) and adds the information from the file
        to the :class:`~episimmer.location.Location` objects.
        """
        if self.filename == '' or self.filename is None:
            return
        f = open(self.filename, 'r')
        self.no_events = int(self.get_value(f.readline()))
        event_info_keys = self.get_value(f.readline())
        if event_info_keys != self.config_obj.event_info_keys:
            raise Exception(
                'Error! Event parameters do not match the config.txt file')

        self.parameter_keys = event_info_keys.split(':')

        for i in range(self.no_events):
            parameter_list = (self.get_value(f.readline())).split(':')
            location_index, info_dict = self.get_event(parameter_list)
            if location_index is not None and info_dict is not None:
                self.locations_obj.locations[location_index].add_event(
                    info_dict)

        f.close()

    def get_event(
        self, parameter_list: List[str]
    ) -> Tuple[Union[str, None], Union[Dict[str, Union[float, str, List[str]]],
                                       None]]:
        """
         Creates a dictionary containing information of a single event.

        Args:
            parameter_list: List of values for all the parameter keys of an event.

        Returns:
            Information dictionary of the event.
        """
        info_dict = {}
        location_index = None
        for i, key in enumerate(self.parameter_keys):
            if key == 'Location Index':
                location_index = parameter_list[i]

            if key == 'Agents':
                info_dict[key] = parameter_list[i].split(',')

                if info_dict[key][-1] == '':
                    info_dict[key] = info_dict[:-1]

                info_dict[key] = list(
                    dict.fromkeys(info_dict[key])
                )  # Convert to unique list (with same order)

                if set(info_dict[key]) - set(list(self.agents_obj.agents)):
                    to_remove = set(info_dict[key]) - set(
                        list(self.agents_obj.agents))
                    info_dict[key] = [
                        index for index in info_dict[key]
                        if index not in to_remove
                    ]

            else:
                info_dict[key] = parameter_list[i]

        if info_dict['Agents'] is None or self.agents_obj.agents is None:
            location_index, info_dict = None, None

        if location_index is None:
            raise Exception('Error! No event to read in the event file')
        return location_index, info_dict


class ReadOneTimeEvents(ReadEvents):
    """
    Class for reading and storing one time event information from the one time event file.
    Inherits :class:`ReadEvents` class.

    Args:
        filename: Name of the file containing one time event information.
    """
    def __init__(self, filename: str):
        super().__init__(filename)
        self.event_info_keys: str = ''
        self.one_time_parameter_keys: List[str] = []
        self.eventsAt: Dict[int, List[str]] = {}

        self.read_one_time_events_file()

    def read_one_time_events_file(self) -> None:
        """
        Reads the one time events file (a txt file) and populates a dictionary mapping from time step to event
        information
        """
        if self.filename == '' or self.filename is None:
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

    def populate_one_time_events(self, config_obj: ReadConfiguration,
                                 locations_obj: ReadLocations,
                                 agents_obj: ReadAgents,
                                 time_step: int) -> None:
        """
        Populates the locations objects with one time events at the current time step

        Args:
            config_obj: An object of class :class:`ReadConfiguration` containing the simulation
                        configurations.
            locations_obj: An object of class :class:`ReadLocations` containing location information
            agents_obj: An object of class :class:`ReadAgents` containing agent information
            time_step: current time step
        """
        if self.filename == '' or self.filename is None:
            return
        self.config_obj = config_obj
        self.locations_obj = locations_obj
        self.agents_obj = agents_obj
        if self.event_info_keys != 'Time Step:' + config_obj.event_info_keys:
            raise Exception(
                'Error! One Time Event parameters do not match the config.txt file'
            )
        for event in self.eventsAt.get(time_step, []):
            parameter_list = (self.get_value(event)).split(':')
            location_index, info_dict = self.get_event(parameter_list)
            self.locations_obj.locations[location_index].add_event(info_dict)
