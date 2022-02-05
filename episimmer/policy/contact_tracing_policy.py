from collections import deque

from .base import AgentPolicy


class CTPolicy(AgentPolicy):
    def __init__(self, num_of_days, attribute=None, value_list=[]):
        super().__init__()
        self.policy_type = 'Contact_Tracing'
        self.num_of_days = num_of_days
        self.attribute = attribute
        self.value_list = value_list

    def reset(self, agents, policy_index):
        for agent in agents:
            agent_ct_state = self.get_agent_policy_state(agent)
            if agent_ct_state is None:
                self.update_agent_policy_state(agent, {})
                agent_ct_state = self.get_agent_policy_state(agent)
            agent_ct_state[policy_index] = {}
            agent_ct_state[policy_index]['schedule_time'] = 0
            if self.attribute is None or agent.info[
                    self.attribute] in self.value_list:
                agent_ct_state[policy_index]['contact_deque'] = deque(
                    maxlen=self.num_of_days)

    def post_policy(self, time_step, agents, locations, model, policy_index):
        self.new_time_step(agents, policy_index)
        self.save_interactions(agents, policy_index)
        self.save_events(agents, locations, policy_index)

    def new_time_step(self, agents, policy_index):
        for agent in agents.values():
            if self.attribute is None or agent.info[
                    self.attribute] in self.value_list:
                agent_contact_set = set()
                agent_ct_state = self.get_agent_policy_state(agent)
                agent_ct_state[policy_index]['contact_deque'].append(
                    agent_contact_set)

    def save_interactions(self, agents, policy_index):
        for agent_index in agents.keys():
            for contact_dict in agents[agent_index].contact_list:
                interacting_agent_index = contact_dict[
                    'Interacting Agent Index']
                if self.attribute is None or agents[
                        interacting_agent_index].info[
                            self.attribute] in self.value_list:
                    agent_ct_state = self.get_agent_policy_state(
                        agents[interacting_agent_index])
                    agent_ct_state[policy_index]['contact_deque'][-1].add(
                        agent_index)

    def save_events(self, agents, locations, policy_index):
        for location in locations:
            for event_dict in location.events:
                for agent_index in event_dict['can_contrib']:
                    if self.attribute is None or agents[agent_index].info[
                            self.attribute] in self.value_list:
                        agent_ct_state = self.get_agent_policy_state(
                            agents[agent_index])
                        ct_deque = agent_ct_state[policy_index][
                            'contact_deque']
                        ct_deque[-1] = ct_deque[-1].union(
                            set(event_dict['can_receive']))
                        if agent_index in event_dict['can_receive']:
                            ct_deque[-1].remove(agent_index)
