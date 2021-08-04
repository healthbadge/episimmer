import Lockdown_Policy
import Testing_Policy
import pickle
import numpy as np


def get_num_agents_from_pickle(time_step):
	fp = open('Stochastic_SIR_CR/tests_dict.pickle', 'rb')
	tests_dict = pickle.load(fp)
	if time_step in tests_dict.keys():
		return tests_dict[time_step]['num_st_tested']
	else:
		return 0

def generate_policy():
	policy_list=[]

	def lockdown_fn(time_step):
		return True

	bin_student_attendance = np.load('Stochastic_SIR_CR/student_attendance.npy')
	policy_list.append(Lockdown_Policy.agent_lockdown_CR(lockdown_fn, bin_student_attendance))

	Normal_Test = Testing_Policy.Test_Policy(get_num_agents_from_pickle)
	Normal_Test.add_machine('Simple_Machine', 200, 0.0, 0.0, 0, 500, 1)
	Normal_Test.set_register_agent_testtube_func(Normal_Test.random_agents_CR(1,1))
	policy_list.append(Normal_Test)

	# ATP = Lockdown_Policy.agent_policy_based_lockdown("Testing",["Positive"],lambda x:True,10)
	# policy_list.append(ATP)

	def event_restriction_fn(agent,event_info,current_time_step):
		return False

	return policy_list,event_restriction_fn
