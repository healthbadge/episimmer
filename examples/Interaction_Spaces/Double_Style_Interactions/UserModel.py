import episimmer.model as model


def probability_of_infection_fn(p_infected_states_list,contact_agent,c_dict,current_time_step):
	if contact_agent.state=='Infected':
		return 0.8
	return 0

class UserModel(model.StochasticModel):
	def __init__(self):
		individual_types=['Susceptible','Infected','Recovered']
		infected_states=['Infected']
		state_proportion={
							'Susceptible':0.8,
							'Infected':0.1,
							'Recovered':0.1
						}
		model.StochasticModel.__init__(self,individual_types,infected_states,state_proportion)
		self.set_transition('Susceptible', 'Infected', self.p_infection(probability_of_infection_fn,None))
		self.set_transition('Infected', 'Recovered', self.p_standard(0.2))



		self.name='Stochastic SIR'
