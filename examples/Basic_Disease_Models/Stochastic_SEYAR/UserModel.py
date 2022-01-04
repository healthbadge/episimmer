import Model

def event_contribute_fn(agent,event_info,location,current_time_step):
		if agent.state=='Symptomatic':
			return 1
		elif agent.state=='Asymptomatic':
			return 0.5
		return 0

def event_recieve_fn(agent,ambient_infection,event_info,location,current_time_step):
	#Example 1
	beta=0.001
	return ambient_infection*beta


class UserModel(Model.StochasticModel):
	def __init__(self):
		individual_types=['Susceptible','Exposed','Asymptomatic','Symptomatic','Recovered']
		infected_states=['Asymptomatic','Symptomatic']
		state_proportion={
							'Susceptible':0.99,
							'Exposed':0,
							'Recovered':0,
							'Asymptomatic':0,
							'Symptomatic':0.01
						}
		Model.StochasticModel.__init__(self,individual_types,infected_states,state_proportion)
		self.set_transition('Susceptible', 'Exposed', self.p_infection([None,None],None))
		self.set_transition('Exposed', 'Symptomatic', self.p_standard(0.15))
		self.set_transition('Exposed', 'Asymptomatic', self.p_standard(0.2))
		self.set_transition('Symptomatic', 'Recovered', self.p_standard(0.1))
		self.set_transition('Asymptomatic', 'Recovered', self.p_standard(0.1))

		self.set_event_contribution_fn(event_contribute_fn)
		self.set_event_recieve_fn(event_recieve_fn)