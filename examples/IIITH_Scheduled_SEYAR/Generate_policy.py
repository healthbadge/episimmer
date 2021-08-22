import Lockdown_Policy

def generate_policy():
	policy_list=[]

	def lockdown_fn(time_step):
		return False

	policy_list.append(Lockdown_Policy.full_lockdown(lockdown_fn))

	def event_restriction_fn(agent,event_info,current_time_step):
		"""
		Total days from 03.02.2021 to 14.06.2021 = 132 days.
		Total days from 03.02.2021 to 15.04.2021 = 72 days.
		"""
		if(current_time_step <= 71):
			if(event_info["Period"] == "Post-Lockdown"):
				return True
		else:
			if(event_info["Period"] == "Pre-Lockdown"):
				return True
		return False

	return policy_list,event_restriction_fn
