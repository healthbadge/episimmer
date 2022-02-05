from typing import Callable, Dict, List, Tuple, Union

import numpy as np

from episimmer.model import BaseModel
from episimmer.read_file import (ReadAgents, ReadConfiguration, ReadEvents,
                                 ReadLocations, ReadOneTimeEvents)

from .read_file import ReadAgents, ReadLocations, ReadOneTimeEvents
from .simulate import Simulate
from .utils.arg_parser import parse_args
from .utils.math import deep_copy_average, deep_copy_stddev
from .utils.time import Time
from .utils.visualize import plot_results, store_animated_time_plot
from .policy.base import AgentPolicy


class World():
    """
    Class for storing the information of the world(s) run by simulations.
    Inherits :class:`~episimmer.policy.base.AgentPolicy` class.

    Args:
        config_obj: A dictionary containing information from the config file of the example.
        model: Disease model specified by the user
        policy_list: List of all the policies part of the simulation
        event_restriction_fn: User-defined function used to determine if an agent is restricted from participating in an event
        agents_filename: Name of the file that contains agents information
        interactionFiles_list: List of path names of all the interactions files
        probabilistic_interactionFiles_list: List of path names of all the prababilistic interactions files
        locations_filename: Name of the file that contains locations information
        eventFiles_list: List of path names of all the events files
        one_time_event_file: File name of the one time event
    """
    def __init__(self, config_obj: ReadConfiguration, model: BaseModel,
                 policy_list: List[AgentPolicy],
                 event_restriction_fn: Callable, agents_filename: str,
                 interactionFiles_list: List[List[str]],
                 probabilistic_interactionFiles_list: List[List[str]],
                 locations_filename: str, eventFiles_list: List[List[str]],
                 one_time_event_file: Union[str, None]):
        self.config_obj: ReadConfiguration = config_obj
        self.policy_list: List[AgentPolicy] = policy_list
        self.event_restriction_fn: Callable = event_restriction_fn
        self.agents_filename: str = agents_filename
        self.locations_filename: str = locations_filename
        self.model: BaseModel = model
        self.interactionFiles_list: List[List[str]] = interactionFiles_list
        self.probabilistic_interactionsFiles_list: List[
            List[str]] = probabilistic_interactionFiles_list
        self.eventFiles_list: List[List[str]] = eventFiles_list
        self.one_time_event_file: Union[str, None] = one_time_event_file

    def one_world(
            self) -> Tuple[Dict[str, List[int]], ReadAgents, ReadLocations]:
        """
        Starts and ends a simulation along with saving the state of the simulation at each time step.

        Returns:
            State of the world at the end of a simulation, result object of agent, and result object of location
        """

        time_steps = self.config_obj.time_steps

        Time.new_world()

        # Initialize agents
        agents_obj = ReadAgents(self.agents_filename, self.config_obj)

        # Intialize locations
        locations_obj = ReadLocations(self.locations_filename, self.config_obj)

        # Initialize one time events
        oneTimeEvent_obj = ReadOneTimeEvents(self.one_time_event_file)

        sim_obj = Simulate(self.config_obj, self.model, self.policy_list,
                           self.event_restriction_fn, agents_obj,
                           locations_obj)
        sim_obj.onStartSimulation()

        for current_time_step in range(time_steps):
            sim_obj.onStartTimeStep(self.interactionFiles_list,
                                    self.eventFiles_list,
                                    self.probabilistic_interactionsFiles_list,
                                    oneTimeEvent_obj)
            sim_obj.handleTimeStepForAllAgents()
            sim_obj.endTimeStep()
            Time.increment_current_time_step()

        end_state = sim_obj.endSimulation()
        return end_state, agents_obj, locations_obj

    def simulate_worlds(self) -> Dict[str, List[float]]:
        """
        Averages over multiple simulations and plots a single plot.

        Returns:
            Object of simulations averaged.
        """

        args = parse_args()
        plot = args.noplot
        anim = args.animate

        tdict = {}
        t2_dict = {}
        maxdict = {}
        mindict = {}
        for state in self.model.individual_state_types:
            tdict[state] = [0] * (self.config_obj.time_steps + 1)
            t2_dict[state] = [0] * (self.config_obj.time_steps + 1)
            maxdict[state] = [0] * (self.config_obj.time_steps + 1)
            mindict[state] = [np.inf] * (self.config_obj.time_steps + 1)

        for i in range(self.config_obj.worlds):
            sdict, _, _ = self.one_world()
            for state in self.model.individual_state_types:
                for j in range(len(tdict[state])):
                    tdict[state][j] += sdict[state][j]
                    t2_dict[state][j] += sdict[state][j]**2
                    maxdict[state][j] = max(maxdict[state][j], sdict[state][j])
                    mindict[state][j] = min(mindict[state][j], sdict[state][j])

        # Average number time series
        avg_dict = deep_copy_average(tdict, self.config_obj.worlds)
        stddev_dict = deep_copy_stddev(tdict, t2_dict, self.config_obj.worlds)
        plot_results(self.config_obj.example_path, self.model, avg_dict,
                     stddev_dict, maxdict, mindict, plot)
        if anim:
            store_animated_time_plot(self.config_obj.example_path, self.model,
                                     avg_dict)
        return avg_dict
