import Model

def external_prevalence(agent, current_time_step):
	if(agent.info['Compliance'] == 'High'):
		return 0.1
	elif(agent.info['Compliance'] == 'Medium'):
		return 0.2
	elif(agent.info['Compliance'] == 'Low'):
		return 0.35

class UserModel(Model.ScheduledModel):
	def __init__(self):
		Model.ScheduledModel.__init__(self)
		self.insert_state('Susceptible',None, None,self.p_infection([None,None],None,{'Infected':1}),False,0.99)
		self.insert_state('Infected',6,3,self.scheduled({'Recovered':1}),True,0.01)
		self.insert_state('Recovered',0, 0,self.scheduled({'Recovered':1}),False,0)

		self.set_external_prevalence_fn(external_prevalence)
