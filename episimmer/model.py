import random
from functools import partial

import numpy as np

from .utils.time import Time

infectious_colors = ['red', 'pink', 'orange', 'purple']
normal_colors = ['blue', 'green', 'black', 'yellow', 'brown', 'white']


class StochasticModel():
    def __init__(self, individual_state_types, infected_states,
                 state_proportion):
        self.individual_state_types = individual_state_types
        self.infected_states = infected_states
        self.state_proportion = state_proportion
        self.name = 'Stochastic Model'
        self.external_prev_fn = lambda x, y: 0.0

        self.colors = {}
        self.color_index = [0, 0]
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

    def reset(self):
        self.transmission_prob = {}
        for t in self.individual_state_types:
            self.transmission_prob[t] = {}

        for t1 in self.individual_state_types:
            for t2 in self.individual_state_types:
                self.transmission_prob[t1][t2] = self.p_standard(0)

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
                    agent.initialize_state(state)
                    break

    def find_next_state(self, agent, agents):
        scheduled_time = None
        r = random.random()
        p = 0
        for new_state in self.individual_state_types:
            p += self.transmission_prob[agent.state][new_state](agent, agents)
            if r < p:
                return new_state, scheduled_time
                break
        return agent.state, scheduled_time

    def full_p_standard(self, p, agent, agents):
        return p

    def p_standard(self, p):
        return partial(self.full_p_standard, p)

    def full_p_function(self, fn, agent, agents):
        return fn(Time.get_current_time_step())

    def p_function(self, fn):
        return partial(self.full_p_function, fn)

    def full_p_infection(self, fn, p_infected_states_list, agent, agents):
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

    def p_infection(self, p_infected_states_list, fn):
        return partial(self.full_p_infection, fn, p_infected_states_list)

    def set_transition(self, s1, s2, fn):
        self.transmission_prob[s1][s2] = fn

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
