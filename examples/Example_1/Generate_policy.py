import Policy

def generate_policy():
	policy_list=[]

	def lockdown_fn(time_step):

		return False

	policy_list.append(Policy.full_lockdown(lockdown_fn))

	return policy_list


