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
    Class for the stochastic model.

    :param individual_state_types: The states in the compartment model
    :param infected_states: The states that are infectious
    :param state_proportion: Starting proportions of each state
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
        Initializes transitions probabilities between states.
        """
        self.transmission_prob = {}
        for t in self.individual_state_types:
            self.transmission_prob[t] = {}

        for t1 in self.individual_state_types:
            for t2 in self.individual_state_types:
                self.transmission_prob[t1][t2] = self.p_standard(0)

    def initalize_states(self, agents: Dict[int, Agent]) -> None:
        """
        Initializes the states of the agents.

        :param agents: A dictionary mapping agent indexes to agent objects
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
                        agents: Dict[int, Agent]) -> Tuple[str, None]:
        """
        Returns new state of the agent according to the probabilities between the states.

        :param agent: The agent whose state is to be changed
        :param agents: A dictionary mapping agent indexes to agent objects
        :return: The new state of the agent
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
                        agents: Dict[int, Agent]) -> float:
        """
        Returns the probability of transition.

        :param p: Probability
        :param agent: An agent object
        :param agents: A dictionary mapping agent indexes to agent objects
        :return: Probability
        """
        return p

    def p_standard(self, p: float) -> Callable:
        """
        Returns the probability of transition.
        This function can be used by the user in ``UserModel.py`` to define a fixed probability.
        It returns a partial function of :meth:`~full_p_standard`.

        :param p: Probability
        :return: Partial function
        """
        return partial(self.full_p_standard, p)

    def full_p_function(self, fn: Callable, agent: Agent,
                        agents: Dict[int, Agent]) -> float:
        """
        Returns the probability of transition that is specified by the user defined function.

        :param fn: Function defining the probability
        :param agent: An agent object
        :param agents: A dictionary mapping agent indexes to agent objects
        :return: Probability
        """
        return fn(Time.get_current_time_step())

    def p_function(self, fn: Callable) -> Callable:
        """
        Returns the probability of transition that is specified by the user defined function.
        This function can be used by the user in ``UserModel.py`` to specify the probability
        from the user defined function.
        It returns a partial function of :meth:`~full_p_function`.

        :param fn: Function defining the probability
        :return: Partial function
        """
        return partial(self.full_p_function, fn)

    def full_p_infection(self, fn: Union[Callable, None],
                         p_infected_states_list: List[Union[float, None]],
                         agent: Agent, agents: Dict[int, Agent]) -> float:
        """
        Returns the probability of infection based on the interaction between agents.

        :param fn: Function defining the probability based on interaction
        :param p_infected_states_list:
        :param agent: An agent object
        :param agents: A dictionary mapping agent indexes to agent objects
        :return: Probability of getting an infection
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
        Returns the probability of infection based on the interaction between agents.
        This function can be used by the user in ``UserModel.py`` to specify a user defined function
        for the probability of infection.
        Returns a partial function of :meth:`~full_p_infection`.

        :param p_infected_states_list: List of probabilities of transition to infected states
        :param fn: Function defining the probability based on interaction
        :return: Partial function
        """
        return partial(self.full_p_infection, fn, p_infected_states_list)

    def set_transition(self, s1: str, s2: str, fn: Callable) -> None:
        """
        Adds a transition probability function between the specified states.

        :param s1: The first state
        :param s2: The second state
        :param fn: The function to be used for the transition probability
        """
        self.transmission_prob[s1][s2] = fn

    def set_event_contribution_fn(self, fn: Union[Callable, None]) -> None:
        """
        Sets the probability of contribution by an agent to an ambient infection.

        :param fn: Function used to determine the probability of contribution by an agent to an ambient infection
        """
        self.contribute_fn = fn

    def set_event_recieve_fn(self, fn: Union[Callable, None]) -> None:
        """
        Sets the probability of an agent receiving ambient infection.

        :param fn: Function used to determine the probability of an agent receiving ambient infection
        """
        self.recieve_fn = fn

    def set_external_prevalence_fn(self, fn: Callable) -> None:
        """
        Sets the probability of an agent receiving an infection due to external prevalence.

        :param fn: User defined function for specifying probability of receiving an infection due to external prevalence
        """
        self.external_prev_fn = fn

    def update_event_infection(self, event_info: Dict[str, Union[str,
                                                                 List[str]]],
                               location: Location, agents_obj: ReadAgents,
                               event_restriction_fn: Callable) -> None:
        """
        Updates event info to agents from location.

        :param event_info: Dictionary containing location and participating agents of an event
        :param location: Location object
        :param agents_obj: An object of class :class:`~episimmer.read_file.ReadAgents` containing all agents
        :param event_restriction_fn: Function used to determine if an agent is restricted from participating in an event
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
    def __init__(self):
        self.individual_state_types = []
        self.state_transition_fn = {}  #One of Scheduled or Dependant
        self.state_mean = {}
        self.state_vary = {}
        self.infected_states = []
        self.state_proportion = {}
        self.external_prev_fn = lambda x, y: 0.0
        self.name = 'Scheduled Model'
        self.state_fn = {}

        self.colors = {}
        self.color_index = [0, 0]

    def insert_state(self, state, mean, vary, transition_fn, infected_state,
                     proportion):
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

    def insert_state_custom(self, state, fn, transition_fn, infected_state,
                            proportion):
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

    def initalize_states(self, agents):
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

    def find_scheduled_time(self, state):

        if (self.state_fn[state] == None):
            mean = self.state_mean[state]
            vary = self.state_vary[state]
            if mean == None or vary == None:
                scheduled_time = None
            else:
                scheduled_time = max(0, int(np.random.normal(mean, vary)))

        else:

            scheduled_time = self.state_fn[state](Time.get_current_time_step())
        return scheduled_time

    def find_next_state(self, agent, agents):
        if agent.schedule_time_left == None:
            return self.state_transition_fn[agent.state](agent, agents)

        return agent.state, agent.schedule_time_left

    def full_scheduled(self, new_states, agent, agents):
        new_state = self.choose_one_state(new_states)
        scheduled_time = self.find_scheduled_time(new_state)
        return new_state, scheduled_time

    def scheduled(self, new_states):
        return partial(self.full_scheduled, new_states)

    def full_p_function(self, new_states, agent, agents):

        new_state = self.choose_one_state(new_states)
        scheduled_time = self.find_scheduled_time(new_state)

        return new_state, scheduled_time

    def p_function(self, new_states):
        return partial(self.full_p_function, new_states)

    def p_infection(self, p_infected_states_list, fn, new_states):
        return partial(self.full_p_infection, fn, p_infected_states_list,
                       new_states)

    def full_p_infection(self, fn, p_infected_states_list, new_states, agent,
                         agents):
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

    def choose_one_state(self, state_dict):
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

    def set_event_contribution_fn(self, fn):
        self.contribute_fn = fn

    def set_event_recieve_fn(self, fn):
        self.recieve_fn = fn

    def set_external_prevalence_fn(self, fn):
        self.external_prev_fn = fn

    def update_event_infection(self, event_info, location, agents_obj,
                               event_restriction_fn):
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
