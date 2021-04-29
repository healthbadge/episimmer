import Lockdown_Policy
import Testing_Policy
import random

def generate_policy():
	policy_list=[]

	def lockdown_fn(time_step):
		return False

	policy_list.append(Lockdown_Policy.full_lockdown(lockdown_fn))
	TP = Testing_Policy.Test_Policy(lambda x:54)
	TP.add_machine('Simple_Machine', 200, 0.0, 0.0, 0, 50, 2)
	# TP.add_machine('Simple_Machine2', 200, 0.0, 0.0, 1, 100, 1)
	# TP.add_machine('Simple_Machine3', 200, 0.0, 0.0, 2, 120, 1)
	# TP.add_machine('Simple_Machine3', 200, 0.0, 0.0, 2, 120, 1)
	TP.set_register_agent_testtube_func(TP.random_agents(1,1))
	policy_list.append(TP)

	ATP = Lockdown_Policy.agent_policy_based_lockdown("Testing",["Positive"],lambda x:random.random()<0.95)
	policy_list.append(ATP)

	def event_restriction_fn(agent,event_info,current_time_step):
		return False

	return policy_list,event_restriction_fn
