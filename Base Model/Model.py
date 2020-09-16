import random
import Agent
from functools import partial

class StochasticModel():
	def __init__(self,individual_state_types):
		self.individual_state_types=individual_state_types

		self.reset()
		

	def reset(self):
		self.transmission_prob={}
		for t in self.individual_state_types:
			self.transmission_prob[t]={}

		for t1 in self.individual_state_types:
			for t2 in self.individual_state_types:
				self.transmission_prob[t1][t2]=self.p_standard(0)

	def find_next_state(self,agent,agents):
		r=random.random()
		p=0
		for new_state in self.individual_state_types:
			p+=self.transmission_prob[agent.state][new_state](agent,agents)
			if r<p:
				return new_state
				break
		return agent.state

	def p_std_fn(self,p,agent,agents):
		return p

	def p_standard(self,p):
		return partial(self.p_std_fn,p)

	def p_inf_fn(self,fn, p_inf_symp,p_inf_asymp,agent,agents):
			p_not_inf=1
			for c_dict in agent.contact_list:
				contact_index=c_dict['Interacting Agent Index']
				contact_agent=agents[contact_index]
				p_not_inf*=(1-fn(p_inf_symp,p_inf_asymp,contact_agent,c_dict))
				
			return 1 - p_not_inf

	def p_infection(self,p1,p2,fn):  
		return partial(self.p_inf_fn,fn,p1,p2)

	def set_transition(self,s1,s2,fn):
		self.transmission_prob[s1][s2]= fn

	
