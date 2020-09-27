import pickle
import sys
#sys.path.insert(1, '../')
import Model
import math

def generate_model():
	#Define Stochastic Model

	#This function is user defined, based on the parameters the user has inputed in agents file and interaction/contact file
	#This function represents the probability of getting infected during a single interaction/contact
	def probabilityOfInfection_fn(p_inf_symp,p_inf_asymp,contact_agent,c_dict):
		#EXAMPLE 1
		if contact_agent.state=='Symptomatic':
			return math.tanh(float(c_dict['Time Interval']))*p_inf_symp
		elif contact_agent.state=='Asymptomatic':
			return math.tanh(float(c_dict['Time Interval']))*p_inf_asymp
		else:
			return 0

		#Example 2
		if contact_agent.state=='Symptomatic':
			return math.tanh(float(c_dict['Time Interval'])*float(c_dict['Intensity']))*p_inf_symp
		elif contact_agent.state=='Asymptomatic':
			return math.tanh(float(c_dict['Time Interval'])*float(c_dict['Intensity']))*p_inf_asymp
		else:
			return 0

	individual_types=['Susceptible','Exposed','Asymptomatic','Symptomatic','Recovered']
	model=Model.StochasticModel(individual_types)
	model.set_transition('Susceptible', 'Exposed', model.p_infection(0.3,0.1,probabilityOfInfection_fn))
	model.set_transition('Exposed', 'Symptomatic', model.p_standard(0.15))
	model.set_transition('Exposed', 'Asymptomatic', model.p_standard(0.2))
	model.set_transition('Symptomatic', 'Recovered', model.p_standard(0.2))
	model.set_transition('Asymptomatic', 'Recovered', model.p_standard(0.2))

	def event_contribute_fn(agent,event_info,location):
		#Example 1
		if agent.state=='Symptomatic':
			return 1
		elif agent.state=='Asymptomatic':
			return 0.3
		else:
			return 0

		#Example 2
		susceptibility=1
		if agent.info['HLA Type']=='A':
			susceptibility=0.9

		if agent.state=='Symptomatic':
			return math.tanh(float(event_info['Time Interval']))*(1-location.info['Ventilation'])*susceptibility
		elif agent.state=='Asymptomatic':
			return 0.3*math.tanh(float(event_info['Time Interval']))*(1-location.info['Ventilation'])*susceptibility

	def event_recieve_fn(agent,ambient_infection,event_info,location):
		p=math.tanh(ambient_infection*0.3)
		return p

	model.set_event_contribution_fn(event_contribute_fn)
	model.set_event_recieve_fn(event_recieve_fn)

	return model

#f = open("example_model", "wb")
#pickle.dump(model, f)
#f.close()

