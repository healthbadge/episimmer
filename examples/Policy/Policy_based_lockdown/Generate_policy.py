import random

from episimmer.policy import lockdown_policy, testing_policy


def generate_policy():
	policy_list=[]

	TP = testing_policy.TestPolicy(lambda x:100)
	TP.add_machine('Simple_Machine', 200, 0.0, 0.0, 0, 50, 2)

	TP.set_register_agent_testtube_func(TP.random_agents(3,1))

	policy_list.append(TP)

	ATP = lockdown_policy.TestingBasedLockdown(lambda x:random.random()<0.95,10)
	policy_list.append(ATP)

	def event_restriction_fn(agent,event_info,current_time_step):
		return False

	return policy_list,event_restriction_fn
