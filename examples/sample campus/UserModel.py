import Model
import math

#User defined functions

def event_contribute_fn(agent,event_info,location,current_time_step):
		#Example 1
		if agent.state=='Symptomatic':
			return 0.7
		elif agent.state=='Asymptomatic':
			return 0.3
		else:
			return 0

def event_recieve_fn(agent,ambient_infection,event_info,location,current_time_step):
	p=math.tanh(ambient_infection*0.3)
	return p




class UserModel(Model.StochasticModel):
	def __init__(self):
		individual_types=['Susceptible','Exposed','Asymptomatic','Symptomatic','Recovered']
		infected_states=['Asymptomatic','Symptomatic']
		state_proportion={
							'Susceptible':0.99,
							'Exposed':0.01,
							'Recovered':0,
							'Asymptomatic':0,
							'Symptomatic':0
						}
		Model.StochasticModel.__init__(self,individual_types,infected_states,state_proportion)
		self.set_transition('Susceptible', 'Exposed', self.p_infection([0.3,0.1],None))
		self.set_transition('Exposed', 'Symptomatic', self.p_standard(0.15))
		self.set_transition('Exposed', 'Asymptomatic', self.p_standard(0.2))
		self.set_transition('Symptomatic', 'Recovered', self.p_standard(0.2))
		self.set_transition('Asymptomatic', 'Recovered', self.p_standard(0.2))

		self.set_event_contribution_fn(event_contribute_fn)
		self.set_event_recieve_fn(event_recieve_fn)