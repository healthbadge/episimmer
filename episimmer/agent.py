from typing import Callable, Dict, List, Tuple, Union, ValuesView
from xmlrpc.client import Boolean


class Agent():
    """
    Class for storing details of each agent.

    Args:
        state: The state of the agent.
        info_dict: Information of each agent taken from agents.txt.
    """
    def __init__(self, state: str, info_dict: Dict[str, str]):
        self.state: str = state
        self.next_state: Union[str, None] = None
        self.contact_list: List[str] = []
        self.location_list: List[str] = []
        self.info: Dict[str, str] = info_dict
        self.index: str = info_dict['Agent Index']
        self.event_probabilities: List[int] = []

        self.schedule_time_left: Union[int, None] = None
        self.can_recieve_infection: int = 1.0
        self.can_contribute_infection: int = 1.0
        self.under_protection: Boolean = False

        self.policy_dict: Dict = {}  #Store all policy related status of agent
        self.initialize_policy_dict()

    def initialize_state(self,
                         state: str,
                         schedule_time_left=Union[int, None]) -> None:
        """
        Stores the state of the agent in the disease model. Also stores schedule time of agent if model is scheduled.

        Args:
            state : Current state of the agent in Disease Model
            scheduled_time_left: Number of remaining time steps for agent to exist in that state uf agent is part of scheduled disease model.
        """
        self.state: str = state
        self.schedule_time_left: Union[int, None] = schedule_time_left

    def initialize_policy_dict(self) -> None:
        """
        Creates Policy Dict with keys as all the possible policies an agent can undergo.
        """
        for policy_type in [
                'Restrict', 'Testing', 'Vaccination', 'Contact_Tracing'
        ]:
            temp = {'History': [], 'State': None}
            self.policy_dict[policy_type] = temp

    def get_policy_state(
            self, policy_type: str) -> Union[None, List, Dict, str, int]:
        """
        Used to fetch the current state of agent under specified policy.

        Args:
            policy_type:Policy whose state is required.

        Returns:
            State of agent under that policy.
        """
        return self.policy_dict[policy_type]['State']

    def get_policy_history(self, policy_type: str) -> List:
        """
        Used to fetch the current state of agent under specified policy.

       Args:
            policy_type:Policy whose state is required.

        Returns:
            History of agent under that policy.
        """
        return self.policy_dict[policy_type]['History']

    def add_contact(self, contact_dict: Dict) -> None:
        """
        Adds the contacts of that time step to agents contact_list.

        Args:
            contact_dict:Dictionary containing contacts of each agent for that timestep.
        """
        self.contact_list.append(contact_dict)

    def add_event_result(self, p: int) -> None:
        """
        Adds the event probabilities that agent has been part of to the event probabilities list.

        Args:
            p:Probability of event.
        """
        self.event_probabilities.append(p)

    def new_time_step(self) -> None:
        """
        Resets all attributes of agent at the beginning of a new world on the first timestep of the simulation.
        """
        self.can_recieve_infection = 1.0
        self.can_contribute_infection = 1.0
        self.next_state = None
        self.contact_list = []
        self.event_probabilities = []
        if self.schedule_time_left != None:
            self.schedule_time_left -= 1
            if self.schedule_time_left <= 0:
                self.schedule_time_left = None

    def update_state(self) -> None:
        """
        Stores the next state of the agent if it exists.
        """
        if self.next_state == None:
            return
        self.state = self.next_state
        self.next_state = None

    def set_next_state(self, state_info: Tuple) -> None:
        """
        Updates the next state and scheduled time of agent in scheduled model.

        Args:
            state_info: Tuple storing next state and scheduled time of agent in the scheduled model.
        """
        next_state, schedule_time = state_info
        self.next_state = next_state
        self.schedule_time_left = schedule_time

    def update_recieve_infection(self, p: int) -> None:
        """
        Updates agents probability to receive any kind of infection.

        Args:
            p: New probability of agents chances to recieve infection.
        """
        self.can_recieve_infection: int = p

    def update_contribute_infection(self, p) -> None:
        """
        Updates agents probability to contribute to any kind of infection.

        Args:
            p: New probability of agents chances to contribute to existing infection.
        """
        self.can_contribute_infection: int = p

    def protect(self) -> None:
        """
        Sets a flag to true.This flag has significance in varous policies.
        """
        self.under_protection = True
