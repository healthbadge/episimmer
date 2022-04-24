from typing import Dict, List, Tuple, Union

import numpy as np

from episimmer.model import BaseModel
from episimmer.policy.base import Policy

from .read_file import (ReadAgents, ReadConfiguration, ReadLocations,
                        ReadOneTimeEvents)
from .simulate import Simulate
from .utils.arg_parser import parse_args
from .utils.math import deep_copy_average, deep_copy_stddev
from .utils.time import Time
from .utils.visualize import plot_results, store_animated_time_plot


class World():
    """
    Class for implementing a simulation world.

    Args:
        config_obj: A dictionary containing information from the config file of the example.
        model: Disease model specified by the user
        policy_list: List of all the policies part of the simulation
        agents_filename: Name of the file that contains agents information
        interaction_files_list: List of path names of all the interactions list files
        probabilistic_interaction_files_list: List of path names of all the probabilistic interactions list files
        locations_filename: Name of the file that contains location information
        event_files_list: List of path names of all the events list files
        one_time_event_file: File name of the one time event
    """
    def __init__(self, config_obj: ReadConfiguration, model: BaseModel,
                 policy_list: List[Policy], agents_filename: str,
                 interaction_files_list: List[List[str]],
                 probabilistic_interaction_files_list: List[List[str]],
                 locations_filename: str, event_files_list: List[List[str]],
                 one_time_event_file: Union[str, None]):
        self.config_obj: ReadConfiguration = config_obj
        self.policy_list: List[Policy] = policy_list
        self.agents_filename: str = agents_filename
        self.locations_filename: str = locations_filename
        self.model: BaseModel = model
        self.interaction_files_list: List[List[str]] = interaction_files_list
        self.probabilistic_interaction_files_list: List[
            List[str]] = probabilistic_interaction_files_list
        self.event_files_list: List[List[str]] = event_files_list
        self.one_time_event_file: Union[str, None] = one_time_event_file

    def one_world(
            self) -> Tuple[Dict[str, List[int]], ReadAgents, ReadLocations]:
        """
        Runs a single simulation world

        Returns:
            State of the world at the end of a simulation, ReadAgents object, and ReadLocations object
        """

        time_steps = self.config_obj.time_steps

        Time.new_world()

        # Initialize agents
        agents_obj = ReadAgents(self.agents_filename, self.config_obj)

        # Initialize locations
        locations_obj = ReadLocations(self.locations_filename, self.config_obj)

        # Initialize one time events
        one_time_event_obj = ReadOneTimeEvents(self.one_time_event_file)

        sim_obj = Simulate(self.config_obj, self.model, self.policy_list,
                           agents_obj, locations_obj)
        sim_obj.on_start_simulation()

        for current_time_step in range(time_steps):
            sim_obj.on_start_time_step(
                self.interaction_files_list, self.event_files_list,
                self.probabilistic_interaction_files_list, one_time_event_obj)
            sim_obj.handle_time_step_for_all_agents()
            sim_obj.end_time_step()
            Time.increment_current_time_step()

        end_state = sim_obj.end_simulation()
        return end_state, agents_obj, locations_obj

    def simulate_worlds(self) -> Dict[str, List[float]]:
        """
        Simulates multiple worlds and saves the epidemic trajectory plot. It also plots it by default (which can be
        disabled with command line flags).

        Returns:
            Averaged epidemic trajectory dictionary
        """

        args = parse_args()
        plot = args.noplot
        anim = args.animate

        tdict = {}
        t2_dict = {}
        max_dict = {}
        min_dict = {}
        for state in self.model.individual_state_types:
            tdict[state] = [0] * (self.config_obj.time_steps + 1)
            t2_dict[state] = [0] * (self.config_obj.time_steps + 1)
            max_dict[state] = [0] * (self.config_obj.time_steps + 1)
            min_dict[state] = [np.inf] * (self.config_obj.time_steps + 1)

        for i in range(self.config_obj.worlds):
            sdict, _, _ = self.one_world()
            for state in self.model.individual_state_types:
                for j in range(len(tdict[state])):
                    tdict[state][j] += sdict[state][j]
                    t2_dict[state][j] += sdict[state][j]**2
                    max_dict[state][j] = max(max_dict[state][j],
                                             sdict[state][j])
                    min_dict[state][j] = min(min_dict[state][j],
                                             sdict[state][j])

        # Average number time series
        avg_dict = deep_copy_average(tdict, self.config_obj.worlds)
        stddev_dict = deep_copy_stddev(tdict, t2_dict, self.config_obj.worlds)
        plot_results(self.config_obj.example_path, self.model, avg_dict,
                     stddev_dict, max_dict, min_dict, plot)
        if anim:
            store_animated_time_plot(self.config_obj.example_path, self.model,
                                     avg_dict)

        return avg_dict
