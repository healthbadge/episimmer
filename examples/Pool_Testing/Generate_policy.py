import Testing_Policy


def generate_policy():
	policy_list=[]

	TP = Testing_Policy.Test_Policy(lambda x:100)
	TP.add_machine('Simple_Machine', 200, 0.0, 0.0, 0, 50, 2)

	# Normal Testing
	#TP.set_register_agent_testtube_func(TP.random_agents(1,1))

	# Group/Pool Testing
	TP.set_register_agent_testtube_func(TP.random_agents(3,1))

	policy_list.append(TP)

	def event_restriction_fn(agent,event_info,current_time_step):
		return False

	return policy_list,event_restriction_fn
