import random
import warnings
from functools import partial
from inspect import signature
from typing import Callable, Dict, List, Tuple, Union

import numpy as np

from episimmer.agent import Agent
from episimmer.location import Location
from episimmer.read_file import ReadAgents

from .utils.time import Time


class BaseModel():
    """
    Base class for disease models in Episimmer.

    Args:
        name: Name of Disease Model
    """
    def __init__(self, name: str):
        self.name: str = name

        self.individual_state_types: List[str] = []
        self.infected_states: List[str] = []
        self.state_proportion: Dict[str, float] = {}
        self.receive_fn: Union[Callable, None] = None
        self.contribute_fn: Union[Callable, None] = None
        self.external_prev_fn: Callable = lambda x, y: 0.0
        self.symptomatic_states: List[str] = []

        self.infectious_colors: List[str] = ['red', 'pink', 'orange', 'purple']
        self.normal_colors: List[str] = [
            'blue', 'green', 'black', 'yellow', 'brown', 'white'
        ]
        self.colors: Dict[str, str] = {}
        self.color_index: List[int] = [0, 0]

    def state_proportion_checker(self) -> None:
        """
        Checks whether the state proportions add up to 1.
        """
        proportion_sum = 0
        for p in self.state_proportion.values():
            proportion_sum += p
        if proportion_sum != 1:
            raise ValueError(
                "Error! Starting state proportions don't add up to 1")

    def initialize_states(self, agents: Dict[str, Agent]) -> None:
        """
        Initializes the states of the agents based on state proportions.

        Args:
            agents: A dictionary mapping from agent indices to agent objects
        """
        raise NotImplementedError

    def find_next_state(self, agent: Agent,
                        agents: Dict[str, Agent]) -> Tuple[str, int]:
        """
        Returns next state of the agent according to the transition functions between the states and the schedule time
        left.

        Args:
            agent: The agent whose next state is to be determined
            agents: A dictionary mapping from agent indices to agent objects

        Returns:
            The new state of the agent, Schedule time left for the agent in current state
        """
        raise NotImplementedError

    def set_state_color(self, state: str, infectious: bool) -> None:
        """
        Sets the state color based on whether the state is infectious or not.

        Args:
            state: State that needs color assignment
            infectious: Whether the state is infectious or not
        """
        if infectious:
            self.colors[state] = self.infectious_colors[
                self.color_index[0] % len(self.infectious_colors)]
            self.color_index[0] += 1
        else:
            self.colors[state] = self.normal_colors[self.color_index[1] %
                                                    len(self.normal_colors)]
            self.color_index[1] += 1

    def update_event_infection(self, event_info: Dict[str, Union[float, str,
                                                                 List[str]]],
                               location: Location,
                               agents_obj: ReadAgents) -> None:
        """
        Updates the agents with event probabilities of all the events the agents attended.

        Args:
            event_info: Dictionary containing location and participating agents of an event
            location: Location object
            agents_obj: An object of class :class:`~episimmer.read_file.ReadAgents` containing all agents
        """
        if self.contribute_fn is None:
            raise TypeError(
                'You have included events in your simulation but the disease model does not have the '
                'event contribute function set to a Callable function.')
        elif self.receive_fn is None:
            raise TypeError(
                'You have included events in your simulation but the disease model does not have the '
                'event receive function set to a Callable function.')
        ambient_infection = 0
        for agent_index in event_info['_can_contrib']:
            agent = agents_obj.agents[agent_index]
            ambient_infection += self.contribute_fn(
                agent, event_info, location, Time.get_current_time_step())

        for agent_index in event_info['_can_receive']:
            agent = agents_obj.agents[agent_index]
            p = self.receive_fn(agent, ambient_infection, event_info, location,
                                Time.get_current_time_step())
            agent.add_event_result(p)

    def set_event_contribution_fn(self, fn: Callable) -> None:
        """
        Sets the event contribute function specifying the contribution of an agent to the ambient infection of an event.
        It must be set to a Callable function with four parameters : agent, event_info, location and time_step. agent
        refers to the current agent responsible for contribution to ambient infection. event_info and location refer
        to the current event's parameters from the event and location files. time_step refers to the current time step.

        Args:
            fn: User-defined function used to determine the contribution of an agent to an ambient infection
        """
        if not callable(fn) or len(signature(fn).parameters) != 4:
            raise TypeError(
                'You must set the event contribution function to a Callable with the following four parameters : '
                'agent, event_info, location and time_step.')
        self.contribute_fn = fn

    def set_event_receive_fn(self, fn: Callable) -> None:
        """
        Sets the event receive function specifying the probability of infection for an agent from the ambient infection
        of an event. It must be set to a Callable function with four parameters : agent, ambient_infection, event_info,
        location and time_step. agent refers to the current agent receiving infection from participating in the event,
        ambient_infection is the total infection accumulated by all the agents in the event (calculated by
        event_contribution_fn). event_info and location refer to the current event's parameters from the event and
        location files. time_step refers to the current time step.

        Args:
            fn: User-defined function used to determine the probability of an agent receiving an ambient infection
        """
        if not callable(fn) or len(signature(fn).parameters) != 5:
            raise TypeError(
                'You must set the event receive function to a Callable with the following four parameters : '
                'agent, event_info, location and time_step.')
        self.receive_fn = fn

    def set_external_prevalence_fn(self, fn: Callable) -> None:
        """
        Sets the external prevalence function to specify probability of infection due to external prevalence. It must
        be set to a Callable function with two parameters : agent and time_step. agent refers to the current agent
        affected by external prevalence and time_step refers to the current time step.

        Args:
            fn: User-defined function for specifying probability of infection due to external prevalence
        """
        if not callable(fn) or len(signature(fn).parameters) != 2:
            raise TypeError(
                'You must set the external prevalence function to a Callable with the following two parameters : '
                'agent and time_step.')
        self.external_prev_fn = fn

    def states_checker(self, states: List[str]) -> bool:
        """
        Checks whether the states list passed belong to the states in the disease model created.

        Args:
            states: List of states to be checked

        Returns:
            Boolean representing whether valid states have been passed
        """
        for state in states:
            if state not in self.individual_state_types:
                return False

        return True

    def set_symptomatic_states(self, states: List[str]) -> None:
        """
        Sets the symptomatic states of the disease model. These agents in these states have visible symptoms of the
        disease.

        Args:
            states: List of disease model states that are symptomatic
        """
        if not isinstance(states, list):
            raise TypeError(
                'You must pass a list of valid disease states defined in the model.'
            )
        if not self.states_checker(states):
            raise ValueError(
                'You must pass a list of valid disease states defined in the model.'
            )
        self.symptomatic_states = states

    def get_final_infection_prob(self, fn: Union[Callable, None],
                                 p_infected_states_list: Union[List[float],
                                                               None],
                                 agent: Agent, agents: Dict[str,
                                                            Agent]) -> float:
        """
        Returns the final infection probability for an agent based on

        * Interactions (Individual and Probabilistic)

        * Events (Regular and One-Time)

        * External Prevalence

        Args:
            fn: User-defined function defining the probability of infection based on individual/probabilistic
                interactions
            p_infected_states_list: List of probabilities that can be used in the user-defined function fn
            agent: Current agent object
            agents: A dictionary mapping from agent indices to agent objects
        """
        p_not_inf = 1
        for c_dict in agent.contact_list:
            contact_index = c_dict['Interacting Agent Index']
            contact_agent = agents[contact_index]

            p_not_inf *= (1 - fn(p_infected_states_list, contact_agent, c_dict,
                                 Time.get_current_time_step()))

        for p in agent.event_probabilities:
            p_not_inf *= (1 - p)
        return (1 - p_not_inf) + self.external_prev_fn(
            agent, Time.get_current_time_step())


class StochasticModel(BaseModel):
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
        super().__init__('Stochastic Model')
        self.transmission_prob: Dict[str, Dict[str, Callable]] = {}
        self.infected_states: List[str] = infected_states
        self.individual_state_types: List[str] = individual_state_types
        self.state_proportion: Dict[str, float] = state_proportion

        for state in individual_state_types:
            if state in infected_states:
                self.set_state_color(state, True)
            else:
                self.set_state_color(state, False)

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
        if not callable(fn) or len(signature(fn).parameters) != 2:
            raise TypeError(
                'You may pass one of the three callable functions (templates) - p_standard, p_function or '
                'p_infection. You may also define your own function that takes the following two '
                'parameters - agent and agents and returns a probability of transition. agent refers to '
                'the current agent and agents refers to the dictionary mapping from agent '
                'indices to agent object.')
        self.transmission_prob[s1][s2] = fn

    def initialize_states(self, agents: Dict[str, Agent]) -> None:
        """
        Initializes the states of the agents based on state proportions.

        Args:
            agents: A dictionary mapping from agent indices to agent objects
        """

        self.state_proportion_checker()

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
        Returns next state of the agent according to the transition functions between the states stored in
        transmission_prob.

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
        This function can be used by the user in ``UserModel.py`` to specify an independent transition with a fixed
        probability. It returns a partial function of :meth:`~full_p_standard`.

        Args:
            p: Probability of transition

        Returns:
            Partial function
        """
        if not isinstance(p, int) and not isinstance(p, float):
            raise TypeError('You must pass an integer or float probability')

        elif p < 0.0 or p > 1.0:
            raise ValueError('You must pass a probability from 0.0 to 1.0')

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
        with a user-defined function defining the probability of transition. This user-defined function must have
        a single parameter defining the current time step of the simulation.
        It returns a partial function of :meth:`~full_p_function`.

        Args:
            fn: User-defined function defining the probability of transition

        Returns:
            Partial function
        """
        if not callable(fn) or len(signature(fn).parameters) != 1:
            raise TypeError(
                'You must pass a callable function with the time step parameter'
            )
        return partial(self.full_p_function, fn)

    def full_p_infection(self, fn: Union[Callable, None],
                         p_infected_states_list: Union[List[float], None],
                         agent: Agent, agents: Dict[str, Agent]) -> float:
        """
        This function returns the probability of infection based on
        all types of interaction between the current agent and other agents.

        Args:
            fn: User-defined function defining the probability of infection based on individual/probabilistic
                interactions
            p_infected_states_list: List of probabilities that can be used in the user-defined function fn
            agent: Current agent object
            agents: A dictionary mapping from agent indices to agent objects

        Returns:
            Probability of getting an infection
        """
        return self.get_final_infection_prob(fn, p_infected_states_list, agent,
                                             agents)

    def p_infection(
            self,
            fn: Union[Callable, None] = None,
            p_infected_states_list: Union[List[float],
                                          None] = None) -> Callable:
        """
        This function can be used by the user in ``UserModel.py`` to specify a dependent transition. The transition
        probability is based on all the types of interactions between the agents. For individual
        and probabilistic interactions, we must pass two parameters. The first parameter defines the user-defined
        function fn which returns the probability of infection for every agent considering these two types of
        interactions. The second parameter is an optional list of infected state probabilities to be used in
        the user-defined function fn. The parameters to be passed in the user-defined function are
        p_infected_states_list, contact_agent, c_dict and current_time_step. p_infected_states_list is the
        above-mentioned list of probabilities, contact_agent is the agent that the current agent is in contact
        with (through an individual or probabilistic interaction), c_dict is a dictionary defining the interaction
        and current_time_step is the current time step. If you do not have any of these types of interactions,
        you need not pass anything.
        Returns a partial function of :meth:`~full_p_infection`.

        Args:
            fn: User-defined function defining the probability based on individual/probabilistic interactions
            p_infected_states_list: List of probabilities that can be used in the user-defined function fn

        Returns:
            Partial function
        """
        if fn is not None:
            if not callable(fn) or len(signature(fn).parameters) != 4:
                raise TypeError(
                    'You must pass a callable function with the time step parameter'
                )

        if p_infected_states_list is not None:
            if not isinstance(p_infected_states_list, list):
                raise TypeError(
                    'You must pass a list of float values which can be used in your user-defined function. '
                    'This is an optional parameter')
            for val in p_infected_states_list:
                if not isinstance(val, float):
                    raise TypeError(
                        'You must pass a list of float values which can be used in your user-defined '
                        'function. This is an optional parameter')

        if fn is None and p_infected_states_list is not None:
            warnings.warn(
                'You have passed a list but there is no user-defined function passed to use it'
            )

        return partial(self.full_p_infection, fn, p_infected_states_list)


class ScheduledModel(BaseModel):
    """
    Class for the Scheduled model.
    """
    def __init__(self):
        super().__init__('Scheduled Model')
        self.individual_state_types: List[str] = []
        self.state_transition_fn: Dict[str, Callable] = {}
        self.state_mean: Dict[str, Union[int, None]] = {}
        self.state_vary: Dict[str, Union[int, None]] = {}
        self.state_proportion: Dict[str, float] = {}
        self.state_fn: Dict[str, Union[Callable, None]] = {}

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

        self.set_state_color(state, infected_state)

    def insert_state_custom(self, state: str, fn: Callable,
                            transition_fn: Callable, infected_state: bool,
                            proportion: float) -> None:
        """
        Inserts a state into the model and schedules the agent for this state using a custom distribution
        specified by the user-defined function. The user must specify one of the following functions for the transition
        function

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

        self.set_state_color(state, infected_state)

    def initialize_states(self, agents: Dict[str, Agent]) -> None:
        """
        Initializes the states of the agents based on state proportions.

        Args:
            agents: A dictionary mapping from agent indices to agent objects
        """
        self.state_proportion_checker()

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
        if self.state_fn[state] is None:
            mean = self.state_mean[state]
            vary = self.state_vary[state]
            if mean is None or vary is None:
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
        Returns next state of the agent according to the transition functions between the states and the schedule time
        left.

        Args:
            agent: The agent whose next state is to be determined
            agents: A dictionary mapping from agent indices to agent objects

        Returns:
            The new state of the agent, Schedule time left for the agent in current state
        """
        if agent.schedule_time_left is None:
            return self.state_transition_fn[agent.state](agent, agents)

        return agent.state, agent.schedule_time_left

    def choose_one_state(self, state_dict: Dict[str, float]) -> str:
        """
        Returns a new state from state_dict according to its proportion in the state_dict.

        Args:
            state_dict: A dictionary mapping states to proportions of current state that can transition into

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
        return new_state

    def full_scheduled(self, new_states: Dict[str, float], agent: Agent,
                       agents: Dict[str, Agent]) -> Tuple[str, int]:
        """
        This function specifies that the state change is scheduled.
        Returns a new state from new_states and its scheduled time for an agent.

        Args:
            new_states: A dictionary mapping states to proportions an agent from the current state can transition to
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

    def full_p_infection(self, new_states: Dict[str, float], fn: Callable,
                         p_infected_states_list: Union[List[float], None],
                         agent: Agent, agents: Dict[str,
                                                    Agent]) -> Tuple[str, int]:
        """
        This function returns a new state from new_states and its scheduled time based on
        all types of interaction between the current agent and other agents.

        Args:
            new_states: A dictionary mapping states to proportions an agent from the current state can transition to
            fn: User-defined function defining the probability of infection based on individual/probabilistic
                interactions
            p_infected_states_list: List of probabilities that can be used in the user-defined function fn
            agent: Current agent object
            agents: A dictionary mapping from agent indices to agent objects

        Returns:
            The new state of the agent and its scheduled time
        """

        new_state = self.choose_one_state(new_states)
        r = random.random()
        if r >= self.get_final_infection_prob(fn, p_infected_states_list,
                                              agent, agents):
            new_state = agent.state

        scheduled_time = self.find_scheduled_time(new_state)
        return new_state, scheduled_time

    def p_infection(
            self,
            new_states: Dict[str, float],
            fn: Union[Callable, None] = None,
            p_infected_states_list: Union[List[float],
                                          None] = None) -> Callable:
        """
        This function can be used by the user in ``UserModel.py`` to specify a dependent transition. The transition
        probability is based on all the types of interactions between the agents. It takes three parameters. The first
        is a dictionary mapping new states to transition proportions. The next two parameters are the same parameters
        as in the p_infection function of the Stochastic Model. The fn parameter defines the user-defined function for
        probability of infection from individual and probabilistic interactions and the p_infected_states_list
        parameter is a list of float probabilities that can be used in the user-defined function. The parameters to be
        passed in the user-defined function are p_infected_states_list, contact_agent, c_dict and current_time_step.
        p_infected_states_list is the above-mentioned list of probabilities, contact_agent is the agent that the
        current agent is in contact with (through an individual or probabilistic interaction), c_dict is a
        dictionary defining the interaction and current_time_step is the current time step. If you do not have any of
        these types of interactions, you need not pass the second and third parameters.
        Returns a partial function of :meth:`~full_p_infection`.

        Args:
            new_states: A dictionary mapping states to proportions an agent from the current state can transition to
            fn: User-defined function defining the probability of infection based on individual/probabilistic
                interactions
            p_infected_states_list: List of probabilities that can be used in the user-defined function fn

        Returns:
            A partial function of :meth:`~full_p_infection`
        """
        if not isinstance(new_states, dict):
            raise TypeError(
                'You must pass a dictionary mapping destination states to valid integer or float valued transition'
                ' proportions')
        for val in new_states.values():
            if not isinstance(val, float) and not isinstance(val, int):
                raise TypeError(
                    'You must pass a dictionary mapping destination states to valid integer or float valued '
                    'transition proportions')

        sum_proportion = 0
        for val in new_states.values():
            sum_proportion += val
        if sum_proportion != 1:
            raise ValueError('Transition proportions do not add up to 1')

        if fn is not None:
            if not callable(fn) or len(signature(fn).parameters) != 4:
                raise TypeError(
                    'You must pass a callable function with the time step parameter'
                )

        if p_infected_states_list is not None:
            if not isinstance(p_infected_states_list, list):
                raise TypeError(
                    'You must pass a list of float values which can be used in your user-defined function. '
                    'This is an optional parameter')
            for val in p_infected_states_list:
                if not isinstance(val, float):
                    raise TypeError(
                        'You must pass a list of float values which can be used in your user-defined '
                        'function. This is an optional parameter')

        if fn is None and p_infected_states_list is not None:
            warnings.warn(
                'You have passed a list but there is no user-defined function passed to use it'
            )

        return partial(self.full_p_infection, new_states, fn,
                       p_infected_states_list)
