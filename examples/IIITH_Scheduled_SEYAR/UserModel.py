import Model

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
	if event_info["Level"] == "Campus_Level":
		beta= 0.0

	elif event_info["Level"] == "Student_Level":
		beta= 0.0
	elif event_info["Level"] == "Hostel_Level":
		beta= 0.0000005
	elif event_info["Level"] == "Floor_Level":
		beta= 0.000005
	elif event_info["Level"] == "Room_Level":
		beta= 0.00005
	elif event_info["Level"] == "Mess_Level":
		beta= 0.00005

	elif event_info["Level"] == "Flat_Level":
		beta= 0.000005
	elif event_info["Level"] == "Quarter_Level":
		beta= 0.0000005

	elif event_info["Level"] == "Staff_Level":
		beta= 0.000005
	elif event_info["Level"] == "Others_Level":
		beta= 0.000005
	return beta*ambient_infection

def external_prevalence(agent, current_time_step):
	"""
	Type : ["Student", "Faculty", "Staff", "Others"]
	Pre-Lockdown : current_time_step<=71 ; Post-Lockdown : current_time_step>71
	"""
	if current_time_step <=71:
		if(agent.info['Type'] == 'Faculty'):
			return 0.001
		elif(agent.info['Type'] in ['Others', 'Staff']):
			return 0.0035
		elif(agent.info['Type'] == 'Student'):
			return 0.002
	else:
		if(agent.info['Type'] == 'Faculty'):
			return 0.001
		elif(agent.info['Type'] in ['Others', 'Staff']):
			return 0.0035
		elif(agent.info['Type'] == 'Student'):
			return 0.002

class UserModel(Model.ScheduledModel):
	def __init__(self):
		Model.ScheduledModel.__init__(self)
		self.insert_state('Susceptible',None, None,self.p_infection([0.3,0.1],None,{'Exposed':1}),False,1.0)
		self.insert_state('Exposed',5,2,self.scheduled({'Symptomatic':0.3,'Asymptomatic':0.7}),False,0)
		self.insert_state('Symptomatic',11,5,self.scheduled({'Recovered':1}),True,0)
		self.insert_state('Asymptomatic',6,3,self.scheduled({'Recovered':1}),True,0)
		self.insert_state('Recovered',100, 0,self.scheduled({'Recovered':1}),False,0)

		self.set_event_contribution_fn(event_contribute_fn)
		self.set_event_recieve_fn(event_recieve_fn)

		self.set_external_prevalence_fn(external_prevalence)
