from .base import AgentPolicy


class FullLockdown(AgentPolicy):
    def __init__(self, do_lockdown_fn, p=0.0):
        self.policy_type = 'Restrict'
        self.do_lockdown_fn = do_lockdown_fn
        self.p = p

    def enact_policy(self, time_step, agents, locations, model=None):
        if self.do_lockdown_fn(time_step):
            for agent in agents:
                agent.update_recieve_infection(self.p)
                agent.update_contribute_infection(self.p)


class AgentLockdown(AgentPolicy):
    def __init__(self, parameter, value_list, do_lockdown_fn, p=0.0):
        self.policy_type = 'Restrict'
        self.do_lockdown_fn = do_lockdown_fn
        self.parameter = parameter
        self.value_list = value_list
        self.p = p

    def enact_policy(self, time_step, agents, locations, model=None):
        if self.do_lockdown_fn(time_step):
            for agent in agents:
                if agent.info[self.parameter] in self.value_list:
                    agent.update_recieve_infection(self.p)
                    agent.update_contribute_infection(self.p)


class AgentPolicyBasedLockdown(AgentPolicy):
    def __init__(self,
                 policy_to_consider,
                 value_list,
                 do_lockdown_fn,
                 time_period,
                 p=0.0):
        self.policy_type = 'Restrict'
        self.policy_to_consider = policy_to_consider
        self.do_lockdown_fn = do_lockdown_fn
        self.value_list = value_list
        self.time_period = time_period
        self.p = p

    def enact_policy(self, time_step, agents, locations, model=None):
        if self.do_lockdown_fn(time_step):
            for agent in agents:
                history = agent.get_policy_history(self.policy_to_consider)
                if (len(history)):
                    last_time_step = history[-1].time_step
                    if (time_step - last_time_step < self.time_period):
                        result = self.get_accumulated_result(
                            history, last_time_step)
                        if (result in self.value_list):
                            agent.update_recieve_infection(self.p)
                            agent.update_contribute_infection(self.p)

    def get_accumulated_result(self, history, last_time_step):

        indx = len(history) - 1
        while (indx >= 0 and history[indx].time_step == last_time_step):
            if (history[indx].result == 'Negative'):
                return 'Negative'

            indx -= 1

        return 'Positive'
