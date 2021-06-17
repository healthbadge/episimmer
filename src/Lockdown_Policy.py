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
	def __init__(self,policy_to_consider,value_list,do_lockdown_fn,time_period):
		self.policy_type='Restrict'
		self.policy_to_consider = policy_to_consider
		self.do_lockdown_fn=do_lockdown_fn
		self.value_list=value_list
		self.time_period = time_period

	def enact_policy(self,time_step,agents,locations,model=None):
		if self.do_lockdown_fn(time_step):
			for agent in agents:
				history = agent.get_policy_history(self.policy_to_consider)
				if(len(history)):
					last_time_step = history[-1].time_step
					if(time_step - last_time_step < self.time_period):
						result = self.get_accumulated_result(history,last_time_step)
						if(result in self.value_list):
							agent.restrict_recieve_infection()
							agent.restrict_contribute_infection()

	def get_accumulated_result(self,history,last_time_step):

		indx = len(history)-1
		while(indx>=0 and history[indx].time_step==last_time_step):
			if(history[indx].result == "Negative"):
				return "Negative"

			indx-=1

		return "Positive"



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
