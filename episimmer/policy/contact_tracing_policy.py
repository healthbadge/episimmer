from collections import deque
from typing import Deque, Dict, List, Union, ValuesView

from episimmer.agent import Agent
from episimmer.location import Location
from episimmer.model import BaseModel

from .base import AgentPolicy


class ContactList():
    """
    Class built to implement an ordered and unique list of contacts
    """
    def __init__(self):
        self.contacts: List[str] = []

    def add_contact(self, contact: str) -> None:
        """
        Adds a contact to the contact list

        Args:
            contact: Contact to be added
        """
        self.contacts.append(contact)
        self.contacts = list(dict.fromkeys(self.contacts))

    def remove_contact(self, contact: str) -> None:
        """
        Removes a contact from the contact list

        Args:
            contact: Contact to be removed
        """
        self.contacts.remove(contact)

    def union_contacts(self, contact_list_obj: 'ContactList') -> 'ContactList':
        """
        Performs a union operation between two ContactList objects and returns a new ContactList object.

        Args:
            contact_list_obj: A :class:`ContactList` object used to perform union operation

        Returns:
            A new ContactList object
        """
        union_obj = ContactList()
        for contact in self.contacts:
            union_obj.add_contact(contact)

        for contact in contact_list_obj.contacts:
            union_obj.add_contact(contact)

        return union_obj

    def __repr__(self) -> str:
        """
        Shows the representation of the object as the contact list

        Returns:
            The list of contacts in string format
        """
        return str(self.contacts)


class CTPolicy(AgentPolicy):
    """
    Class built to implement the contact tracing policy. Agent contacts are saved based on all types of interactions
    in Episimmer. You can optionally choose the agents that save their contacts by passing an agent attribute and
    a value list.
    Inherits :class:`~episimmer.policy.base.AgentPolicy` class.

    An example of a GeneratePolicy.py file illustrating contact tracing policy is given below. It saves contacts for
    agents of Type Teacher and Student for a period of 7 and 3 time steps respectively.

    .. code-block:: python
            :linenos:

            from episimmer.policy import contact_tracing_policy

            def generate_policy():
                policy_list=[]

                CT_object = contact_tracing_policy.CTPolicy(7, 'Type', ['Teacher'])
                CT_object2 = contact_tracing_policy.CTPolicy(3, 'Type', ['Student'])

                policy_list.append(CT_object)
                policy_list.append(CT_object2)

                return policy_list

    Args:
        num_of_days : Number of days to store the agent's contacts
        attribute : Parameter (attribute) type of agents
        value_list: List of attribute values of agents
    """
    def __init__(self,
                 num_of_days: int,
                 attribute: Union[str, None] = None,
                 value_list: List[str] = []):
        super().__init__('Contact_Tracing')
        self.num_of_days: int = num_of_days
        self.attribute: str = attribute
        self.value_list: List[str] = value_list

        CTPolicy.reduce_flag = True

    def reset(self, agents: ValuesView[Agent], locations: ValuesView[Location],
              model: BaseModel, policy_index: int) -> None:
        """
        Resets all the agents contact tracing policy state for a new world.

        Args:
            agents: Collection of :class:`~episimmer.agent.Agent` objects
            locations: Collection of :class:`~episimmer.location.Location` objects
            model: Disease model specified by the user
            policy_index: Policy index passed to differentiate policies.
        """
        for agent in agents:
            agent_ct_state = self.get_agent_policy_state(agent)
            if agent_ct_state is None:
                agent_ct_state = {}
                self.update_agent_policy_state(agent, agent_ct_state)
            agent_ct_state[policy_index] = {}
            agent_ct_state[policy_index]['schedule_time'] = 0
            if self.attribute is None or agent.info[
                    self.attribute] in self.value_list:
                agent_ct_state[policy_index]['contact_deque'] = deque(
                    maxlen=self.num_of_days)

    def post_policy(self, time_step: int, agents: Dict[str, Agent],
                    locations: ValuesView[Location], model: BaseModel,
                    policy_index: int) -> None:
        """
        Runs the post policy method to save contacts.

        Args:
            time_step: Current time step
            agents: Dictionary mapping from agent indices to :class:`~episimmer.agent.Agent` objects
            locations: Collection of :class:`~episimmer.location.Location` objects
            model: Disease model specified by the user
            policy_index: Policy index passed to differentiate policies
        """
        self.new_time_step(agents, policy_index)
        self.save_interactions(agents, policy_index)
        self.save_events(agents, locations, policy_index)

    def new_time_step(self, agents: Dict[str, Agent],
                      policy_index: int) -> None:
        """
        Initialises the contact list for agents for the new time step

        Args:
            agents: Dictionary mapping from agent indices to :class:`~episimmer.agent.Agent` objects
            policy_index: Policy index passed to differentiate policies
        """
        for agent in agents.values():
            if self.attribute is None or agent.info[
                    self.attribute] in self.value_list:
                agent_contact_list = ContactList()
                agent_ct_state = self.get_agent_policy_state(agent)
                agent_ct_state[policy_index]['contact_deque'].append(
                    agent_contact_list)
        CTPolicy.reduce_flag = True

    def save_interactions(self, agents: Dict[str, Agent],
                          policy_index: int) -> None:
        """
        Saving the contacts of the agent accounting individual and probabilistic interactions.

        Args:
            agents: Dictionary mapping from agent indices to :class:`~episimmer.agent.Agent` objects
            policy_index: Policy index passed to differentiate policies
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
                    agent_ct_state[policy_index]['contact_deque'][
                        -1].add_contact(agent_index)

    def save_events(self, agents: Dict[str,
                                       Agent], locations: ValuesView[Location],
                    policy_index: int) -> None:
        """
        Saving the contacts of the agent accounting regular and one time events.

        Args:
            agents: Dictionary mapping from agent indices to :class:`~episimmer.agent.Agent` objects
            locations: Collection of :class:`~episimmer.location.Location` objects
            policy_index: Policy index passed to differentiate policies
        """
        for location in locations:
            for event_dict in location.events:
                for agent_index in event_dict['_can_contrib']:
                    if self.attribute is None or agents[agent_index].info[
                            self.attribute] in self.value_list:
                        agent_ct_state = self.get_agent_policy_state(
                            agents[agent_index])
                        ct_deque = agent_ct_state[policy_index][
                            'contact_deque']
                        for contact in event_dict['_can_receive']:
                            ct_deque[-1].add_contact(contact)
                        if agent_index in event_dict['_can_receive']:
                            ct_deque[-1].remove_contact(agent_index)

    @staticmethod
    def reduce_agent_schedule_time(agent_ct_state: Dict[int, Dict[str, Union[
        int, Deque[ContactList]]]], policy_index: int) -> None:
        """
        If the agent's scheduled time is positive, this function decrements its scheduled time to lockdown by 1.

        Args:
            agent_ct_state: State of the contact tracing policy of the agent
            policy_index: Policy index passed to differentiate policies
        """
        agent_ct_scheduled_time = agent_ct_state[policy_index]['schedule_time']
        if agent_ct_scheduled_time > 0:
            agent_ct_state[policy_index]['schedule_time'] -= 1

    @staticmethod
    def reduce_agents_schedule_time(agents: Dict[str, Agent]) -> None:
        """
        Reduces the scheduled time for contacts by 1 across all contact tracing policies. This method must be run
        only once during a time step, even if multiple policies call this method.

        Args:
            agents: Collection of :class:`~episimmer.agent.Agent` objects
        """
        if CTPolicy.reduce_flag:
            for agent in agents.values():
                agent_ct_state = agent.get_policy_state('Contact_Tracing')
                if agent_ct_state is not None:
                    for policy_index in agent_ct_state.keys():
                        CTPolicy.reduce_agent_schedule_time(
                            agent_ct_state, policy_index)
            CTPolicy.reduce_flag = False

    @staticmethod
    def get_policy_index_list(agent: Agent) -> Union[List[int], None]:
        """
        Gets the list of policy indices corresponding to contact tracing policies

        Args:
            agent: Current agent

        Returns:
            List of policy indices (if they exist)
        """
        agent_ct_state = agent.get_policy_state('Contact_Tracing')
        if agent_ct_state is not None:
            return list(agent_ct_state.keys())

        return None

    @staticmethod
    def get_contact_list(agent: Agent, policy_index: int) -> List[str]:
        """
        Gets the contacts saved in an agent's contact tracing policy state for a particular policy index.

        Args:
            agent: Agent whose contacts are to be returned
            policy_index: Policy index of contact tracing policy

        Returns:
            All the contacts of the agent saved across all contact tracing policies
        """
        agent_ct_state = agent.get_policy_state('Contact_Tracing')
        contact_list = ContactList()
        if agent_ct_state is not None:
            if 'contact_deque' in agent_ct_state[policy_index].keys():
                contacts_deque = agent_ct_state[policy_index]['contact_deque']
                for contact_list_obj in contacts_deque:
                    contact_list = contact_list.union_contacts(
                        contact_list_obj)
        return contact_list.contacts

    @staticmethod
    def set_contacts_schedule_time(agents: Dict[str, Agent],
                                   contacts: List[str], policy_index: int,
                                   time_period: int) -> None:
        """
        Sets the time needed to lockdown for contacts of a positive agent to a fixed period. If the scheduled time of
        the contact is not 0 (contact currently in lockdown), then the time needed to lockdown is not reset.

        Args:
            agents: Collection of :class:`~episimmer.agent.Agent` objects
            contacts: List of contacts of a positively tested agent
            policy_index: Policy index of contact tracing policy
            time_period: Time period of lockdown
        """
        for contact_index in contacts:
            contact_agent = agents[contact_index]
            contact_ct_state = contact_agent.get_policy_state(
                'Contact_Tracing')
            if contact_ct_state[policy_index]['schedule_time'] == 0:
                contact_ct_state[policy_index]['schedule_time'] = time_period

    @staticmethod
    def get_max_schedule_time(agent: Agent) -> int:
        """
        Gets the maximum scheduled time left across contact tracing policies.

        Args:
            agent: Current agent

        Returns:
            Maximum schedule time left for lockdown for an agent
        """
        max_schedule_time = 0
        agent_ct_policy = agent.get_policy_state('Contact_Tracing')
        if agent_ct_policy is not None:
            for policy_index in agent_ct_policy.keys():
                agent_ct_scheduled_time = agent_ct_policy[policy_index][
                    'schedule_time']
                if agent_ct_scheduled_time is not None:
                    max_schedule_time = max(max_schedule_time,
                                            agent_ct_scheduled_time)

        return max_schedule_time
