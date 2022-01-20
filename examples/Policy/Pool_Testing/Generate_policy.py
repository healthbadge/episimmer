import random

from episimmer.policy import lockdown_policy, testing_policy


def generate_policy():
	policy_list=[]

	# Normal Testing
	#Normal_Test = Testing_Policy.TestPolicy(lambda x:60)
	#Normal_Test.add_machine('Simple_Machine', 200, 0.0, 0.0, 0, 50, 2)
	#Normal_Test.set_register_agent_testtube_func(Normal_Test.random_agents(1,1))
	#policy_list.append(Normal_Test)

	# Group/Pool Testing
	Pool_Testing = testing_policy.TestPolicy(lambda x:150)
	Pool_Testing.add_machine('Simple_Machine', 200, 0.0, 0.0, 0, 50, 2)
	Pool_Testing.set_register_agent_testtube_func(Pool_Testing.random_agents(5,2))
	policy_list.append(Pool_Testing)

	ATP = lockdown_policy.TestingBasedLockdown(lambda x:random.random()<0.95,10)
	policy_list.append(ATP)

	def event_restriction_fn(agent,event_info,current_time_step):
		return False

	return policy_list,event_restriction_fn
