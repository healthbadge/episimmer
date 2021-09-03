import Lockdown_Policy
import Testing_Policy
import pickle

def get_num_agents_from_pickle_other(time_step):
	fp = open('IIITH_3_months_separate/tests_dict.pickle', 'rb')
	tests_dict = pickle.load(fp)
	if time_step in tests_dict.keys():
		return tests_dict[time_step]["Other"]
	else:
		return 0



def get_num_agents_from_pickle_rest(time_step):
	fp = open('IIITH_3_months_separate/tests_dict.pickle', 'rb')
	tests_dict = pickle.load(fp)
	if time_step in tests_dict.keys():
		return tests_dict[time_step]["Student"]+tests_dict[time_step]["Faculty"]+tests_dict[time_step]["Staff"]
	else:
		return 0

def event_restriction_fn(agent,event_info,current_time_step):
	"""
	Total days = 80 days.
	Total days = 20 days.
	"""
	if(current_time_step <= 19):
		if(event_info["Period"] == "Post-Lockdown"):
			return True
	else:
		if(event_info["Period"] == "Pre-Lockdown"):
			return True
	return False

def generate_policy():
	policy_list=[]
	"""
	Using only Total agents that are tested for Testing policy. 60% of total tests are agents randomly picked, the rest are based on
	symptomatic factors.
	"""
	Normal_Test = Testing_Policy.Test_Policy(get_num_agents_from_pickle_other)
	Normal_Test.add_machine('Simple_Machine', 200, 0.0, 0.0, 0, 500, 1)
	Normal_Test.set_register_agent_testtube_func(Normal_Test.random_agents_CR3(1,1,["Symptomatic"],"Other"))
	policy_list.append(Normal_Test)

	Normal_Test2 = Testing_Policy.Test_Policy(get_num_agents_from_pickle_rest)
	Normal_Test2.add_machine('Simple_Machine', 200, 0.0, 0.0, 0, 500, 1)
	Normal_Test2.set_register_agent_testtube_func(Normal_Test2.random_agents_CR3(1,1,["Symptomatic"],"Rest"))
	policy_list.append(Normal_Test2)

	ATP = Lockdown_Policy.agent_policy_based_lockdown("Testing",["Positive"],lambda x:True,12)
	policy_list.append(ATP)

	return policy_list,event_restriction_fn
