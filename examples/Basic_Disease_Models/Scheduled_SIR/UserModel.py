import episimmer.model as model


def event_contribute_fn(agent,event_info,location,current_time_step):
		if agent.state=='Infected':
			return 1
		return 0

def event_receive_fn(agent,ambient_infection,event_info,location,current_time_step):
	#Example 1
	beta=0.001
	return ambient_infection*beta


class UserModel(model.ScheduledModel):
	def __init__(self):
		model.ScheduledModel.__init__(self)
		self.insert_state('Susceptible',None, None,self.p_infection({'Infected':1}),False,0.99)
		self.insert_state('Infected',6,3,self.scheduled({'Recovered':1}),True,0.01)
		self.insert_state('Recovered',0, 0,self.scheduled({'Recovered':1}),False,0)

		self.set_event_contribution_fn(event_contribute_fn)
		self.set_event_receive_fn(event_receive_fn)
