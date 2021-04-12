import random

class Policy():
	def __init__(self):
		self.policy_name=None

	def enact_policy(self,time_step,agents,locations):
		pass

class full_lockdown(Policy):
	def __init__(self,do_lockdown_fn):
		self.do_lockdown_fn=do_lockdown_fn

	def enact_policy(self,time_step,agents,locations):
		if self.do_lockdown_fn(time_step):
			for agent in agents:
				agent.lock_down_state=True

class agent_lockdown(Policy):
	def __init__(self,parameter,value_list,do_lockdown_fn):
		self.do_lockdown_fn=do_lockdown_fn
		self.parameter=parameter
		self.value_list=value_list

	def enact_policy(self,time_step,agents,locations):
		if self.do_lockdown_fn(time_step):
			for agent in agents:
				if agent.info[self.parameter] in self.value_list:
					agent.lock_down_state=True

class location_lockdown(Policy):
	def __init__(self,parameter,value_list):
		self.do_lockdown_fn=do_lockdown_fn
		self.parameter=parameter
		self.value_list=value_list

	def enact_policy(self,time_step,agents,locations):
		if self.do_lockdown_fn(time_step):
			for location in locations:
				if location.info[self.parameter] in self.value_list:
					location.lock_down_state=True

'''
class Vaccination(Policy):
	def __init__(self,vaccinations_per_time_step_fn,vaccination_state,scheduled_time,agents_obj):
		self.vaccinations_per_time_step_fn=vaccinations_per_time_step_fn
		self.agents=agents_obj.agents
		self.not_vaccinated_index=[]

		for agent_index in self.agents.keys():
			self.not_vaccinated_index.append(agent_index)

		random.shuffle(self.not_vaccinated_index)

	def enact_policy(self,time_step,agents,locations):
'''



