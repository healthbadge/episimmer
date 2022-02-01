import copy
from typing import Callable, Dict, List, Union, ValuesView, Set, Deque

from .base import AgentPolicy
from episimmer.agent import Agent
from episimmer.location import Location
from episimmer.model import BaseModel

class LockdownPolicy(AgentPolicy):
    """
    Base class for implementing the lockdown policy.

    Args:
        do_lockdown_fn: User-defined function to specify which time steps to enforce lockdown in.
        p: Measure of how much the agent's contribution to and reception of the infection is influenced by lockdown.
    """
    def __init__(self, do_lockdown_fn: Callable, p: float):
        self.policy_type: str = 'Restrict'
        self.do_lockdown_fn: Callable = do_lockdown_fn
        self.p: float = p

    def lockdown_agent(self, agent: Agent):
        """
        Updates the agent's contribution to and reception of infection.

        Args:
            agent: Agent whose contribution to and reception of infection is updated.
        """
        agent.update_recieve_infection(self.p)
        agent.update_contribute_infection(self.p)


class FullLockdown(LockdownPolicy):
    """
    Class for implementing the lockdown policy for all agents.
    Inherits :class:`~episimmer.policy.lockdown_policy.LockdownPolicy` class.

    Args:
        do_lockdown_fn: User-defined function to specify which time steps to enforce lockdown in.
        p: Measure of how much the agent's contribution to and reception of the infection is influenced by lockdown.
    """
    def __init__(self, do_lockdown_fn: Callable, p: float=0.0):
        super().__init__(do_lockdown_fn, p)

    def enact_policy(self,
                     time_step: int,
                     agents: Dict[str, Agent],
                     locations: ValuesView[Location],
                     model: Union[BaseModel, None] =None,
                     policy_index: int=None):
        """
        If lockdown policy is enforced in the time step, it lockdowns all agents.

        Args:
            time_step: Time step in which the policy is enacted.
            agents: Collection of :class:`~episimmer.agent.Agent` objects.
            locations: Collection of :class:`~episimmer.location.Location` objects.
            model: Disease model specified by the user.
            policy_index: Policy index passed to differentiate policies.
        """
        if self.do_lockdown_fn(time_step):
            agents = agents.values()
            for agent in agents:
                self.lockdown_agent(agent)


class AgentLockdown(LockdownPolicy):
    """
    Class for implementing the lockdown policy for a select set of agents.
    Inherits :class:`~episimmer.policy.lockdown_policy.LockdownPolicy` class.

    Args:
        parameter: Parameter (attribute) type of agents.
        value_list: List of attribute values of agents.
        do_lockdown_fn: User-defined function to specify which time steps to enforce lockdown in.
        p: Measure of how much the agent's contribution to and reception of the infection is influenced by lockdown.
    """
    def __init__(self, parameter: Union[str, None], value_list: List[str], do_lockdown_fn: Callable, p: float=0.0):
        super().__init__(do_lockdown_fn, p)
        self.parameter: Union[str, None] = parameter
        self.value_list: List[str] = value_list

    def enact_policy(self,
                     time_step: int,
                     agents: Dict[str, Agent],
                     locations: ValuesView[Location],
                     model: Union[BaseModel, None]=None,
                     policy_index: int=None):
        """
        If lockdown policy is enforced in the time step, it lockdowns select set of agents according to value list.

        Args:
            time_step: Time step in which the policy is enacted.
            agents: Collection of :class:`~episimmer.agent.Agent` objects.
            locations: Collection of :class:`~episimmer.location.Location` objects.
            model: Disease model specified by the user.
            policy_index: Policy index passed to differentiate policies.
        """
        if self.do_lockdown_fn(time_step):
            agents = agents.values()
            for agent in agents:
                if agent.info[self.parameter] in self.value_list:
                    self.lockdown_agent(agent)


class TestingBasedLockdown(LockdownPolicy):
    """
    Class for implementing the lockdown policy for agents taking into account positively tested agents and their contacts.
    Inherits :class:`~episimmer.policy.lockdown_policy.LockdownPolicy` class.

    Args:
        do_lockdown_fn: User-defined function to specify which time steps to enforce lockdown in.
        time_period: Number of time steps for which a test is valid, or, for which an agent has to lock down.
        contact_tracing: Boolean which specifies whether contact tracing is enabled or not.
        p: Measure of how much the agent's contribution to and reception of the infection is influenced by lockdown.
    """
    def __init__(self,
                 do_lockdown_fn: Callable,
                 time_period: int,
                 contact_tracing: bool=False,
                 p: float=0.0):
        super().__init__(do_lockdown_fn, p)
        self.time_period: int = time_period
        self.contact_tracing: bool = contact_tracing

    def enact_policy(self,
                     time_step: int,
                     agents: Dict[str, Agent],
                     locations: ValuesView[Location],
                     model: Union[BaseModel, None] =None,
                     policy_index: int =None):
        """
        Reduces scheduled time of agents. If lockdown policy is enforced in the time step, it lockdowns positive agents and their 
        contacts as well if contact tracing is enabled.

        Args:
            time_step: Time step in which the policy is enacted.
            agents: Collection of :class:`~episimmer.agent.Agent` objects.
            locations: Collection of :class:`~episimmer.location.Location` objects.
            model: Disease model specified by the user.
            policy_index: Policy index passed to differentiate policies.
        """
        self.reduce_agent_schedule_time(agents)
        if self.do_lockdown_fn(time_step):
            self.lockdown_positive_agents(agents, time_step)
            if self.contact_tracing:
                self.lockdown_contacts(agents)

    def reduce_agent_schedule_time(self, agents: Dict[str, Agent]):
        """
        Reduces the scheduled time for all agents across all contact tracing policies.

        Args:
            agents: Collection of :class:`~episimmer.agent.Agent` objects.
        """
        for agent in agents.values():
            agent_ct_state = agent.get_policy_state('Contact_Tracing')
            if agent_ct_state is not None:
                for ct_policy_index in agent_ct_state.keys():
                    self.reduce_schedule_time(agent, agent_ct_state,
                                              ct_policy_index)

    def reduce_schedule_time(self, agent: Agent, policy_state: Dict[int, Dict[str, Union[int, Deque[int]]]], policy_num: int):
        """
        If the agent's scheduled time is positive, this function decrements its scheduled time by 1.

        Args:
            agent: Agent whose scheduled time is to be decremented
            policy_state: State of the contact tracing policy of the agent
            policy_num: Policy index of the contact tracing policy
        """
        agent_ct_scheduled_time = policy_state[policy_num]['schedule_time']
        if agent_ct_scheduled_time > 0:
            policy_state[policy_num]['schedule_time'] -= 1

    def lockdown_positive_agents(self, agents: Dict[str, Agent], time_step: int):
        """
        Locks down the positively tested agents and resets the scheduled time of their contacts.

        Args:
            agents: Collection of :class:`~episimmer.agent.Agent` objects.
            time_step: Time step in which the policy is enacted.
        """
        for agent in agents.values():
            result = self.get_agent_test_result(agent, time_step)
            if (result == 'Positive'):
                self.lockdown_agent(agent)
                if (self.contact_tracing):
                    contacts = self.obtain_contact_set(agent)
                    if contacts:
                        self.set_schedule_time(agents, contacts)

    def get_agent_test_result(self, agent: Agent, time_step: int):
        """
        Gets the result of most recently conducted test on the agent from its testing history if its validity still holds in the 
        curent time step.

        Args:
            agent: Agent whose most recent test result is returned.
            time_step: Time step in which the policy is enacted.

        Returns:
            Result of most recent test of the agent whose validity holds in the current time step.
        """
        history = agent.get_policy_history('Testing')
        if (len(history)):
            last_time_step = history[-1].time_step
            if (time_step - last_time_step < self.time_period):
                result = self.get_accumulated_test_result(
                    history, last_time_step)
                return result
        return None

    def get_accumulated_test_result(self, history: Dict[str, Union[str, List[str], List[int]]], last_time_step: int):
        """
        Gets the test result from the last time step that the agent was tested in.

        Args:
            history: Agent's testing history information.
            last_time_step: Most recent time step in which agent was tested.

        Returns:
            Result of most recent test of the agent
        """
        indx = len(history) - 1
        while (indx >= 0 and history[indx].time_step == last_time_step):
            if (history[indx].result == 'Negative'):
                return 'Negative'
            indx -= 1
        return 'Positive'

    def obtain_contact_set(self, agent: Agent):
        """
        Finds set of contacts of an agent across all contact tracing policies.

        Args:
            agent: Agent whose contacts are to be found.

        Returns:
            Set of all contacts of the agent across all contact tracing policies.
        """
        agent_ct_state = agent.get_policy_state('Contact_Tracing')
        contacts = set()
        if agent_ct_state is not None:
            for ct_policy_index in agent_ct_state.keys():
                if 'contact_deque' in agent_ct_state[ct_policy_index].keys():
                    contacts_deque = agent_ct_state[ct_policy_index][
                        'contact_deque']
                    for contact in contacts_deque:
                        contacts = contacts.union(set(contact))
        return contacts

    def set_schedule_time(self, agents: Dict[str, Agent], contacts: Set[str]):
        """
        Sets the scheduled time of contacts of positive agent as time period of the lockdown policy if the scheduled time of the 
        contact is 0.

        Args:
            agents: Collection of :class:`~episimmer.agent.Agent` objects.
            contacts: Set of all contacts of an agent across all contact tracing policies.
        """
        for contact_index in contacts:
            contact_agent = agents[contact_index]
            contact_ct_state = contact_agent.get_policy_state(
                'Contact_Tracing')
            for contact_ct_policy_index in contact_ct_state.keys():
                if contact_ct_state[contact_ct_policy_index][
                        'schedule_time'] == 0:
                    contact_ct_state[contact_ct_policy_index][
                        'schedule_time'] = self.time_period

    def lockdown_contacts(self, agents: Dict[str, Agent]):
        """
        Locks down a contact if its scheduled time is greater than 0.

        Args:
            agents: Collection of :class:`~episimmer.agent.Agent` objects.
        """
        for agent in agents.values():
            max_schedule_time = 0
            agent_ct_policy = agent.get_policy_state('Contact_Tracing')
            if agent_ct_policy is not None:
                for policy_index in agent_ct_policy.keys():
                    agent_ct_scheduled_time = agent_ct_policy[policy_index][
                        'schedule_time']
                    if agent_ct_scheduled_time is not None:
                        max_schedule_time = max(max_schedule_time,
                                                agent_ct_scheduled_time)
                if max_schedule_time > 0:
                    self.lockdown_agent(agent)
