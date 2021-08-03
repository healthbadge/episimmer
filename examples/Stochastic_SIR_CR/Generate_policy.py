import Lockdown_Policy
import numpy as np

def generate_policy():
	policy_list=[]

	def lockdown_fn(time_step):
		return True

	bin_student_attendance = np.load('Stochastic_SIR_CR/student_attendance.npy')
	policy_list.append(Lockdown_Policy.agent_lockdown_CR(lockdown_fn, bin_student_attendance))

	def event_restriction_fn(agent,event_info,current_time_step):
		return False

	return policy_list,event_restriction_fn
