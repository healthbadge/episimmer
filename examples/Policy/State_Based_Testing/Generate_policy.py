import random

from episimmer.policy import lockdown_policy, testing_policy


def generate_policy():
	policy_list=[]

	# Pool Testing with specific agent states.
	Pool_Testing = testing_policy.TestPolicy(lambda x:5)
	Pool_Testing.add_machine('Simple_Machine', 200, 0.0, 0.0, 0, 50, 1)
	Pool_Testing.set_register_agent_testtube_func(Pool_Testing.state_testing(['Symptomatic']))
	policy_list.append(Pool_Testing)

	ATP = lockdown_policy.TestingBasedLockdown(lambda x:random.random()<0.95,10)
	policy_list.append(ATP)

	def event_restriction_fn(agent,event_info,current_time_step):
		return False

	return policy_list,event_restriction_fn
