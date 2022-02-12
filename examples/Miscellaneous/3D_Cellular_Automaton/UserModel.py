import episimmer.model as model


def probability_of_infection_fn(p_infected_states_list, contact_agent, c_dict, current_time_step):
	if contact_agent.state in ['Exposed', 'Symptomatic', 'Asymptomatic']:
		return 0.5
	return 0

class UserModel(model.ScheduledModel):
	def __init__(self):
		model.ScheduledModel.__init__(self)
		self.insert_state('Susceptible', None, None, self.p_infection({'Exposed':1},probability_of_infection_fn,[0.3, 0.1]),False,0.90)
		self.insert_state('Exposed', 5, 2, self.scheduled({'Symptomatic':0.3,'Asymptomatic':0.7}),False,0.02)
		self.insert_state('Symptomatic', 30, 5, self.scheduled({'Recovered':1}),True,0.03)
		self.insert_state('Asymptomatic', 25, 3, self.scheduled({'Recovered':1}),True,0.05)
		self.insert_state('Recovered', 100, 0, self.scheduled({'Recovered': 1}),False,0)
