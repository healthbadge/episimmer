from episimmer.policy import lockdown_policy


def generate_policy():
	policy_list=[]

	def lockdown_fn(time_step):
		return False

	policy_list.append(lockdown_policy.FullLockdown(lockdown_fn))

	def event_restriction_fn(agent,event_info,current_time_step):
		return False

	return policy_list,event_restriction_fn
