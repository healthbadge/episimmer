import pickle
import sys
#sys.path.insert(1, '../')
import Model
import math

def generate_model():

	#Example Stochastic Model
	'''
	individual_types=['Susceptible','Infected','Recovered','ICU','Dead']
	infected_states=['Infected']
	model=Model.StochasticModel(individual_types,infected_states)
	model.set_transition('Susceptible', 'Infected', model.p_infection(None,None))
	model.set_transition('Infected', 'Recovered', model.p_standard(0.1))
	model.set_transition('Infected', 'ICU', model.p_standard(0.1))
	model.set_transition('ICU', 'Recovered', model.p_standard(0.2))
	model.set_transition('ICU', 'Dead', model.p_standard(0.05))
	'''
	#Example Scheduled Model
	model=Model.ScheduledModel()
	model.insert_state('Susceptible',None, None,model.p_infection(None,None,{'Infected':1}),True)
	model.insert_state('Infected',7,1,model.scheduled({'Recovered':0.7, 'ICU':0.3}),True)
	model.insert_state('Recovered',None, None,model.scheduled({'Recovered':1}),False)
	model.insert_state('ICU',4,1,model.scheduled({'Recovered':1}),False)
	


	def event_contribute_fn(agent,event_info,location):
		if agent.state=='Infected':
			return 1
		return 0

	def event_recieve_fn(agent,ambient_infection,event_info,location):
		#Example 1
		beta=0.0001
		return ambient_infection*beta


	model.set_event_contribution_fn(event_contribute_fn)
	model.set_event_recieve_fn(event_recieve_fn)

	return model







