import Testing_Policy
import Lockdown_Policy
import random

def generate_policy():
	policy_list=[]

	Pool_Testing = Testing_Policy.Test_Policy(lambda x:3)
	Pool_Testing.add_machine('Simple_Machine', 200, 0.0, 0.0, 0, 50, 2)
	Pool_Testing.set_register_agent_testtube_func(Pool_Testing.random_agents(3,2))
	policy_list.append(Pool_Testing)

	ATP = Lockdown_Policy.agent_policy_based_lockdown("Testing",["Positive"],lambda x:random.random()<0.95,10)
	policy_list.append(ATP)

	def event_restriction_fn(agent,event_info,current_time_step):
		return False

	return policy_list,event_restriction_fn
