import Model
import numpy as np

def event_contribute_fn(agent,event_info,location,current_time_step):
		if agent.state=='Symptomatic':
			return 1
		elif agent.state=='Asymptomatic':
			return 0.6
		return 0

def event_recieve_fn(agent,ambient_infection,event_info,location,current_time_step):
	"""
	All levels : ["Campus_Level", "Student_Level", "Hostel_Level", "Floor_Level", "Room_Level", "Mess_Level",\
					"Flat_Level", "Quarter_Level", "Staff_Level", "Others_Level"]
	"""
	lockdown_coefficient = None
	if current_time_step <=19:
		lockdown_coefficient = 0.8
	elif current_time_step >19 and current_time_step<=26:
		lockdown_coefficient = 0.1
	else:
		lockdown_coefficient = 0.2

	if event_info["Level"] == "Campus_Level":
		beta= 0.00008
		beta = beta*lockdown_coefficient

	elif event_info["Level"] == "Student_Level":
		beta= 0.0001
		beta = beta*lockdown_coefficient
		# beta=0

	elif event_info["Level"] == "Hostel_Level":
		beta= 0.00015
		beta = beta*lockdown_coefficient
	elif event_info["Level"] == "Floor_Level":
		beta= 0.0002
	elif event_info["Level"] == "Room_Level":
		beta= 0.0003
	elif event_info["Level"] == "Mess_Level":
		beta= 0.00015
		beta = beta*lockdown_coefficient

	elif event_info["Level"] == "Flat_Level":
		beta= 0.0003
	elif event_info["Level"] == "Quarter_Level":
		beta= 0.00015
		beta = beta*lockdown_coefficient

	elif event_info["Level"] == "Staff_Level":
		beta= 0.00015
		beta = beta*lockdown_coefficient
	elif event_info["Level"] == "Others_Level":
		beta= 0.0002
		beta = beta*lockdown_coefficient
	scale = 14
	return scale*beta*ambient_infection

def external_prevalence(agent, current_time_step):
	"""
	Type : ["Student", "Faculty", "Staff", "Others"]
	Pre-Lockdown : current_time_step<=14 ; Post-Lockdown : current_time_step>14
	"""
	# if current_time_step <=14:
	# 	if(agent.info['Type'] == 'Faculty'):
	# 		return 0.001
	# 	elif(agent.info['Type'] in ['Others', 'Staff']):
	# 		return 0.0035
	# 	elif(agent.info['Type'] == 'Student'):
	# 		return 0.002
	# else:
	# 	if(agent.info['Type'] == 'Faculty'):
	# 		return 0.001
	# 	elif(agent.info['Type'] in ['Others', 'Staff']):
	# 		return 0.0035
	# 	elif(agent.info['Type'] == 'Student'):
	# 		return 0.002

	if(agent.info['Type'] in ['Others', 'Staff']):
		if current_time_step <=19:
			return current_time_step/19*0.012

		elif current_time_step >19 and current_time_step <=26:
			return 0.001

		elif current_time_step >26:
			return 0.003
	return 0

def incubation_fn(time_step):
	return np.random.lognormal(1.8, 0.52, 1)[0]


class UserModel(Model.ScheduledModel):
	def __init__(self):
		Model.ScheduledModel.__init__(self)
		self.insert_state('Susceptible',None, None,self.p_infection([0.3,0.1],None,{'Exposed':1}),False,0.998)
		self.insert_state_custom('Exposed', incubation_fn, self.p_function({'Symptomatic':0.4,'Asymptomatic':0.6}),False,0.0)
		self.insert_state('Symptomatic',11,1,self.scheduled({'Recovered':1}),True,0.002)
		self.insert_state('Asymptomatic',9,1,self.scheduled({'Recovered':1}),True,0)
		self.insert_state('Recovered',300, 0,self.scheduled({'Recovered':1}),False,0)

		self.set_event_contribution_fn(event_contribute_fn)
		self.set_event_recieve_fn(event_recieve_fn)

		self.set_external_prevalence_fn(external_prevalence)
