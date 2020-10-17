import pickle
import sys
#sys.path.insert(1, '../')
import Model
import math

# In this example the rates change over time. 
# For example, due to improvement in treatment, those who go to ICU have higher chnace of recovery as time increases.

def generate_model():

	#User defined functions
	def fn1(current_time_step): #ICU recovery improves over time as doctors learn how to treat better
		return min(0.5,0.2+current_time_step*0.01)

	def fn2(current_time_step): #People going into ICU decreases due to better drugs
		return max(0.02,0.1-current_time_step*0.001)

	#Example Stochastic Model
	individual_types=['Susceptible','Infected','Recovered','ICU','Dead']
	infected_states=['Infected']
	model=Model.StochasticModel(individual_types,infected_states)
	model.set_transition('Susceptible', 'Infected', model.p_infection(None,None))
	model.set_transition('Infected', 'Recovered', model.p_standard(0.1))
	model.set_transition('Infected', 'ICU', model.p_function(fn2))
	model.set_transition('ICU', 'Recovered', model.p_function(fn1))
	model.set_transition('ICU', 'Dead', model.p_standard(0.05))


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


	model.set_event_contribution_fn(event_contribute_fn)
	model.set_event_recieve_fn(event_recieve_fn)

	return model







