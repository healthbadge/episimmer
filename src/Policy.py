class Agent_Policy():
	def __init__(self):
		self.policy_type=None

	def enact_policy(self,time_step,agents,locations,model):
		pass

	def reset(self):
		pass

	def update_agent_policy_history(self,agent,history_value):
		agent.policy_dict[self.policy_type]['History'].append(history_value)

	def get_agent_policy_history(self,agent):
		return agent.policy_dict[self.policy_type]['History']

	def get_agent_policy_state(self,agent):
		return agent.policy_dict[self.policy_type]['State']

	def update_agent_policy_state(self,agent,new_state_value):
		agent.policy_dict[self.policy_type]['State']=new_state_value

def default_event_restriction_fn(agent,event_info,current_time_step):
		return False

class PolicyTemplate():
	def __init__(self):
		self.policy_list=[]
		self.event_restriction_fn=default_event_restriction_fn

	def add_policy(self,policy):
		self.policy_list.append(policy)
