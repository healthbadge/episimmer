import copy
import json
import os.path as osp
import random
import re
from csv import DictReader
from typing import Callable, Dict, List, Tuple, Union
from episimmer.agent import Agent
from episimmer.location import Location
from episimmer.utils.time import Time

from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from episimmer.model import BaseModel
    



class ReadConfiguration():
    """
    Class for reading the configuration file of an example used in Episimmer to obtain the required file paths and file names
    needed for its simulation.

    Args:
        filename: Name of the example directory
    """
    def __init__(self, filename: str):
        self.worlds: int = None
        self.time_steps: int = None
        self.starting_exposed_percentage: float = None
        self.agent_info_keys: str = None
        self.interaction_info_keys: str = None
        self.example_path: str = osp.dirname(filename)

        f = open(filename, 'r')

        self.random_seed: int = (self.get_value_config(f.readline()))
        if (self.random_seed != ''):
            random.seed((int)(self.random_seed))

        self.worlds = (int)(self.get_value_config(f.readline()))
        self.time_steps = (int)(self.get_value_config(f.readline()))

        self.agent_info_keys = self.get_value_config(f.readline())
        self.agents_filename: str = self.get_value_config(f.readline())
        self.interaction_info_keys = self.get_value_config(f.readline())
        self.interactions_files_list_list: List[str] = (self.get_value_config(
            f.readline())).split(',')
        self.probabilistic_interactions_files_list_list: List[str] = (
            self.get_value_config(f.readline())).split(',')

        self.location_info_keys: str = self.get_value_config(f.readline())
        self.locations_filename: str = self.get_value_config(f.readline())
        self.event_info_keys: str = self.get_value_config(f.readline())
        self.events_files_list_list: List[str] = (self.get_value_config(
            f.readline())).split(',')
        self.one_time_event_file: str = self.get_value_config(f.readline())
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

    def get_value_config(self, line: str) -> str:
        """
        Gets the value associated with the label in a line of the config file.

        Args:
            line: Line in the config file which has a label and its respective value
            
        Returns:
            Value of an entry in the config file.
        """
        l = re.findall('\<.*?\>', line)
        if len(l) != 1:
            raise Exception('Error! Invalid entry in config.txt')
        value = (((l[0])[1:])[:-1])
        return value

    def get_file_paths(self, example_path: str) -> Tuple[str]:
        # File Names
        """
        Gets the paths of the agents file, interactions files, events files, locations file, one time event file, and
        probabalistic interactions files from the config file.

        Args:
            example_path: Path of the directory of the example used in Episimmer.
            
        Returns:
            Tuple containing paths of the agents file, interactions files, events files, locations file, one time event file, and
            probabalistic interactions files.
        """
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

    def get_file_names_list(self, example_path: str,
                            interactions_FilesList_filename: str,
                            events_FilesList_filename: str,
                            probabilistic_interactions_FilesList_filename: str) -> Tuple[List[str]]:
        # Reading through a file (for interactions/events) that contain file names which contain interactions and event details for a time step
        """
        Gets the list of all the interaction files, events files and probabilistic interaction files.

        Args:
            example_path: Path of the directory of the example used in Episimmer
            interactions_FilesList_filename: List of path names of all the interactions files
            events_FilesList_filename: List of path names of all the events files
            probabilistic_interactions_FilesList_filename: List of path names of all the prababilistic interactions files
            
        Returns:
            Tuple containing list of interaction files, list of events files, and list of probabilistic interaction files.
        """

        interactions_files_list = events_files_list = probabilistic_interactions_files_list = []

        if self.interactions_files_list_list == ['']:
            pass
        else:
            interactionFiles_obj = [
                ReadFilesList(file) for file in interactions_FilesList_filename
            ]
            interactions_files_list = [
                list(map(lambda x: osp.join(example_path, x), obj.file_list))
                for obj in interactionFiles_obj
            ]

        if self.probabilistic_interactions_files_list_list == ['']:
            pass
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
            pass
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
    """
    Class for reading the configuration file of an example built for Vulnerability Detection used in Episimmer to obtain the
    required file paths and file names needed for its simulation.

    Args:
        filename: Name of the example directory
    """
    def __init__(self, filename: str):
        self.target: str = None
        self.algorithm: str = None
        self.parameter_dict: Dict[str, Union[List[str], int]] = {}
        self.pre_process: str = None
        self.post_process: str = None
        self.output_mode: str = None
        self.example_path: str = osp.dirname(filename)

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

    def get_value_config(self, line: str) -> str:
        """
        Gets the value associated with the label in a line of the config file.

        Args:
            line: Line in the config file which has a label and its respective value
            
        Returns:
            Value of an entry in the config file.
        """
        l = re.findall('\<.*?\>', line)
        if len(l) != 1:
            raise Exception('Error! Invalid entry in vd_config.txt')
        value = (((l[0])[1:])[:-1])
        return value

    def read_parameter_file(self, filename: str) -> None:
        """
        Gets the parameters associated with the Vulnerability Detection example.

        Args:
            filename: Name of the json file containing the parameters
        """
        f = open(osp.join(self.example_path, filename), 'r')
        data = json.load(f)
        self.parameter_dict = data
        f.close()


class ReadFilesList():
    """
    Reads environment components that contains the list of file lists files.
    """
    def __init__(self, filename: str):
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
    """
    Base class for reading agents, locations, interactions and events from a file.
    """
    def __init__(self):
        pass

    def get_value(self, line: str):
        if line.endswith('\n'):
            line = line[:-1]
        return line


class ReadAgents(BaseReadFile):
    """
    Class for reading and storing agent information from a file.
    Inherits :class:`~episimmer.read_file.BaseReadFile` class.

    Args:
        filename: Name of the file containing agent information.
        config_obj: A dictionary containing information from the config file of the example.
    """
    def __init__(self, filename: str, config_obj: ReadConfiguration):
        super().__init__()

        if filename.endswith('.txt'):
            f = open(filename, 'r')
            self.n: int = int(self.get_value(f.readline()))
            agent_info_keys = self.get_value(f.readline())
            if agent_info_keys != config_obj.agent_info_keys:
                raise Exception(
                    'Error! Agent Information parameters do not match the config.txt file'
                )

            self.parameter_keys: List[str] = agent_info_keys.split(':')
            self.agents: Dict[str, Agent] = {}

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
    Class for reading and storing interaction information of the agents from a file.
    Inherits :class:`~episimmer.read_file.BaseReadFile` class.

    Args:
        filename: Name of the file containing agent interaction information.
        config_obj: An object of class :class:`~episimmer.read_file.ReadConfiguration` containing all configurations.
    """
    def __init__(self, filename: str, config_obj: ReadConfiguration, agents_obj: ReadAgents):
        super().__init__()
        self.config_obj: ReadConfiguration = config_obj
        self.agents_obj: ReadAgents= agents_obj
        if filename == '' or filename == None:
            return

        if filename.endswith('.txt'):
            f = open(filename, 'r')
            self.no_interactions: int = int(self.get_value(f.readline()))
            interaction_info_keys = self.get_value(f.readline())
            if interaction_info_keys != config_obj.interaction_info_keys:
                raise Exception(
                    'Error! Interaction parameters do not match the config.txt file'
                )
            self.parameter_keys: List[str] = interaction_info_keys.split(':')

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
                self.n: int = len(csv_list)

                self.parameter_keys: str = ':'.join(csv_dict_reader.fieldnames)
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

    def get_interaction(self, parameter_list: List[str]) -> Tuple[str, Dict[str, str]]:
        """
        Creates a dictionary for an agent containing interaction information.

        Args:
            parameter_list: List containing agent index and interacting agent index
            
        Returns:
            Agent index and information dictionary of the agent.
        """
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
    """
    Class for reading and storing probabilistic interaction information of the agents from a file.
    Inherits :class:`~episimmer.read_file.BaseReadFile` class.

    Args:
        filename: Name of the file containing agent probabilistic interaction information.
        config_obj: An object of class :class:`~episimmer.read_file.ReadConfiguration` containing all configurations.
        agents_obj: An object of class :class:`~episimmer.read_file.ReadAgents` containing all agents
    """
    def __init__(self, filename: str, config_obj: ReadConfiguration, agents_obj: ReadAgents):
        super().__init__()
        self.config_obj: ReadConfiguration = config_obj
        self.agents_obj: ReadAgents = agents_obj
        if filename == '' or filename == None:
            return

        if filename.endswith('.txt'):
            f = open(filename, 'r')
            self.no_interaction_sets: int = int(self.get_value(f.readline()))
            self.parameter_keys: List[str] = self.get_value(f.readline()).split(':')
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

    def get_interactions(self, parameter_list: List[str]) -> Union[Tuple[str, Dict[str, str]], None]:
        """
        Creates a list of interactions using probability values and agent indices according to parameter values.

        Args:
            parameter_list: List containing probability of interaction and agent indices associated with that probability.
            
        Returns:
            Interaction list consisting of tuples of agent index and interaction information.
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
    """
    Class for reading and storing location information from a file.
    Inherits :class:`~episimmer.read_file.BaseReadFile` class.

    Args:
        filename: Name of the file containing location information.
        config_obj: An object of class :class:`~episimmer.read_file.ReadConfiguration` containing all configurations.
    """
    def __init__(self, filename: str, config_obj: ReadConfiguration):
        super().__init__()
        self.config_obj: ReadConfiguration = config_obj
        self.locations: Dict[str, ReadLocations] = {}
        if filename == '' or filename == None:
            return
        f = open(filename, 'r')

        self.no_locations: int = int(self.get_value(f.readline()))
        location_info_keys = self.get_value(f.readline())
        if location_info_keys != config_obj.location_info_keys:
            raise Exception(
                'Error! Location parameters do not match the config.txt file')
        self.parameter_keys: List[str] = location_info_keys.split(':')

        for i in range(self.no_locations):
            info_dict = self.create_info_dict(
                self.get_value(f.readline()).split(':'))
            location = Location(info_dict)
            self.locations[location.index] = location
        
        f.close()

    def create_info_dict(self, info_list: List[str]) -> Dict[str, str]:
        """
        Creates a dictionary of information regarding an agent.

        Args:
            info_list: List of values for all the parameter keys of a location.

        Returns:
            Information dictionary of the agent.
        """
        info_dict = {}
        for i, key in enumerate(self.parameter_keys):
            info_dict[key] = info_list[i]

        return info_dict


class ReadEvents(BaseReadFile):
    """
    Class for reading and storing event information from a file.
    Inherits :class:`~episimmer.read_file.BaseReadFile` class.

    Args:
        filename: Name of the file containing event information.
        config_obj: An object of class :class:`~episimmer.read_file.ReadConfiguration` containing all configurations.
    """
    def __init__(self, filename: str, config_obj: ReadConfiguration, locations_obj: ReadLocations, agents_obj: ReadAgents):
        super().__init__()
        self.config_obj: ReadConfiguration = config_obj
        self.locations_obj: ReadLocations = locations_obj
        self.agents_obj: ReadAgents = agents_obj
        if filename == '' or filename == None:
            return
        f = open(filename, 'r')
        self.no_events: int = int(self.get_value(f.readline()))
        event_info_keys = self.get_value(f.readline())
        if event_info_keys != config_obj.event_info_keys:
            raise Exception(
                'Error! Event parameters do not match the config.txt file')

        self.parameter_keys: List[str] = event_info_keys.split(':')

        for i in range(self.no_events):
            parameter_list = (self.get_value(f.readline())).split(':')
            location_index, info_dict = self.get_event(parameter_list)
            if (location_index is not None and info_dict is not None):
                self.locations_obj.locations[location_index].add_event(
                    info_dict)

        f.close()

    def get_event(self, parameter_list: List[str]) -> Tuple[str, Dict[str, Union[str, List[str]]]]:
        """
        Creates a dictionary for a location containing information about the events taking place at that location.

        Args:
            parameter_list: List containing location index of a location and agent indices of the agents part of an event taking place
            at that location.

        Returns:
            Location index and information dictionary of the location.
        """
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
    """
    Class for reading and storing one time event information from a file.
    Inherits :class:`~episimmer.read_file.BaseReadFile` class.

    Args:
        filename: Name of the file containing ont time event information.
    """
    def __init__(self, filename: str):
        super().__init__()
        self.filename: str = filename
        if self.filename == '' or self.filename == None:
            return
        f = open(self.filename, 'r')
        self.no_events: int = int(self.get_value(f.readline()))
        self.event_info_keys: str = self.get_value(f.readline())
        self.one_time_parameter_keys: List[sttr] = self.event_info_keys.split(':')
        self.parameter_keys: List[str] = self.one_time_parameter_keys[1:]
        self.eventsAt: Dict[int, List[str]] = {}
        for i in range(self.no_events):
            line = (self.get_value(f.readline())).split(':')
            for time in line[0].split(','):
                self.eventsAt[int(time)] = self.eventsAt.get(
                    int(time), []) + [':'.join(line[1:])]
        f.close()

    def ReadOneTimeEvents(self, config_obj: ReadConfiguration, locations_obj: ReadLocations, agents_obj: ReadAgents) -> None:
        """
        Reads one time event information if it takes place at the current time step.

        Args:
            config_obj: An object of class :class:`~episimmer.read_file.ReadConfiguration` containing all configurations
            locations_obj: An object of class :class:`~episimmer.read_file.ReadLocations` containing all locations
            agents_obj: An object of class :class:`~episimmer.read_file.ReadAgents` containing all agents
        """
        if self.filename == '' or self.filename == None:
            return
        self.config_obj: ReadConfiguration = config_obj
        self.locations_obj: ReadLocations = locations_obj
        self.agents_obj: ReadLocations = agents_obj
        if self.event_info_keys != 'Time Step:' + config_obj.event_info_keys:
            raise Exception(
                'Error! One Time Event parameters do not match the config.txt file'
            )
        for event in self.eventsAt.get(Time.get_current_time_step(), []):
            parameter_list = (self.get_value(event)).split(':')
            location_index, info_dict = self.get_event(parameter_list)
            self.locations_obj.locations[location_index].add_event(info_dict)

    def get_event(self, parameter_list: List[str]) -> Tuple[str, Dict[str, Union[str, List[str]]]]:
        """
        Creates a dictionary for a location containing information about the one time event taking place at that location.

        Args:
            parameter_list: List containing time steps at which the one time event takes place, index of the location and agent indices
            of the agents part of the event.
        
        Returns: Location index and information dictionary of the location.

        """
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