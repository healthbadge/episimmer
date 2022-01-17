import random
from functools import partial
from typing import Callable, Dict, List, Tuple, Union

import numpy as np

from episimmer.agent import Agent
from episimmer.location import Location
from episimmer.read_file import ReadAgents

from .utils.time import Time

infectious_colors = ['red', 'pink', 'orange', 'purple']
normal_colors = ['blue', 'green', 'black', 'yellow', 'brown', 'white']


class StochasticModel():
    """
    Class for the Stochastic model.

    Args:
        individual_state_types: The states in the compartment model
        infected_states: The states that are infectious
        state_proportion: Starting proportions of each state
    """
    def __init__(self, individual_state_types: List[str],
                 infected_states: List[str], state_proportion: Dict[str,
                                                                    float]):
        self.recieve_fn: Union[Callable, None] = None
        self.contribute_fn: Union[Callable, None] = None
        self.transmission_prob: Dict[str, Dict[str, Callable]] = {}
        self.individual_state_types: List[str] = individual_state_types
        self.infected_states: List[str] = infected_states
        self.state_proportion: Dict[str, float] = state_proportion
        self.name: str = 'Stochastic Model'
        self.external_prev_fn: Callable = lambda x, y: 0.0
        self.colors: Dict[str, str] = {}
        self.color_index: List[int] = [0, 0]
        for state in individual_state_types:
            if state in infected_states:
                self.colors[state] = infectious_colors[self.color_index[0] %
                                                       len(infectious_colors)]
                self.color_index[0] += 1
            else:
                self.colors[state] = normal_colors[self.color_index[1] %
                                                   len(normal_colors)]
                self.color_index[1] += 1

        self.reset()

    def reset(self) -> None:
        """
        Initializes transitions probabilities between states to 0.
        """
        self.transmission_prob = {}
        for t in self.individual_state_types:
            self.transmission_prob[t] = {}

        for t1 in self.individual_state_types:
            for t2 in self.individual_state_types:
                self.transmission_prob[t1][t2] = self.p_standard(0)

    def initalize_states(self, agents: Dict[str, Agent]) -> None:
        """
        Initializes the states of the agents based on state proportions.

        Args:
            agents: A dictionary mapping from agent indices to agent objects
        """
        proportion_sum = 0
        for p in self.state_proportion.values():
            proportion_sum += p
        if proportion_sum != 1:
            raise ValueError(
                "Error! Starting state proportions don't add up to 1")

        prob_list = []
        cum_prob = 0
        for state in self.state_proportion.keys():
            cum_prob += self.state_proportion[state]
            prob_list.append(cum_prob)

        for agent in agents.values():
            r = random.random()
            for indx, value in enumerate(prob_list):
                if r < value:
                    state = list(self.state_proportion.keys())[indx]
                    agent.initialize_state(state)
                    break

    def find_next_state(self, agent: Agent,
                        agents: Dict[str, Agent]) -> Tuple[str, None]:
        """
        Returns next state of the agent according to the transition functions between the states stored in transmission_prob.

        Args:
            agent: The current agent whose next state is to be determined
            agents: A dictionary mapping from agent indices to agent objects

        Returns:
            The new state of the agent
        """
        scheduled_time = None
        r = random.random()
        p = 0
        for new_state in self.individual_state_types:
            p += self.transmission_prob[agent.state][new_state](agent, agents)
            if r < p:
                return new_state, scheduled_time
                break
        return agent.state, scheduled_time

    def full_p_standard(self, p: float, agent: Agent,
                        agents: Dict[str, Agent]) -> float:
        """
        Returns a fixed probability of transition.

        Args:
            p: Probability of transition
            agent: An agent object
            agents: A dictionary mapping from agent indices to agent objects

        Returns:
            Probability of transition
        """
        return p

    def p_standard(self, p: float) -> Callable:
        """
        This function can be used by the user in ``UserModel.py`` specifies an independent transition with a fixed probability.
        It returns a partial function of :meth:`~full_p_standard`.

        Args:
            p: Probability of transition

        Returns:
            Partial function
        """
        return partial(self.full_p_standard, p)

    def full_p_function(self, fn: Callable, agent: Agent,
                        agents: Dict[str, Agent]) -> float:
        """
        Returns the probability of transition that is specified by a user-defined function.

        Args:
            fn: User-defined function defining the probability of transition
            agent: An agent object
            agents: A dictionary mapping from agent indices to agent objects

        Returns:
            Probability of transition
        """
        return fn(Time.get_current_time_step())

    def p_function(self, fn: Callable) -> Callable:
        """
        This function can be used by the user in ``UserModel.py`` to specify an independent transition
        with a user-defined function defining the probability of transition.
        It returns a partial function of :meth:`~full_p_function`.

        Args:
            fn: User-defined function defining the probability of transition

        Returns:
            Partial function
        """
        return partial(self.full_p_function, fn)

    def full_p_infection(self, fn: Union[Callable, None],
                         p_infected_states_list: Union[List[float], None],
                         agent: Agent, agents: Dict[str, Agent]) -> float:
        """
        This function returns the probability of infection based on
        all types of interaction between the current agent and other agents.

        Args:
            fn: User-defined function defining the probability of infection based on individual/probabilistic interactions
            p_infected_states_list: List of probabilities that can be used in the user-defined function fn
            agent: Current agent object
            agents: A dictionary mapping from agent indices to agent objects

        Returns:
            Probability of getting an infection
        """
        p_not_inf = 1
        for c_dict in agent.contact_list:
            contact_index = c_dict['Interacting Agent Index']
            contact_agent = agents[contact_index]
            if random.random(
            ) < contact_agent.can_contribute_infection and random.random(
            ) < agent.can_recieve_infection:
                p_not_inf *= (1 - fn(p_infected_states_list, contact_agent,
                                     c_dict, Time.get_current_time_step()))

        for p in agent.event_probabilities:
            p_not_inf *= (1 - p)
        return (1 - p_not_inf) + self.external_prev_fn(
            agent, Time.get_current_time_step())

    def p_infection(self, p_infected_states_list: Union[List[float], None],
                    fn: Union[Callable, None]) -> Callable:
        """
        This function can be used by the user in ``UserModel.py`` to specify a dependent transition. The transition
        probability is based on all the types of interactions between the agents.
        Returns a partial function of :meth:`~full_p_infection`.

        Args:
            p_infected_states_list: List of probabilities that can be used in the user-defined function fn
            fn: User-defined function defining the probability based on individual/probabilistic interactions

        Returns:
            Partial function
        """
        return partial(self.full_p_infection, fn, p_infected_states_list)

    def set_transition(self, s1: str, s2: str, fn: Callable) -> None:
        """
        Adds a transition probability function between the specified states. The user must specify one of the following
        functions for the transition function

        * :meth:`~p_standard`

        * :meth:`~p_function`

        * :meth:`~p_infection`

        Args:
            s1: The first state
            s2: The second state
            fn: The function to be used for calculating the probability of transition

        """
        self.transmission_prob[s1][s2] = fn

    def set_event_contribution_fn(self, fn: Union[Callable, None]) -> None:
        """
        Sets the event contribute function specifying the contribution of an agent to the ambient infection of an event.

        Args:
            fn: User-defined function used to determine the contribution of an agent to the ambient infection of an event
        """
        self.contribute_fn = fn

    def set_event_recieve_fn(self, fn: Union[Callable, None]) -> None:
        """
        Sets the event receive function specifying the probability of infection for an agent from the ambient infection of an event.

        Args:
            fn: User-defined function for specifying the probability of infection for an agent from the ambient infection of an event
        """
        self.recieve_fn = fn

    def set_external_prevalence_fn(self, fn: Callable) -> None:
        """
        Sets the external prevalence function to specify probability of infection due to external prevalence.

        Args:
            fn: User-defined function for specifying probability of infection due to external prevalence
        """
        self.external_prev_fn = fn

    def update_event_infection(self, event_info: Dict[str, Union[str,
                                                                 List[str]]],
                               location: Location, agents_obj: ReadAgents,
                               event_restriction_fn: Callable) -> None:
        """
        Updates the agents with event probabilities of the events the agents attended.

        Args:
            event_info: Dictionary containing location and participating agents of an event
            location: Location object
            agents_obj: An object of class :class:`~episimmer.read_file.ReadAgents` containing all agents
            event_restriction_fn: User-defined function used to determine if an agent is restricted from participating in an event
        """
        ambient_infection = 0
        for agent_index in event_info['Agents']:
            agent = agents_obj.agents[agent_index]
            if event_restriction_fn(agent, event_info,
                                    Time.get_current_time_step()):
                continue
            if random.random() < agent.can_contribute_infection:
                ambient_infection += self.contribute_fn(
                    agent, event_info, location, Time.get_current_time_step())

        for agent_index in event_info['Agents']:
            agent = agents_obj.agents[agent_index]
            if event_restriction_fn(agent, event_info,
                                    Time.get_current_time_step()):
                continue
            if random.random() < agent.can_recieve_infection:
                p = self.recieve_fn(agent, ambient_infection, event_info,
                                    location, Time.get_current_time_step())
                agent.add_event_result(p)


class ScheduledModel():
    """
    Class for the Scheduled model.
    """
    def __init__(self):
        self.recieve_fn: Union[Callable, None] = None
        self.contribute_fn: Union[Callable, None] = None
        self.individual_state_types: List[str] = []
        self.state_transition_fn: Dict[str, Callable] = {}
        self.state_mean: Dict[str, Union[int, None]] = {}
        self.state_vary: Dict[str, Union[int, None]] = {}
        self.infected_states: List[str] = []
        self.state_proportion: Dict[str, float] = {}
        self.external_prev_fn: Callable = lambda x, y: 0.0
        self.name: str = 'Scheduled Model'
        self.state_fn: Dict[str, Union[Callable, None]] = {}

        self.colors: Dict[str, str] = {}
        self.color_index: List[int] = [0, 0]

    def insert_state(self, state: str, mean: Union[int, None],
                     vary: Union[int, None], transition_fn: Callable,
                     infected_state: bool, proportion: float) -> None:
        """
        Inserts a state into the model and schedules the agent for this state using a Normal
        distribution. The mean and variance are passed here as parameters to the Normal distribution. The user
        must specify one of the following functions for the transition function

        * :meth:`~scheduled`

        * :meth:`~p_infection`

        Args:
            state: The state to be inserted
            mean: The mean parameter of the Normal distribution
            vary: The variance parameter of the Normal distribution
            transition_fn: A function that encodes the states the agent can transition into from the current state
            infected_state: Defines whether the state is infectious
            proportion: Initial proportion of the state
        """
        if infected_state:
            self.infected_states.append(state)
        self.individual_state_types.append(state)
        self.state_transition_fn[state] = transition_fn
        self.state_mean[state] = mean
        self.state_vary[state] = vary
        self.state_proportion[state] = proportion
        self.state_fn[state] = None

        if infected_state:
            self.colors[state] = infectious_colors[self.color_index[0] %
                                                   len(infectious_colors)]
            self.color_index[0] += 1
        else:
            self.colors[state] = normal_colors[self.color_index[1] %
                                               len(normal_colors)]
            self.color_index[1] += 1

    def insert_state_custom(self, state: str, fn: Callable,
                            transition_fn: Callable, infected_state: bool,
                            proportion: float) -> None:
        """
        Inserts a state innto the model and schedules the agent for this state using a custom distribution
        specified by the user-defined function. The user must specify one of the following functions for the transition function

        * :meth:`~scheduled`

        * :meth:`~p_infection`

        Args:
            state: The state to be inserted
            fn: User-defined function that encodes the scheduled time step for transition
            transition_fn: A function that encodes the states an agent can transition into from the current state
            infected_state: Defines whether the state is infectious
            proportion: Initial proportion of the state
        """
        if infected_state:

            self.infected_states.append(state)
        self.individual_state_types.append(state)
        self.state_transition_fn[state] = transition_fn
        self.state_proportion[state] = proportion
        self.state_fn[state] = fn

        if infected_state:
            self.colors[state] = infectious_colors[self.color_index[0] %
                                                   len(infectious_colors)]
            self.color_index[0] += 1
        else:
            self.colors[state] = normal_colors[self.color_index[1] %
                                               len(normal_colors)]
            self.color_index[1] += 1

    def initalize_states(self, agents: Dict[str, Agent]) -> None:
        """
        Initializes the states of the agents based on state proportions.

        Args:
            agents: A dictionary mapping from agent indices to agent objects
        """
        proportion_sum = 0
        for p in self.state_proportion.values():
            proportion_sum += p
        if proportion_sum != 1:
            raise ValueError(
                "Error! Starting state proportions don't add up to 1")

        prob_list = []
        cum_prob = 0
        for state in self.state_proportion.keys():
            cum_prob += self.state_proportion[state]
            prob_list.append(cum_prob)

        for agent in agents.values():
            r = random.random()
            for indx, value in enumerate(prob_list):
                if r < value:
                    state = list(self.state_proportion.keys())[indx]
                    try:
                        schedule_time_left = random.randint(
                            0, int(self.state_mean[state]))
                    except:
                        schedule_time_left = None
                    agent.initialize_state(state, schedule_time_left)
                    break

    def find_scheduled_time(self, state: str) -> int:
        """
        Returns the scheduled time of transition for a state.

        Args:
            state: The state for which the scheduled time is returned

        Returns:
            The scheduled time of transition for the state
        """
        if (self.state_fn[state] == None):
            mean = self.state_mean[state]
            vary = self.state_vary[state]
            if mean == None or vary == None:
                scheduled_time = None
            else:
                scheduled_time = max(
                    0, int(np.random.normal(mean, np.sqrt(vary))))

        else:

            scheduled_time = self.state_fn[state](Time.get_current_time_step())
        return scheduled_time

    def find_next_state(self, agent: Agent,
                        agents: Dict[str, Agent]) -> Tuple[str, int]:
        """
        Returns next state of the agent according to the transition functions between the states.

        Args:
            agent: The agent whose next state is to be determined
            agents: A dictionary mapping from agent indices to agent objects

        Returns:
            The new state of the agent
        """
        if agent.schedule_time_left == None:
            return self.state_transition_fn[agent.state](agent, agents)

        return agent.state, agent.schedule_time_left

    def full_scheduled(self, new_states: Dict[str, float], agent: Agent,
                       agents: Dict[str, Agent]) -> Tuple[str, int]:
        """
        This function specifies that the state change is scheduled.
        Returns a new state from new_states and its scheduled time for an agent.

        Args:
            new_states: A dictionary mapping states to proportion an agent from the current state can transition to
            agent: An agent object
            agents: A dictionary mapping from agent indices to agent objects

        Returns:
            The new state of the agent and its scheduled time
        """
        new_state = self.choose_one_state(new_states)
        scheduled_time = self.find_scheduled_time(new_state)
        return new_state, scheduled_time

    def scheduled(self, new_states: Dict[str, float]) -> Callable:
        """
        This function can be used by the user in ``UserModel.py`` to specify an independent transition. The transition
        will occur based on a calculated scheduled time of stay for the state.
        Returns a partial function of :meth:`~full_scheduled`.

        Args:
            new_states: A dictionary mapping states to proportions an agent from the current state can transition to

        Returns:
            A partial function of :meth:`~full_scheduled`
        """
        return partial(self.full_scheduled, new_states)

    def p_infection(self, p_infected_states_list: List[Union[float, None]],
                    fn: Union[Callable,
                              None], new_states: Dict[str, float]) -> Callable:
        """
        This function can be used by the user in ``UserModel.py`` to specify that state change is driven by interaction with another state.
        Returns a partial function of :meth:`~full_p_infection`.

        Args:
            p_infected_states_list: List of probabilities that can be used in the user-defined function fn
            fn: User-defined function defining the probability of infection based on individual/probabilistic interactions
            new_states: A dictionary mapping states to proportion an agent from the current state can transition to

        Returns:
            A partial function of :meth:`~full_p_infection`
        """
        return partial(self.full_p_infection, fn, p_infected_states_list,
                       new_states)

    def full_p_infection(self, fn: Callable,
                         p_infected_states_list: List[Union[float, None]],
                         new_states: Dict[str, float], agent: Agent,
                         agents: Dict[str, Agent]) -> Tuple[str, int]:
        """
        This function returns returns a new state from new_states and its scheduled time based on
        all types of interaction between the current agent and other agents.

        Args:
            fn: User-defined function defining the probability of infection based on individual/probabilistic interactions
            p_infected_states_list: List of probabilities that can be used in the user-defined function fn
            new_states: A dictionary mapping states to proportion an agent from the current state can transition to
            agent: Current agent object
            agents: A dictionary mapping from agent indices to agent objects

        Returns:
            The new state of the agent and its scheduled time
        """

        new_state = self.choose_one_state(new_states)
        p_not_inf = 1
        for c_dict in agent.contact_list:
            contact_index = c_dict['Interacting Agent Index']
            contact_agent = agents[contact_index]
            if random.random(
            ) < contact_agent.can_contribute_infection and random.random(
            ) < agent.can_recieve_infection:
                p_not_inf *= (1 - fn(p_infected_states_list, contact_agent,
                                     c_dict, Time.get_current_time_step()))

        for p in agent.event_probabilities:
            p_not_inf *= (1 - p)

        r = random.random()
        if r >= (1 - p_not_inf) + self.external_prev_fn(
                agent, Time.get_current_time_step()):
            new_state = agent.state

        scheduled_time = self.find_scheduled_time(new_state)
        return new_state, scheduled_time

    def p_infection(self, p_infected_states_list: List[Union[float, None]],
                    fn: Union[Callable,
                              None], new_states: Dict[str, float]) -> Callable:
        """
        This function can be used by the user in ``UserModel.py`` to specify a dependent transition. The transition
        probability is based on all the types of interactions between the agents.
        Returns a partial function of :meth:`~full_p_infection`.

        Args:
            p_infected_states_list: List of probabilities that can be used in the user-defined function fn
            fn: User-defined function defining the probability of infection based on individual/probabilistic interactions
            new_states: A dictionary mapping states to proportion an agent from the current state can transition to

        Returns:
            A partial function of :meth:`~full_p_infection`
        """
        return partial(self.full_p_infection, fn, p_infected_states_list,
                       new_states)

    def choose_one_state(self, state_dict: Dict[str, float]) -> str:
        """
        Returns a new state from state_dict according to its proportion in the state_dict.

        Args:
            state_dict: A dictionary mapping states to proportion of current state that can transition into

        Returns:
            A new state
        """
        new_state = None
        p = 0
        r = random.random()
        for state in state_dict.keys():
            p += state_dict[state]
            if r < p:
                new_state = state
                break

        if new_state == None:
            raise ValueError('Error! State probabilities do not add to 1')
        return new_state

    def set_event_contribution_fn(self, fn: Union[Callable, None]) -> None:
        """
        Sets the event contribute function specifying the contribution of an agent to the ambient infection of an event.

        Args:
            fn: Function used to determine the contribution of an agent to an ambient infection
        """
        self.contribute_fn = fn

    def set_event_recieve_fn(self, fn: Union[Callable, None]) -> None:
        """
        Sets the event receive function specifying the probability of infection for an agent from the ambient infection of an event.

        Args:
            fn: Function used to determine the probability of an agent receiving an ambient infection
        """
        self.recieve_fn = fn

    def set_external_prevalence_fn(self, fn: Callable) -> None:
        """
        Sets the external prevalence function to specify probability of infection due to external prevalence.

        Args:
            fn: User-defined function for specifying probability of infection due to external prevalence
        """
        self.external_prev_fn = fn

    def update_event_infection(self, event_info: Dict[str, Union[str,
                                                                 List[str]]],
                               location: Location, agents_obj: ReadAgents,
                               event_restriction_fn: Callable) -> None:
        """
        Updates the agents with event probabilities of the events the agents attended.

        Args:
            event_info: Dictionary containing location and participating agents of an event
            location: Location object
            agents_obj: An object of class :class:`~episimmer.read_file.ReadAgents` containing all agents
            event_restriction_fn: User-defined function used to determine if an agent is restricted from participating in an event
        """
        ambient_infection = 0
        for agent_index in event_info['Agents']:
            agent = agents_obj.agents[agent_index]
            if event_restriction_fn(agent, event_info,
                                    Time.get_current_time_step()):
                continue
            if random.random() < agent.can_contribute_infection:
                ambient_infection += self.contribute_fn(
                    agent, event_info, location, Time.get_current_time_step())

        for agent_index in event_info['Agents']:
            agent = agents_obj.agents[agent_index]
            if event_restriction_fn(agent, event_info,
                                    Time.get_current_time_step()):
                continue
            if random.random() < agent.can_recieve_infection:
                p = self.recieve_fn(agent, ambient_infection, event_info,
                                    location, Time.get_current_time_step())
                agent.add_event_result(p)
