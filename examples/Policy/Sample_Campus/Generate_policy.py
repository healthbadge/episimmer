from episimmer.policy import lockdown_policy


def monday_online():
	#This function ensures classes are online on Monday
	policy_list=[]

	def lockdown_fn(time_step):
		if time_step%7 in [0]:
			return True
		return False

	policy_list.append(lockdown_policy.FullLockdown(lockdown_fn))

	return policy_list

def tuesday_thursday_online():
	#This function ensures classes are online on Tuesday and Thursday
	policy_list=[]

	def lockdown_fn(time_step):
		if time_step%7 in [1,3]:
			return True
		return False

	policy_list.append(lockdown_policy.FullLockdown(lockdown_fn))

	return policy_list

def monday_tuesday_online():
	#This function ensures classes are online on Monday and Tuesday
	policy_list=[]

	def lockdown_fn(time_step):
		if time_step%7 in [1,3]:
			return True
		return False

	policy_list.append(lockdown_policy.FullLockdown(lockdown_fn))

	return policy_list

def monday_no_grade1():
	#This function ensures that there are no grade 1 students on Monday
	policy_list=[]

	def lockdown_fn(time_step):
		if time_step%7 in [0]:
			return True
		return False

	policy_list.append(lockdown_policy.AgentLockdown('Grade',['Grade 1'],lockdown_fn))

	return policy_list

def wednesday_no_grade1_grade2():
	#This function ensures that there are no grade 2 students on Wednesday
	policy_list=[]

	def lockdown_fn(time_step):
		if time_step%7 in [2]:
			return True
		return False

	policy_list.append(lockdown_policy.AgentLockdown('Grade',['Grade 1','Grade 2'],lockdown_fn))

	return policy_list

def mw_no_grade1_tf_no_grade3():
	#This function ensures that there are no grade 1 students on Monday,Wednesday and grade 3 students on tuesday,friday
	policy_list=[]

	def lockdown_mw(time_step):
		if time_step%7 in [0,2]:
			return True
		return False

	def lockdown_tf(time_step):
		if time_step%7 in [1,4]:
			return True
		return False

	policy_list.append(lockdown_policy.AgentLockdown('Grade',['Grade 1'],lockdown_mw))
	policy_list.append(lockdown_policy.AgentLockdown('Grade',['Grade 3'],lockdown_tf))

	return policy_list

def mt_no_grade2_wednesday_online():
	#This function ensures that there are no grade 1 students on Monday,tuesday and wednesday is online
	policy_list=[]

	def lockdown_mt(time_step):
		if time_step%7 in [0,1]:
			return True
		return False

	def lockdown_wednesday(time_step):
		if time_step%7 in [2]:
			return True
		return False

	policy_list.append(lockdown_policy.AgentLockdown('Grade',['Grade 1'],lockdown_mt))
	policy_list.append(lockdown_policy.FullLockdown(lockdown_wednesday))

	return policy_list


def generate_policy():
	#return monday_online()
	return tuesday_thursday_online()
	#return monday_tuesday_online()
	#return monday_no_grade1()
	#return wednesday_no_grade1_grade2()
	#return mw_no_grade1_tf_no_grade3()
	return mt_no_grade2_wednesday_online()
