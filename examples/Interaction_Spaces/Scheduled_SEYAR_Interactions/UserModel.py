import episimmer.model as model


def probabilityOfInfection_fn(p_infected_states_list,contact_agent,c_dict,current_time_step):
	if contact_agent.state=='Infected':
		return 0.1
	return 0

def event_contribute_fn(agent,event_info,location,current_time_step):
		if agent.state=='Symptomatic':
			return 1
		elif agent.state=='Asymptomatic':
			return 0.6
		return 0

def event_receive_fn(agent,ambient_infection,event_info,location,current_time_step):
	beta=0.001
	return ambient_infection*beta


class UserModel(model.ScheduledModel):
	def __init__(self):
		model.ScheduledModel.__init__(self)
		self.insert_state('Susceptible',None, None,self.p_infection({'Exposed':1},probabilityOfInfection_fn,[0.3,0.1]),False,0.95)
		self.insert_state('Exposed',5,2,self.scheduled({'Symptomatic':0.3,'Asymptomatic':0.7}),False,0.02)
		self.insert_state('Symptomatic',11,5,self.scheduled({'Recovered':1}),True,0.02)
		self.insert_state('Asymptomatic',6,3,self.scheduled({'Recovered':1}),True,0.01)
		self.insert_state('Recovered',100, 0,self.scheduled({'Recovered':1}),False,0)

		self.set_event_contribution_fn(event_contribute_fn)
		self.set_event_receive_fn(event_receive_fn)
