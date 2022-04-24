import random

from episimmer.policy import lockdown_policy, testing_policy


def generate_policy():
	policy_list=[]

	# Normal Testing
	# Normal_Test = testing_policy.TestPolicy(lambda x:120)
	# Normal_Test.add_machine('Simple_Machine', 200, 0.0, 0.0, 0, 60, 5, 2)
	# Normal_Test.set_register_agent_testtube_func(Normal_Test.random_testing(1,1))
	# policy_list.append(Normal_Test)

	# Group/Pool Testing
	Pool_Testing = testing_policy.TestPolicy(lambda x:150)
	Pool_Testing.add_machine('Simple_Machine', 200, 0.0, 0.0, 0, 50, 3, 3)
	Pool_Testing.set_register_agent_testtube_func(Pool_Testing.random_testing(5,2))
	policy_list.append(Pool_Testing)

	ATP = lockdown_policy.TestingBasedLockdown(lambda x:random.random()<0.95,10)
	policy_list.append(ATP)

	return policy_list
