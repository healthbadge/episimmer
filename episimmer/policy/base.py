class AgentPolicy():
    def __init__(self):
        self.policy_type = None

    def enact_policy(self, time_step, agents, locations, model):
        pass

    def reset(self):
        pass

    def update_agent_policy_history(self, agent, history_value):
        agent.policy_dict[self.policy_type]['History'].append(history_value)

    def get_agent_policy_history(self, agent):
        return agent.policy_dict[self.policy_type]['History']

    def get_agent_policy_state(self, agent):
        return agent.policy_dict[self.policy_type]['State']

    def update_agent_policy_state(self, agent, new_state_value):
        agent.policy_dict[self.policy_type]['State'] = new_state_value
