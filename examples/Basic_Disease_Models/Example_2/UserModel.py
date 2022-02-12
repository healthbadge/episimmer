import math

import episimmer.model as model


#User defined functions
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



class UserModel(model.ScheduledModel):
	def __init__(self):
		model.ScheduledModel.__init__(self)
		self.insert_state('Susceptible',None, None,self.p_infection({'Exposed':1},probabilityOfInfection_fn,[0.3,0.1]),False,0.99)
		self.insert_state('Exposed',5,2,self.scheduled({'Symptomatic':0.3,'Asymptomatic':0.7}),False,0.01)
		self.insert_state('Symptomatic',11,5,self.scheduled({'Recovered':1}),True,0)
		self.insert_state('Asymptomatic',6,3,self.scheduled({'Recovered':1}),True,0)
		self.insert_state('Recovered',100, 0,self.scheduled({'Recovered':1}),False,0)
