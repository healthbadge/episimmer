import Model

def event_contribute_fn(agent,event_info,location,current_time_step):
		if agent.state=='Infected':
			return 1
		return 0

def event_recieve_fn(agent,ambient_infection,event_info,location,current_time_step):
	#Example 1
	beta=0.001
	return ambient_infection*beta


class UserModel(Model.StochasticModel):
	def __init__(self):
		individual_types=['Susceptible','Infected','Recovered']
		infected_states=['Infected']
		state_proportion={
							'Susceptible':0.99,
							'Infected':0.01,
							'Recovered':0
						}
		Model.StochasticModel.__init__(self,individual_types,infected_states,state_proportion)
		self.set_transition('Susceptible', 'Infected', self.p_infection(None,None))
		self.set_transition('Infected', 'Recovered', self.p_standard(0.2))


		self.set_event_contribution_fn(event_contribute_fn)
		self.set_event_recieve_fn(event_recieve_fn)