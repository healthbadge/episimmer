import copy

from .base import AgentPolicy


class LockdownPolicy(AgentPolicy):
    def __init__(self, do_lockdown_fn, p):
        self.policy_type = 'Restrict'
        self.do_lockdown_fn = do_lockdown_fn
        self.p = p

    def lockdown_agent(self, agent):
        agent.update_recieve_infection(self.p)
        agent.update_contribute_infection(self.p)


class FullLockdown(LockdownPolicy):
    def __init__(self, do_lockdown_fn, p=0.0):
        super().__init__(do_lockdown_fn, p)

    def enact_policy(self,
                     time_step,
                     agents,
                     locations,
                     model=None,
                     policy_index=None):
        if self.do_lockdown_fn(time_step):
            agents = agents.values()
            for agent in agents:
                self.lockdown_agent(agent)


class AgentLockdown(LockdownPolicy):
    def __init__(self, parameter, value_list, do_lockdown_fn, p=0.0):
        super().__init__(do_lockdown_fn, p)
        self.parameter = parameter
        self.value_list = value_list

    def enact_policy(self,
                     time_step,
                     agents,
                     locations,
                     model=None,
                     policy_index=None):
        if self.do_lockdown_fn(time_step):
            agents = agents.values()
            for agent in agents:
                if agent.info[self.parameter] in self.value_list:
                    self.lockdown_agent(agent)


class TestingBasedLockdown(LockdownPolicy):
    def __init__(self,
                 do_lockdown_fn,
                 time_period,
                 contact_tracing=False,
                 p=0.0):
        super().__init__(do_lockdown_fn, p)
        self.time_period = time_period
        self.contact_tracing = contact_tracing

    def enact_policy(self,
                     time_step,
                     agents,
                     locations,
                     model=None,
                     policy_index=None):

        self.reduce_agent_schedule_time(agents)
        if self.do_lockdown_fn(time_step):
            self.lockdown_positive_agents(agents, time_step)
            if self.contact_tracing:
                self.lockdown_contacts(agents)

    def reduce_agent_schedule_time(self, agents):
        for agent in agents.values():
            agent_ct_state = agent.get_policy_state('Contact_Tracing')
            if agent_ct_state is not None:
                for ct_policy_index in agent_ct_state.keys():
                    self.reduce_schedule_time(agent, agent_ct_state,
                                              ct_policy_index)

    def reduce_schedule_time(self, agent, policy_state, policy_num):
        agent_ct_scheduled_time = policy_state[policy_num]['schedule_time']
        if agent_ct_scheduled_time > 0:
            policy_state[policy_num]['schedule_time'] -= 1

    def lockdown_positive_agents(self, agents, time_step):
        for agent in agents.values():
            result = self.get_agent_test_result(agent, time_step)
            if (result == 'Positive'):
                self.lockdown_agent(agent)
                if (self.contact_tracing):
                    contacts = self.obtain_contact_set(agent)
                    if contacts:
                        self.set_schedule_time(agents, contacts)

    def get_agent_test_result(self, agent, time_step):
        history = agent.get_policy_history('Testing')
        if (len(history)):
            last_time_step = history[-1].time_step
            if (time_step - last_time_step < self.time_period):
                result = self.get_accumulated_test_result(
                    history, last_time_step)
                return result
        return None

    def get_accumulated_test_result(self, history, last_time_step):
        indx = len(history) - 1
        while (indx >= 0 and history[indx].time_step == last_time_step):
            if (history[indx].result == 'Negative'):
                return 'Negative'
            indx -= 1
        return 'Positive'

    def obtain_contact_set(self, agent):
        agent_ct_state = agent.get_policy_state('Contact_Tracing')
        contacts = set()
        if agent_ct_state is not None:
            for ct_policy_index in agent_ct_state.keys():
                if 'contact_deque' in agent_ct_state[ct_policy_index].keys():
                    contacts_deque = agent_ct_state[ct_policy_index][
                        'contact_deque']
                    for contact in contacts_deque:
                        contacts = contacts.union(set(contact))
        return contacts

    def set_schedule_time(self, agents, contacts):
        for contact_index in contacts:
            contact_agent = agents[contact_index]
            contact_ct_state = contact_agent.get_policy_state(
                'Contact_Tracing')
            for contact_ct_policy_index in contact_ct_state.keys():
                if contact_ct_state[contact_ct_policy_index][
                        'schedule_time'] == 0:
                    contact_ct_state[contact_ct_policy_index][
                        'schedule_time'] = self.time_period

    def lockdown_contacts(self, agents):
        for agent in agents.values():
            max_state = 0
            agent_ct_policy = agent.get_policy_state('Contact_Tracing')
            if agent_ct_policy is not None:
                for policy_index in agent_ct_policy.keys():
                    agent_ct_scheduled_time = agent_ct_policy[policy_index][
                        'schedule_time']
                    if agent_ct_scheduled_time is not None:
                        max_state = max(max_state, agent_ct_scheduled_time)
                if max_state > 0:
                    self.lockdown_agent(agent)
