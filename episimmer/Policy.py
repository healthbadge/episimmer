import random

class Policy():
	def __init__(self):
		self.policy_name=None

	def enact_policy(self,time_step):
		pass

class Lockdown(Policy):
	def __init__(self,do_lockdown_fn):
		self.do_lockdown_fn=do_lockdown_fn


'''class Vaccination(Policy):
	def __init__(self,vaccinations_per_time_step,vaccination_state, scheduled_time_of_effectivess,agents_obj):
		self.agents=agents_obj.agents
		self.not_vaccinated_index=[]

		for agent_index in self.agents.keys():
			self.not_vaccinated_index.append(agent_index)
'''

