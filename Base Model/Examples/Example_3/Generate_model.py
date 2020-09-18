import pickle
import sys
#sys.path.insert(1, '../')
import Model
import math

def generate_model():
	#Define Scheduled Model

	#This function is user defined, based on the parameters the user has inputed in agents file and interaction/contact file
	#This function represents the probability of getting infected during a single interaction/contact
	def probabilityOfInfection_fn(p_inf_symp,p_inf_asymp,contact_agent,c_dict):

		#Example 2
		if contact_agent.state=='Symptomatic':
			return (float(c_dict['Room Ventilation'])+0.1)*p_inf_symp
		elif contact_agent.state=='Asymptomatic':
			return (float(c_dict['Room Ventilation'])+0.1)*p_inf_asymp
		else:
			return 0


	model=Model.ScheduledModel()
	model.insert_state('Susceptible',None, None,model.p_infection(0.3,0.1,probabilityOfInfection_fn,{'Exposed':1}))
	model.insert_state('Exposed',5,2,model.scheduled({'Symptomatic':0.7,'Asymptomatic':0.3}))
	model.insert_state('Symptomatic',7,1,model.scheduled({'Recovered':0.7, 'ICU':0.3}))
	model.insert_state('ICU',10,5,model.scheduled({'Recovered':0.1,'Dead':0.9}))
	model.insert_state('Asymptomatic',6,3,model.scheduled({'Recovered':1}))
	model.insert_state('Recovered',None, None,model.scheduled({'Recovered':1}))
	model.insert_state('Dead',None, None,model.scheduled({'Dead':1}))

	return model


