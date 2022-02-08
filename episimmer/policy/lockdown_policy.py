from typing import Callable, Dict, List, Union, ValuesView

from episimmer.agent import Agent
from episimmer.location import Location
from episimmer.model import BaseModel

from .base import AgentPolicy
from .contact_tracing_policy import CTPolicy
from .testing_policy import TestPolicy


class LockdownPolicy(AgentPolicy):
    """
    Base class for implementing the lockdown policy.

    Args:
        do_lockdown_fn: User-defined function to specify which time step(s) to enforce lockdown in
        p: Probability of agent to contribute and receive infection from any source of infection
    """
    def __init__(self, do_lockdown_fn: Callable, p: float):
        super().__init__()
        self.policy_type: str = 'Restrict'
        self.do_lockdown_fn: Callable = do_lockdown_fn
        self.p: float = p

    def lockdown_agent(self, agent: Agent) -> None:
        """
        Updates the agent's probability to contribute and receive infection.

        Args:
            agent: Current agent
        """
        agent.update_receive_infection(self.p)
        agent.update_contribute_infection(self.p)


class FullLockdown(LockdownPolicy):
    """
    Class for implementing a lockdown policy common for all agents.
    Inherits :class:`LockdownPolicy` class.

    Args:
        do_lockdown_fn: User-defined function to specify which time step(s) to enforce lockdown in
        p: Probability of agent to contribute and receive infection from any source of infection
    """
    def __init__(self, do_lockdown_fn: Callable, p: float = 0.0):
        super().__init__(do_lockdown_fn, p)

    def enact_policy(self,
                     time_step: int,
                     agents: Dict[str, Agent],
                     locations: ValuesView[Location],
                     model: Union[BaseModel, None] = None,
                     policy_index: Union[int, None] = None) -> None:
        """
        If lockdown policy is enforced in the current time step, it restricts all agents from receiving and
        contributing disease.

        Args:
            time_step: Current time step
            agents: Dictionary mapping from agent indices to :class:`~episimmer.agent.Agent` objects
            locations: Collection of :class:`~episimmer.location.Location` objects
            model: Disease model specified by the user
            policy_index: Policy index passed to differentiate policies
        """
        if self.do_lockdown_fn(time_step):
            agents = agents.values()
            for agent in agents:
                self.lockdown_agent(agent)


class AgentLockdown(LockdownPolicy):
    """
    Class for implementing the lockdown policy for agents based on a fixed attribute of the agent.
    Inherits :class:`~episimmer.policy.lockdown_policy.LockdownPolicy` class.

    Args:
        attribute: Parameter (attribute) type of agents
        value_list: List of attribute values of agents
        do_lockdown_fn: User-defined function to specify which time step(s) to enforce lockdown in
        p: Probability of agent to contribute and receive infection from any source of infection
    """
    def __init__(self,
                 attribute: str,
                 value_list: List[str],
                 do_lockdown_fn: Callable,
                 p: float = 0.0):
        super().__init__(do_lockdown_fn, p)
        self.attribute: str = attribute
        self.value_list: List[str] = value_list
        super().__init__(do_lockdown_fn, p)

    def enact_policy(self,
                     time_step: int,
                     agents: Dict[str, Agent],
                     locations: ValuesView[Location],
                     model: Union[BaseModel, None] = None,
                     policy_index: Union[int, None] = None) -> None:
        """
       If lockdown policy is enforced in the current time step, it restricts a subset of agents from receiving and
       contributing disease. The agents selected are based on an agent attribute and the value list for that attribute.

        Args:
            time_step: Current time step
            agents: Dictionary mapping from agent indices to :class:`~episimmer.agent.Agent` objects
            locations: Collection of :class:`~episimmer.location.Location` objects
            model: Disease model specified by the user
            policy_index: Policy index passed to differentiate policies
        """
        if self.do_lockdown_fn(time_step):
            agents = agents.values()
            for agent in agents:
                if agent.info[self.attribute] in self.value_list:
                    self.lockdown_agent(agent)


class TestingBasedLockdown(LockdownPolicy):
    """
    Class for implementing the lockdown policy for agents taking into account their test results. This policy also
    handles locking down contacts of positively tested agents.
    Inherits :class:`~episimmer.policy.lockdown_policy.LockdownPolicy` class.

    Args:
        do_lockdown_fn: User-defined function to specify which time steps to enforce lockdown in
        time_period: Number of time steps for which an agent has to lock down
        contact_tracing: Boolean specifying whether lockdown for contacts of positively tested agents is enabled or not
        p: Probability of agent to contribute and receive infection from any source of infection
    """
    def __init__(self,
                 do_lockdown_fn: Callable,
                 time_period: int,
                 contact_tracing: bool = False,
                 p: float = 0.0):
        super().__init__(do_lockdown_fn, p)
        self.time_period: int = time_period
        self.contact_tracing: bool = contact_tracing

    def enact_policy(self,
                     time_step: int,
                     agents: Dict[str, Agent],
                     locations: ValuesView[Location],
                     model: Union[BaseModel, None] = None,
                     policy_index: Union[int, None] = None) -> None:
        """
        If lockdown policy is enforced in the current time step, it restricts positively tested agents from receiving
        and contributing disease. If contact tracing is enabled, contacts of positively tested agents are also
        lockdown.

        Args:
            time_step: Current time step
            agents: Dictionary mapping from agent indices to :class:`~episimmer.agent.Agent` objects
            locations: Collection of :class:`~episimmer.location.Location` objects
            model: Disease model specified by the user
            policy_index: Policy index passed to differentiate policies
        """
        if self.contact_tracing:
            CTPolicy.reduce_agents_schedule_time(agents)
        if self.do_lockdown_fn(time_step):
            self.lockdown_positive_agents(agents, time_step)
            if self.contact_tracing:
                self.lockdown_contacts(agents)

    def lockdown_positive_agents(self, agents: Dict[str, Agent],
                                 time_step: int) -> None:
        """
        Locks down positively tested agents. If contact tracing is enabled, contacts of positively tested agents
        are lockdown for a fixed time period. Each contact will save this period as a scheduled time left for lockdown
        and this value is reduced each time step.

        Args:
            agents: Dictionary mapping from agent indices to :class:`~episimmer.agent.Agent` objects
            time_step: Current time step
        """
        for agent in agents.values():
            result = TestPolicy.get_agent_test_result(
                agent, time_step, self.time_period)  # The number of time steps
            # an agent must be lockdown is considered to be the same as the number of time steps a test is valid.
            if result == 'Positive':
                self.lockdown_agent(agent)
                if self.contact_tracing:
                    policy_index_list = CTPolicy.get_policy_index_list(agent)
                    for policy_index in policy_index_list:
                        contacts = CTPolicy.get_contact_list(
                            agent, policy_index)
                        if contacts:
                            CTPolicy.set_contacts_schedule_time(
                                agents, contacts, policy_index,
                                self.time_period)

    def lockdown_contacts(self, agents: Dict[str, Agent]) -> None:
        """
        Locks down a contact if its scheduled time left for lockdown is greater than 0.

        Args:
            agents: Collection of :class:`~episimmer.agent.Agent` objects.
        """
        for agent in agents.values():
            max_schedule_time = CTPolicy.get_max_schedule_time(agent)
            if max_schedule_time > 0:
                self.lockdown_agent(agent)
