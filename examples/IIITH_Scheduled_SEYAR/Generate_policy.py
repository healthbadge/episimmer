import Lockdown_Policy
import Testing_Policy
import pickle

def get_num_agents_from_pickle(time_step):
	fp = open('IIITH_Scheduled_SEYAR/tests_dict.pickle', 'rb')
	tests_dict = pickle.load(fp)
	if time_step in tests_dict.keys():
		return tests_dict[time_step]['num_st_tested']
	else:
		return 0

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

def generate_policy():
	policy_list=[]
	"""
	Using only Total agents that are tested for Testing policy. 60% of total tests are agents randomly picked, the rest are based on
	symptomatic factors.
	"""
	Normal_Test = Testing_Policy.Test_Policy(get_num_agents_from_pickle)
	Normal_Test.add_machine('Simple_Machine', 200, 0.0, 0.0, 0, 500, 1)
	Normal_Test.set_register_agent_testtube_func(Normal_Test.random_agents_CR2(1,1,["Symptomatic"]))
	policy_list.append(Normal_Test)

	ATP = Lockdown_Policy.agent_policy_based_lockdown("Testing",["Positive"],lambda x:True,10)
	policy_list.append(ATP)

	return policy_list,event_restriction_fn
