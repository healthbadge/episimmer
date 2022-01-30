import copy
from typing import Callable, Dict, List, Union, ValuesView
from xmlrpc.client import Boolean
from collections import deque

from Healthbadge.episimmer.episimmer.agent import Agent
from Healthbadge.episimmer.episimmer.location import Location

from .base import AgentPolicy


class CTPolicy(AgentPolicy):
    """
    Class built to implement the contact tracing policy

    Args:
        num_of_days : Number of days upto which you need to store the agent's contacts.
        attribute : Used to implement contact tracing based on agent attribute if needed.
        value_list: List of attribute values of agents.
    """
    def __init__(self, num_of_days:int, attribute: Union[str,None]=None, value_list:List[str]=[]):
        super().__init__()
        self.policy_type:str = 'Contact_Tracing'
        self.num_of_days:int = num_of_days
        self.attribute:str = attribute
        self.value_list:List[str] = value_list

    def reset(self, agents:ValuesView[AgentPolicy], policy_index:str)->None:
        """
        Used to reset the states of the agents at the first time step of simulation.

        Args:
            agents: Collection of :class:`~episimmer.agent.Agent` objects.
            policy_index: the index of the ith contact tracing policy being run.
        """
        for agent in agents:
            agent_ct_state = self.get_agent_policy_state(agent)
            if agent_ct_state is None:
                self.update_agent_policy_state(agent, {})
                agent_ct_state = self.get_agent_policy_state(agent)
            agent_ct_state[policy_index] = {}
            agent_ct_state[policy_index]['schedule_time'] = 0
            if self.attribute is None or agent.info[
                    self.attribute] in self.value_list:
                agent_ct_state[policy_index]['contact_deque'] = deque(
                    maxlen=self.num_of_days)
    

    def post_policy(self, agents:Dict[str,Agent], locations:ValuesView[Location], policy_index:str)->None:
        """
        Runs all the methods that have to be called after saving valid interactions and events.

        Args:
            agents: Collection of :class:`~episimmer.agent.Agent` objects.
            locations: Collection of :class:`~episimmer.location.Location` objects.
            policy_index: the index of the ith contact tracing policy being run.
        """
        self.new_day(agents, policy_index)
        self.save_interactions(agents, policy_index)
        self.save_events(agents, locations, policy_index)

    def new_day(self, agents:Dict[str,Agent], policy_index:str)->None:
        """
        Adds the contacts for agents in that timestep.

        Args:
            agents: Collection of :class:`~episimmer.agent.Agent` objects.
            policy_index: the index of the ith contact tracing policy being run.
        """
        for agent in agents.values():
            if self.attribute is None or agent.info[
                    self.attribute] in self.value_list:
                agent_contact_set = set()
                agent_ct_state = self.get_agent_policy_state(agent)
                agent_ct_state[policy_index]['contact_deque'].append(
                    agent_contact_set)

    def save_interactions(self, agents:Dict[str,Agent], policy_index:str)->None:
        """
        Saving the contacts of the agent due to interactions.

        Args:
            agents: Collection of :class:`~episimmer.agent.Agent` objects.
            policy_index: the index of the ith contact tracing policy being run.
        """
        for agent_index in agents.keys():
            for contact_dict in agents[agent_index].contact_list:
                interacting_agent_index = contact_dict[
                    'Interacting Agent Index']
                if self.attribute is None or agents[
                        interacting_agent_index].info[
                            self.attribute] in self.value_list:
                    agent_ct_state = self.get_agent_policy_state(
                        agents[interacting_agent_index])
                    agent_ct_state[policy_index]['contact_deque'][-1].add(
                        agent_index)

    def save_events(self, agents:Dict[str,Agent], locations:ValuesView[Location], policy_index:str)->None:
        """
        Saving the contacts of agent via events.

        Args: 
            locations: Collection of :class:`~episimmer.location.Location` objects.
            policy_index: the index of the ith contact tracing policy being run.
        """
        for location in locations:
            for event_dict in location.events:
                for agent_index in event_dict['can_contrib']:
                    if self.attribute is None or agents[agent_index].info[
                            self.attribute] in self.value_list:
                        agent_ct_state = self.get_agent_policy_state(
                            agents[agent_index])
                        ct_deque = agent_ct_state[policy_index][
                            'contact_deque']
                        ct_deque[-1] = ct_deque[-1].union(
                            set(event_dict['can_receive']))
                        if agent_index in event_dict['can_receive']:
                            ct_deque[-1].remove(agent_index)
