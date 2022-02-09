from typing import Dict, Union, ValuesView

from episimmer.agent import Agent
from episimmer.location import Location
from episimmer.model import BaseModel


class Policy():
    """
    Class for implementing an Agent policy.

    Args:
        policy_type: Type of Agent Policy
    """
    def __init__(self, policy_type: str):
        self.policy_type: str = policy_type

    def reset(self, agents: ValuesView[Agent], locations: ValuesView[Location],
              model: BaseModel, policy_index: int) -> None:
        """
        Resets the policy for a new world.

        Args:
            agents: Collection of :class:`~episimmer.agent.Agent` objects
            locations: Collection of :class:`~episimmer.location.Location` objects
            model: Disease model specified by the user
            policy_index: Policy index passed to differentiate policies
        """
        pass

    def enact_policy(self, time_step: int, agents: Dict[str, Agent],
                     locations: ValuesView[Location], model: BaseModel,
                     policy_index: int) -> None:
        """
        Executes a policy for the given time step.

        Args:
            time_step: Current time step
            agents: Dictionary mapping from agent indices to :class:`~episimmer.agent.Agent` objects
            locations: Collection of :class:`~episimmer.location.Location` objects
            model: Disease model specified by the user
            policy_index: Policy index passed to differentiate policies
        """
        pass

    def post_policy(self, time_step: int, agents: Dict[str, Agent],
                    locations: ValuesView[Location], model: BaseModel,
                    policy_index: int) -> None:
        """
        Post policy procedure used for policies that require the interactions and events that
        are going to take place in the current time step.

        Args:
            time_step: Current time step
            agents: Dictionary mapping from agent indices to :class:`~episimmer.agent.Agent` objects
            locations: Collection of :class:`~episimmer.location.Location` objects
            model: Disease model specified by the user
            policy_index: Policy index passed to differentiate policies.
        """
        pass


class AgentPolicy(Policy):
    """
    Class for implementing an Agent policy.

    Args:
        policy_type: Type of Agent Policy
    """
    def __init__(self, policy_type: str):
        super().__init__(policy_type)

    def update_agent_policy_history(self, agent: Agent,
                                    history_value: object) -> None:
        """
        Updates the agent policy history list for the current policy type.

        Args:
            agent: Instance of :class:`~episimmer.agent.Agent`
            history_value: Value to be appended to the history list
        """
        agent.policy_dict[self.policy_type]['History'].append(history_value)

    def get_agent_policy_history(self, agent: Agent) -> object:
        """
        Returns the agent policy history list for the current policy type.

        Args:
            agent: Instance of :class:`~episimmer.agent.Agent`

        Returns:
            The agent policy history list for the current policy type
        """
        return agent.policy_dict[self.policy_type]['History']

    def update_agent_policy_state(self, agent: Agent,
                                  new_state_value: object) -> None:
        """
        Updates the agent policy state for the current policy type.

        Args:
            agent: Instance of :class:`~episimmer.agent.Agent`
            new_state_value: Value to be set as the policy state
        """
        agent.policy_dict[self.policy_type]['State'] = new_state_value

    def get_agent_policy_state(self, agent: Agent) -> object:
        """
        Returns the agent policy state for the current policy type.

        Args:
            agent: Instance of :class:`~episimmer.agent.Agent`

        Returns:
            The agent policy state for the current policy type
        """
        return agent.policy_dict[self.policy_type]['State']


class EventPolicy(Policy):
    """
    Class for implementing an Event policy.

    Args:
        policy_type: Type of Event Policy
    """
    def __init__(self, policy_type: str):
        super().__init__(policy_type)
