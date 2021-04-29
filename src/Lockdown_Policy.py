from Policy import Agent_Policy
import random

class full_lockdown(Agent_Policy):
	def __init__(self,do_lockdown_fn):
		self.policy_type='Restrict'
		self.do_lockdown_fn=do_lockdown_fn

	def enact_policy(self,time_step,agents,locations,model=None):
		if self.do_lockdown_fn(time_step):
			for agent in agents:
				agent.restrict_recieve_infection()
				agent.restrict_contribute_infection()

class agent_lockdown(Agent_Policy):
	def __init__(self,parameter,value_list,do_lockdown_fn):
		self.policy_type='Restrict'
		self.do_lockdown_fn=do_lockdown_fn
		self.parameter=parameter
		self.value_list=value_list

	def enact_policy(self,time_step,agents,locations,model=None):
		if self.do_lockdown_fn(time_step):
			for agent in agents:
				if agent.info[self.parameter] in self.value_list:
					agent.restrict_recieve_infection()
					agent.restrict_contribute_infection()


class agent_policy_based_lockdown(Agent_Policy):
	def __init__(self,policy_to_consider,value_list,do_lockdown_fn):
		self.policy_type='Restrict'
		self.policy_to_consider = policy_to_consider
		self.do_lockdown_fn=do_lockdown_fn
		self.value_list=value_list

	def enact_policy(self,time_step,agents,locations,model=None):
		if self.do_lockdown_fn(time_step):
			for agent in agents:
				history = agent.get_policy_history(self.policy_to_consider)
				if(len(history) and history[-1].result in self.value_list):
					agent.restrict_recieve_infection()
					agent.restrict_contribute_infection()

'''
class location_lockdown(Policy):
	def __init__(self,parameter,value_list):
		self.policy_type='Lockdown'
		self.do_lockdown_fn=do_lockdown_fn
		self.parameter=parameter
		self.value_list=value_list

	def enact_policy(self,time_step,agents,locations):
		if self.do_lockdown_fn(time_step):
			for location in locations:
				if location.info[self.parameter] in self.value_list:
					location.lock_down_state=True
'''
