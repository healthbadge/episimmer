from typing import Callable, Dict, List, Union, ValuesView

from episimmer.agent import Agent
from episimmer.location import Location
from episimmer.model import BaseModel

from .base import AgentPolicy, EventPolicy
from .contact_tracing_policy import CTPolicy
from .testing_policy import TestPolicy


class AgentLockdownPolicy(AgentPolicy):
    """
    Base class for implementing the lockdown policy for agents.
    Inherits :class:`~episimmer.policy.base.AgentPolicy` class.

    Args:
        do_lockdown_fn: User-defined function to specify which time step(s) to enforce lockdown in
        p: Probability of agent to contribute and receive infection from any source of infection under lockdown
    """
    def __init__(self, do_lockdown_fn: Callable, p: float):
        super().__init__('Restrict')
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


class FullLockdown(AgentLockdownPolicy):
    """
    Class for implementing a lockdown policy common for all agents.
    Inherits :class:`AgentLockdownPolicy` class.

    An example of a GeneratePolicy.py file illustrating full lockdown policy where all agents are lockdown on
    alternate days is given below

    .. code-block:: python
            :linenos:

            from episimmer.policy import lockdown_policy

            def generate_policy():
                policy_list=[]

                def lockdown_fn(time_step):
                    if time_step % 2 == 0:
                        return True

                    return False

                policy_list.append(lockdown_policy.FullLockdown(lockdown_fn))

                return policy_list

    Args:
        do_lockdown_fn: User-defined function to specify which time step(s) to enforce lockdown in
        p: Probability of agent to contribute and receive infection from any source of infection under lockdown
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


class AgentLockdown(AgentLockdownPolicy):
    """
    Class for implementing the lockdown policy for agents based on a fixed attribute of the agent.
    Inherits :class:`~episimmer.policy.lockdown_policy.AgentLockdownPolicy` class.

    An example of a GeneratePolicy.py file illustrating an agent lockdown policy where agents are lockdown
    based on their Grade attribute

    .. code-block:: python
            :linenos:

            from episimmer.policy import lockdown_policy

            def generate_policy():
                policy_list=[]

                def lockdown_fn(time_step):
                    return True

                policy_list.append(lockdown_policy.AgentLockdown('Grade',['Grade 1'],lockdown_fn))

                return policy_list

    Args:
        attribute: Parameter (attribute) type of agents
        value_list: List of attribute values of agents
        do_lockdown_fn: User-defined function to specify which time step(s) to enforce lockdown in
        p: Probability of agent to contribute and receive infection from any source of infection under lockdown
    """
    def __init__(self,
                 attribute: str,
                 value_list: List[str],
                 do_lockdown_fn: Callable,
                 p: float = 0.0):
        super().__init__(do_lockdown_fn, p)
        self.attribute: str = attribute
        self.value_list: List[str] = value_list

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


class TestingBasedLockdown(AgentLockdownPolicy):
    """
    Class for implementing the lockdown policy for agents taking into account their test results. This policy also
    handles locking down contacts of positively tested agents.
    Inherits :class:`~episimmer.policy.lockdown_policy.AgentLockdownPolicy` class.

    An example of a GeneratePolicy.py file illustrating locking down positively tested agents for a period of 10 days
    is given below

    .. code-block:: python
            :linenos:

            from episimmer.policy import lockdown_policy, testing_policy

            def generate_policy():
                policy_list=[]

                Normal_Test = testing_policy.TestPolicy(lambda x:60)
                Normal_Test.add_machine('Simple_Machine', 200, 0.0, 0.0, 0, 50, 3, 2)
                Normal_Test.set_register_agent_testtube_func(Normal_Test.random_testing())
                policy_list.append(Normal_Test)

                ATP = lockdown_policy.TestingBasedLockdown(lambda x:True,10)
                policy_list.append(ATP)

                return policy_list

    An example of a GeneratePolicy.py file illustrating locking down positively tested agents along with their contacts
    for a period of 2 days is given below

    .. code-block:: python
            :linenos:

            from episimmer.policy import (contact_tracing_policy, lockdown_policy,
                                          testing_policy)

            def generate_policy():
                policy_list=[]
                Normal_Test = testing_policy.TestPolicy(lambda x:7)
                Normal_Test.add_machine('Simple_Machine', 200, 0.0, 0.0, 0, 50, 3, 2)
                Normal_Test.set_register_agent_testtube_func(Normal_Test.random_testing())
                policy_list.append(Normal_Test)

                CT_object = contact_tracing_policy.CTPolicy(7)
                policy_list.append(CT_object)

                Lockdown_object = lockdown_policy.TestingBasedLockdown(lambda x:True, 2, True)
                policy_list.append(Lockdown_object)

                return policy_list

    Args:
        do_lockdown_fn: User-defined function to specify which time steps to enforce lockdown in
        lockdown_period: Number of time steps for which an agent has to lock down
        contact_tracing: Boolean specifying whether lockdown for contacts of positively tested agents is enabled or not
        p: Probability of agent to contribute and receive infection from any source of infection under lockdown
    """
    def __init__(self,
                 do_lockdown_fn: Callable,
                 lockdown_period: int,
                 contact_tracing: bool = False,
                 p: float = 0.0):
        super().__init__(do_lockdown_fn, p)
        self.lockdown_period: int = lockdown_period
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
            result = TestPolicy.get_agent_test_result(agent, time_step)
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
                                self.lockdown_period)

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


class EventLockdownPolicy(EventPolicy):
    """
    Base class for implementing the lockdown policy for events.
    Inherits :class:`~episimmer.policy.base.EventPolicy` class.

    Args:
        do_lockdown_fn: User-defined function to specify which time step(s) to enforce lockdown in
        p: Probability of an event occurring during lockdown
    """
    def __init__(self, do_lockdown_fn: Callable, p: float):
        super().__init__('Restrict')
        self.do_lockdown_fn: Callable = do_lockdown_fn
        self.p: float = p

    def lockdown_event(
            self, event_info: Dict[str, Union[float, str, List[str]]]) -> None:
        """
        Updates the event's probability of occurring

        Args:
            event_info: A dictionary containing event information at a location that contains all the agents part of
            the event.
        """
        event_info['_prob_of_occur'] = self.p


class EventLockdown(EventLockdownPolicy):
    """
    Class for implementing the lockdown policy for events based on a fixed attribute of the event.
    Inherits :class:`~episimmer.policy.lockdown_policy.EventLockdownPolicy` class.

    An example of a GeneratePolicy.py file illustrating Event lockdown policy where events are lockdown based on an
    Event attribute. Here, Events of Type - Low Priority are lockdown.

    .. code-block:: python
            :linenos:

            from episimmer.policy import lockdown_policy, testing_policy

            def generate_policy():
                policy_list=[]

                event_lockdown = lockdown_policy.EventLockdown('Type', ['Low Priority'], lambda x: True)
                policy_list.append(event_lockdown)

                return policy_list

    Args:
        attribute: Parameter (attribute) type of events
        value_list: List of attribute values of events
        do_lockdown_fn: User-defined function to specify which time step(s) to enforce lockdown in
        p: Probability of an event occurring during lockdown
    """
    def __init__(self,
                 attribute: str,
                 value_list: List[str],
                 do_lockdown_fn: Callable,
                 p: float = 0.0):
        super().__init__(do_lockdown_fn, p)
        self.attribute: str = attribute
        self.value_list: List[str] = value_list

    def enact_policy(self,
                     time_step: int,
                     agents: Dict[str, Agent],
                     locations: ValuesView[Location],
                     model: Union[BaseModel, None] = None,
                     policy_index: Union[int, None] = None) -> None:
        """
        If lockdown policy is enforced in the current time step, it restricts a subset of events from occurring. The
        events selected are based on an event attribute and the value list for that attribute.

        Args:
            time_step: Current time step
            agents: Dictionary mapping from agent indices to :class:`~episimmer.agent.Agent` objects
            locations: Collection of :class:`~episimmer.location.Location` objects
            model: Disease model specified by the user
            policy_index: Policy index passed to differentiate policies
        """
        if self.do_lockdown_fn(time_step):
            for location in locations:
                for event_info in location.events:
                    if event_info[self.attribute] in self.value_list:
                        self.lockdown_event(event_info)
