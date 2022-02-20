import random
from typing import Dict, List, Union

import networkx as nx

from episimmer.agent import Agent
from episimmer.model import BaseModel
from episimmer.policy.base import Policy

from .read_file import (ReadAgents, ReadConfiguration, ReadEvents,
                        ReadInteractions, ReadLocations, ReadOneTimeEvents,
                        ReadProbabilisticInteractions)
from .utils.statistics import save_stats
from .utils.time import Time
from .utils.visualize import save_env_graph, store_animated_dynamic_graph


class Simulate():
    """
    Class for handling a simulation. It takes care of all the steps throughout a simulation run.

    Args:
        config_obj: A dictionary containing information from the config file of the example.
        model: Disease model specified by the user
        policy_list: List of all the policies part of the simulation
        agents_obj: An object of class :class:`~episimmer.read_file.ReadAgents`
        locations_obj: An object of class :class:`~episimmer.read_file.ReadLocations`
    """
    def __init__(self, config_obj: ReadConfiguration, model: BaseModel,
                 policy_list: List[Policy], agents_obj: ReadAgents,
                 locations_obj: ReadLocations):
        self.agents_obj: ReadAgents = agents_obj
        self.locations_obj: ReadLocations = locations_obj
        self.model: BaseModel = model
        self.policy_list: List[Policy] = policy_list
        self.config_obj: ReadConfiguration = config_obj
        self.g_list: List[nx.Graph] = []
        self.state_list: Dict[str, List[str]] = {}
        self.state_history: Dict[str, List[int]] = {}

    def on_start_simulation(self) -> None:
        """
        Function to initialize agent states, reset policies and initialize the state list and history,
        """
        # Initialize state list
        for state in self.model.individual_state_types:
            self.state_list[state] = []
            self.state_history[state] = []

        # Initialize states
        self.model.initialize_states(self.agents_obj.agents)

        # Reset Policies
        for policy_index, policy in enumerate(self.policy_list):
            policy.reset(self.agents_obj.agents.values(),
                         self.locations_obj.locations.values(), self.model,
                         policy_index)

        # Update State list
        for agent in self.agents_obj.agents.values():
            self.state_list[agent.state].append(agent.index)

        # Store state list
        self.store_state()

    @save_env_graph()
    @save_stats([('agents_obj', 3)], 'Agents', ['state'])
    def on_start_time_step(self,
                           interaction_files_list_of_list: List[List[str]],
                           event_files_list_of_list: List[List[str]],
                           probabilistic_interaction_files_list_of_list: List[
                               List[str]],
                           one_time_event_obj: ReadOneTimeEvents) -> None:
        """
        Function to reset agents and locations for a new time step, to load all the types of interactions from their
        respective files and to run policies. Policies are run in two steps here. First, the policies that are
        independent of all the interactions and events present are run with the `enact_policy` method and the policies
        that do depend on them are run with `post_policy` method. After the policy is finished running, all types of
        events are handled by saving the probability of infection for each agent.


        Args:
            interaction_files_list_of_list: List of path names of all the interactions files
            event_files_list_of_list: List of path names of all the events files
            probabilistic_interaction_files_list_of_list: List of path names of all the probabilistic interactions files
            one_time_event_obj: An object of class :class:`~episimmer.read_file.ReadOneTimeEvents`
        """

        for agent in self.agents_obj.agents.values():
            agent.new_time_step()

        for location in self.locations_obj.locations.values():
            location.new_time_step()

        # Initialize filenames
        interactions_filename = events_filename = None

        # Load interactions
        for interaction_files_list in interaction_files_list_of_list:
            if interaction_files_list:
                interactions_filename = interaction_files_list[
                    Time.get_current_time_step() % len(interaction_files_list)]
                ReadInteractions(interactions_filename, self.config_obj,
                                 self.agents_obj)

        # Load probabilistic interactions
        for probabilistic_interaction_files_list in probabilistic_interaction_files_list_of_list:
            if probabilistic_interaction_files_list:
                probabilistic_interactions_filename = probabilistic_interaction_files_list[
                    Time.get_current_time_step() %
                    len(probabilistic_interaction_files_list)]
                ReadProbabilisticInteractions(
                    probabilistic_interactions_filename, self.config_obj,
                    self.agents_obj)

        # Load Events
        for event_files_list in event_files_list_of_list:
            if event_files_list:
                events_filename = event_files_list[
                    Time.get_current_time_step() % len(event_files_list)]
                ReadEvents(events_filename, self.config_obj,
                           self.locations_obj, self.agents_obj)

        # Load One Time Events
        one_time_event_obj.populate_one_time_events(
            self.config_obj, self.locations_obj, self.agents_obj,
            Time.get_current_time_step())

        # Enact policies by updating agent and location states.
        for policy_index, policy in enumerate(self.policy_list):
            policy.enact_policy(Time.get_current_time_step(),
                                self.agents_obj.agents,
                                self.locations_obj.locations.values(),
                                self.model, policy_index)

        # Restrict agents with can_contribute_infection and can_receive_infection
        # All interactions and events restricted by removing elements in
        # agent.contact_list and location.events
        self.save_valid_interactions_events()

        # Enact post-policy procedures after saving all types of interactions.
        for policy_index, policy in enumerate(self.policy_list):
            policy.post_policy(Time.get_current_time_step(),
                               self.agents_obj.agents,
                               self.locations_obj.locations.values(),
                               self.model, policy_index)

        if events_filename is not None:
            # Update event info to agents from location
            for location in self.locations_obj.locations.values():
                if not location.lock_down_state:
                    for event_info in location.events:
                        self.model.update_event_infection(
                            event_info, location, self.agents_obj)

    def handle_time_step_for_all_agents(self) -> None:
        """
        Find the next state and save it for every agent, and then convert each agent's current state to the saved next
        state.
        """
        for agent in self.agents_obj.agents.values():
            self.handle_time_step_as_agent(agent)

        for agent in self.agents_obj.agents.values():
            self.convert_state(agent)

    def handle_time_step_as_agent(self, agent: Agent) -> None:
        """
       Finds the next state and save it for the agent

        Args:
            agent: Agent whose next state is to be set
        """
        agent.set_next_state(
            self.model.find_next_state(agent, self.agents_obj.agents))

    def end_time_step(self) -> None:
        """
        Stores the state of the simulation at the end of the time step.
        """
        self.store_state()

    def valid_interaction(self, agent: Agent, c_dict: Dict[str, str]) -> bool:
        """
        Checks whether the contact of an agent will interact with the agent. If the current agent is under the
        protection of a vaccine, the contact is said to not occur. Other factors include variables set by lockdown
        (restriction) policies that change the probability of the current agent locking himself down. This is done
        with the `can_contribute_infection` and `can_receive_infection` variables.

        Args:
            agent: The current agent
            c_dict: Contact dictionary of the agent

        Returns:
            Boolean representing whether the interaction will take place or not.
        """
        if agent.under_protection:
            return False

        r = random.random()
        contact_index = c_dict['Interacting Agent Index']
        contact_agent = self.agents_obj.agents[contact_index]
        if r < contact_agent.can_contribute_infection and r < agent.can_receive_infection:
            return True
        return False

    def store_event_lists(
            self, event_info: Dict[str, Union[float, str, List[str]]]) -> None:
        """
        Checks whether agents part of an event can contribute infection to the event or receive infection from
        the event or both. This function saves the agents that can do either in the event_info dictionary,

        Args:
            event_info: A dictionary containing event information at a location that contains all the agents part of
            the event.
        """
        r = random.random()
        if r < event_info['_prob_of_occur']:
            for agent_index in event_info['Agents']:
                r = random.random()
                agent = self.agents_obj.agents[agent_index]

                if r < agent.can_contribute_infection:
                    event_info['_can_contrib'].append(agent_index)

                if not agent.under_protection and r < agent.can_receive_infection:
                    event_info['_can_receive'].append(agent_index)

    def save_valid_interactions_events(self) -> None:
        """
        Saves all the valid interactions and events in the current time step of the simulation.
        """
        for agent in self.agents_obj.agents.values():
            agent.contact_list[:] = [
                c_dict for c_dict in agent.contact_list
                if self.valid_interaction(agent, c_dict)
            ]

        for location in self.locations_obj.locations.values():
            for event_info in location.events:
                self.store_event_lists(event_info)

    @store_animated_dynamic_graph()
    def end_simulation(self) -> Dict[str, List[int]]:
        """
        Returns the state history at the end of the simulation.
        """
        return self.state_history

    def store_state(self) -> None:
        """
        Stores the number of agents in each state in the state history at each time step.
        """
        for state in self.state_history.keys():
            self.state_history[state].append(len(self.state_list[state]))

    def convert_state(self, agent: Agent) -> None:
        """
        Updates the state list when an agent transitions from one state to another.

        Args:
            agent: Agent whose next state is to be set
        """
        self.state_list[agent.state].remove(agent.index)
        agent.update_state()
        self.state_list[agent.state].append(agent.index)
