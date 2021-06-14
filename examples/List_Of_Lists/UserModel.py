import Model
import math

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

	#Example 2
	if contact_agent.state=='Symptomatic':
		return math.tanh(float(c_dict['Time Interval'])*float(c_dict['Intensity']))*p_inf_symp
	elif contact_agent.state=='Asymptomatic':
		return math.tanh(float(c_dict['Time Interval'])*float(c_dict['Intensity']))*p_inf_asymp
	else:
		return 0

def event_contribute_fn(agent,event_info,location,current_time_step):
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
		self.set_transition('Susceptible', 'Exposed', self.p_infection([0.3,0.1],probabilityOfInfection_fn))
		self.set_transition('Exposed', 'Symptomatic', self.p_standard(0.15))
		self.set_transition('Exposed', 'Asymptomatic', self.p_standard(0.2))
		self.set_transition('Symptomatic', 'Recovered', self.p_standard(0.2))
		self.set_transition('Asymptomatic', 'Recovered', self.p_standard(0.2))

		self.set_event_contribution_fn(event_contribute_fn)
		self.set_event_recieve_fn(event_recieve_fn)