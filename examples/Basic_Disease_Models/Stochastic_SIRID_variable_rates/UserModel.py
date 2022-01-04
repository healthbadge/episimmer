import Model
import math

#User defined functions
def fn1(current_time_step): #ICU recovery improves over time as doctors learn how to treat better
	return min(0.5,0.2+current_time_step*0.01)

def fn2(current_time_step): #People going into ICU decreases due to better drugs
	return max(0.02,0.1-current_time_step*0.001)

def event_contribute_fn(agent,event_info,location,current_time_step):
		if agent.state=='Infected':
			return 1
		return 0

def event_recieve_fn(agent,ambient_infection,event_info,location,current_time_step):
	#Example 1
	#6th to 10th day lockdown so no spread, after that precations are taken so rate of infection decreases
	if current_time_step<5:
		beta=0.001
	elif current_time_step<10:
		beta=0
	else:
		beta=0.0008
	return ambient_infection*beta


class UserModel(Model.StochasticModel):
	def __init__(self):
		individual_types=['Susceptible','Infected','Recovered','ICU','Dead']
		infected_states=['Infected']
		state_proportion={
							'Susceptible':0.99,
							'Infected':0.01,
							'Recovered':0,
							'ICU':0,
							'Dead':0
						}
		Model.StochasticModel.__init__(self,individual_types,infected_states,state_proportion)
		self.set_transition('Susceptible', 'Infected', self.p_infection(None,None))
		self.set_transition('Infected', 'Recovered', self.p_standard(0.1))
		self.set_transition('Infected', 'ICU', self.p_function(fn2))
		self.set_transition('ICU', 'Recovered', self.p_function(fn1))
		self.set_transition('ICU', 'Dead', self.p_standard(0.05))

		self.set_event_contribution_fn(event_contribute_fn)
		self.set_event_recieve_fn(event_recieve_fn)