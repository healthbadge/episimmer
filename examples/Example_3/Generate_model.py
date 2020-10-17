import pickle
import sys
#sys.path.insert(1, '../')
import Model
import math

def generate_model():
	#Define Scheduled Model

	#This function is user defined, based on the parameters the user has inputed in agents file and interaction/contact file
	#This function represents the probability of getting infected during a single interaction/contact
	def probabilityOfInfection_fn(p_infected_states_list,contact_agent,c_dict,current_time_step):
		
		p_inf_symp,p_inf_asymp=p_infected_states_list[0],p_infected_states_list[1]
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


	model=Model.ScheduledModel()
	model.insert_state('Susceptible',None, None,model.p_infection([0.3,0.1],probabilityOfInfection_fn,{'Exposed':1}),False)
	model.insert_state('Exposed',5,2,model.scheduled({'Symptomatic':0.3,'Asymptomatic':0.7}),False)
	model.insert_state('Symptomatic',11,5,model.scheduled({'Recovered':1}),True)
	model.insert_state('Asymptomatic',6,3,model.scheduled({'Recovered':1}),True)
	model.insert_state('Recovered',100, 0,model.scheduled({'Recovered':1}),False)

	model.set_event_contribution_fn(None)
	model.set_event_recieve_fn(None)

	return model


