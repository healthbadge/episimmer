from typing import Dict, List, Tuple, Union


class Agent():
    """
    Class for an agent of the simulation.

    Args:
        state: The state of the agent.
        info_dict: Information of each agent taken from the agents file.
    """
    def __init__(self, state: Union[str, None], info_dict: Dict[str, str]):
        self.state: Union[str, None] = state
        self.next_state: Union[str, None] = None
        self.contact_list: List[Dict[str, str]] = []
        self.info: Dict[str, str] = info_dict
        self.index: str = info_dict['Agent Index']
        self.event_probabilities: List[float] = []

        self.schedule_time_left: Union[int, None] = None
        self.can_receive_infection: float = 1.0
        self.can_contribute_infection: float = 1.0
        self.under_protection: bool = False

        self.policy_dict: Dict[str, Dict[str, Union[List[object],
                                                    object]]] = {}
        self.initialize_policy_dict()

    def __repr__(self) -> str:
        """
        Shows the representation of the object as the string index

        Returns:
            The index of agent
        """
        return str(self.index)

    def initialize_state(self,
                         state: str,
                         schedule_time_left: Union[int, None] = None) -> None:
        """
        Stores the state of the agent in the disease model. Also stores schedule time of agent if model is scheduled.

        Args:
            state : Current state of the agent in Disease Model
            schedule_time_left: Number of remaining time steps for an agent to exist in the state.
        """
        self.state = state
        self.schedule_time_left = schedule_time_left

    def initialize_policy_dict(self) -> None:
        """
        Creates a policy dictionary with keys of all the possible policies an agent can experience.
        """
        for policy_type in [
                'Restrict', 'Testing', 'Vaccination', 'Contact_Tracing'
        ]:
            temp = {'History': [], 'State': None}
            self.policy_dict[policy_type] = temp

    def get_policy_state(self, policy_type: str) -> object:
        """
        Used to fetch the current state of agent under specified policy.

        Args:
            policy_type: Policy whose state is required.

        Returns:
            State of agent under that policy.
        """
        return self.policy_dict[policy_type]['State']

    def get_policy_history(self, policy_type: str) -> List[object]:
        """
        Used to fetch the current history of agent under specified policy.

        Args:
            policy_type: Policy whose history is required.

        Returns:
            History of agent under that policy.
        """
        return self.policy_dict[policy_type]['History']

    def add_contact(self, contact_dict: Dict[str, str]) -> None:
        """
        Adds a contact (interaction) to the agents contact_list.

        Args:
            contact_dict: Dictionary containing information for a single interaction.
        """
        self.contact_list.append(contact_dict)

    def add_event_result(self, p: float) -> None:
        """
        Adds an event probability that agent has been part of to the event probabilities list.

        Args:
            p: Probability of infection for attending an event
        """
        self.event_probabilities.append(p)

    def new_time_step(self) -> None:
        """
        Resets all attributes of agent at the beginning of a time step of the simulation.
        """
        self.can_receive_infection = 1.0
        self.can_contribute_infection = 1.0
        self.next_state = None
        self.contact_list = []
        self.event_probabilities = []
        if self.schedule_time_left is not None:
            self.schedule_time_left -= 1
            if self.schedule_time_left <= 0:
                self.schedule_time_left = None

    def update_state(self) -> None:
        """
        Stores the next state of the agent if it exists.
        """
        if self.next_state is None:
            return
        self.state = self.next_state
        self.next_state = None

    def set_next_state(self, state_info: Tuple[str, int]) -> None:
        """
        Updates the next state and scheduled time left

        Args:
            state_info: Tuple storing next state and scheduled time left
        """
        next_state, schedule_time = state_info
        self.next_state = next_state
        self.schedule_time_left = schedule_time

    def update_receive_infection(self, p: float) -> None:
        """
        Updates agent's probability to receive infection.

        Args:
            p: Probability of receiving infection
        """
        self.can_receive_infection = p

    def update_contribute_infection(self, p: float) -> None:
        """
        Updates agent's probability to contribute infection.

        Args:
            p: Probability of contributing to infection
        """
        self.can_contribute_infection = p

    def protect(self) -> None:
        """
        Sets the under_protection flag to True. This flag indicates that the Agent is under the protection of a vaccine.
        """
        self.under_protection = True
