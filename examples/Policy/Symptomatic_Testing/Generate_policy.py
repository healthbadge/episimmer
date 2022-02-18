import random

from episimmer.policy import lockdown_policy, testing_policy


def generate_policy():
	policy_list=[]

	# Testing only symptomatic agents.
	Normal_Testing = testing_policy.TestPolicy(lambda x:5)
	Normal_Testing.add_machine('Simple_Machine', 200, 0.0, 0.0, 0, 50, 3, 1)
	Normal_Testing.set_register_agent_testtube_func(Normal_Testing.random_testing(only_symptomatic=True))
	policy_list.append(Normal_Testing)

	ATP = lockdown_policy.TestingBasedLockdown(lambda x:random.random()<0.95,10)
	policy_list.append(ATP)

	return policy_list
