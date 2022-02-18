import episimmer.model as model


#This function represents the probability of getting infected during a single interaction/contact
def probability_of_infection_fn(p_infected_states_list,contact_agent,c_dict,current_time_step):
	if contact_agent.state=='Infected':
		return 0.1  #This is the probability of getting infected from contact in a time step isf contact is infected
	return 0 # If contact is not infected then the probability of them infecting you is 0

class UserModel(model.StochasticModel):
	def __init__(self):
		individual_types=['Susceptible','Infected','Recovered']
		infected_states=['Infected']
		state_proportion={
							'Susceptible':0.97,
							'Infected':0.03,
							'Recovered':0
						}
		model.StochasticModel.__init__(self,individual_types,infected_states,state_proportion)
		self.set_transition('Susceptible', 'Infected', self.p_infection(probability_of_infection_fn,None))	#Adding S-> I transition which is based on probability_of_infection_fn
		self.set_transition('Infected', 'Recovered', self.p_standard(0.2))

		self.name='Stochastic SIR on complete graph'
