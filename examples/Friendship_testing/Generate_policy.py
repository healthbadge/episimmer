import Testing_Policy
import Lockdown_Policy
import random

def generate_policy():
	policy_list=[]

	# Friendship testing
	Normal_Test = Testing_Policy.Test_Policy(lambda x:60)
	Normal_Test.add_machine('Simple_Machine', 200, 0.0, 0.0, 0, 50, 2)
	Normal_Test.set_register_agent_testtube_func(Normal_Test.friendship_testing(5))
	policy_list.append(Normal_Test)


	ATP = Lockdown_Policy.agent_policy_based_lockdown("Testing",["Positive"],lambda x:random.random()<0.95,10)
	policy_list.append(ATP)

	def event_restriction_fn(agent,event_info,current_time_step):
		return False

	return policy_list,event_restriction_fn
