from episimmer.policy import lockdown_policy, testing_policy


def generate_policy():
	policy_list=[]

	event_lockdown = lockdown_policy.EventLockdown('Type', ['Low Priority'], lambda x: True)
	policy_list.append(event_lockdown)

	return policy_list
