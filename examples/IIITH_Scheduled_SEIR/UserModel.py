import Model
import random
import numpy as np
import math

def event_contribute_fn(agent,event_info,location,current_time_step):
		if agent.state=='Infected':
			return 1
		return 0

def event_recieve_fn(agent,ambient_infection,event_info,location,current_time_step):
	if event_info["Type"] == "Hostel":
		beta= 0.0002
	elif event_info["Type"] == "Mess":
		beta= 0.0002
	elif event_info["Type"] == "Class":
		beta= 0.0002
	elif event_info["Type"] == "Campus":
		beta= 0.00002
	return ambient_infection*beta

def incubation_fn(time_step):
	return np.random.lognormal(1.8, 0.52, 1)[0]


class UserModel(Model.ScheduledModel):
	def __init__(self):
		Model.ScheduledModel.__init__(self)
		self.insert_state('Susceptible', None, None, self.p_infection([None],None,{'Exposed':1}),False,0.98)
		self.insert_state_custom('Exposed', incubation_fn, self.p_function({'Infected':1}),False,0.01)
		self.insert_state('Infected',14,1,self.scheduled({'Recovered':1}),True,0.01)
		self.insert_state('Recovered',0,0,self.scheduled({'Recovered':1}),False,0)

		self.set_event_contribution_fn(event_contribute_fn)
		self.set_event_recieve_fn(event_recieve_fn)
