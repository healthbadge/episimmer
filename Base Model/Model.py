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
		scheduled_time=None
		r=random.random()
		p=0
		for new_state in self.individual_state_types:
			p+=self.transmission_prob[agent.state][new_state](agent,agents)
			if r<p:
				return new_state,scheduled_time
				break
		return agent.state,scheduled_time

	def full_p_standard(self,p,agent,agents):
		return p

	def p_standard(self,p):
		return partial(self.full_p_standard,p)

	def full_p_infection(self,fn, p_inf_symp,p_inf_asymp,agent,agents):
			p_not_inf=1
			for c_dict in agent.contact_list:
				contact_index=c_dict['Interacting Agent Index']
				contact_agent=agents[contact_index]
				p_not_inf*=(1-fn(p_inf_symp,p_inf_asymp,contact_agent,c_dict))
				
			return 1 - p_not_inf

	def p_infection(self,p1,p2,fn):  
		return partial(self.full_p_infection,fn,p1,p2)

	def set_transition(self,s1,s2,fn):
		self.transmission_prob[s1][s2]= fn

class ScheduledModel():
	def __init__(self):
		self.individual_state_types=[]
		self.state_transition_fn={}	#One of Scheduled or Dependant
		self.state_mean={}
		self.state_vary={}
	
	def insert_state(self, state, mean, vary, transition_fn):
		self.individual_state_types.append(state)
		self.state_transition_fn[state]=transition_fn
		self.state_mean[state]=mean
		self.state_vary[state]=vary

	def find_scheduled_time(self,state):
		mean=self.state_mean[state]
		vary=self.state_vary[state]
		if mean==None or vary==None:
			scheduled_time=None
		else:
			scheduled_time= random.randint(mean-vary,mean+vary)
		return scheduled_time

	def find_next_state(self,agent,agents):
		if agent.schedule_time_left==None:
			return self.state_transition_fn[agent.state](agent,agents)

		return agent.state,agent.schedule_time_left

	def full_scheduled(self,new_states, agent,agents):
		new_state=self.choose_one_state(new_states)
		scheduled_time=self.find_scheduled_time(new_state)
		return new_state,scheduled_time

	def scheduled(self,new_states):
		return partial(self.full_scheduled,new_states)

	def p_infection(self,p1,p2,fn,new_states):
		return partial(self.full_p_infection,fn,p1,p2,new_states)

	def full_p_infection(self,fn, p_inf_symp,p_inf_asymp,new_states,agent,agents):
			new_state=self.choose_one_state(new_states)
			p_not_inf=1
			for c_dict in agent.contact_list:
				contact_index=c_dict['Interacting Agent Index']
				contact_agent=agents[contact_index]
				p_not_inf*=(1-fn(p_inf_symp,p_inf_asymp,contact_agent,c_dict))
				
			r=random.random()
			if r>=1 - p_not_inf:
				new_state = agent.state

			scheduled_time=self.find_scheduled_time(new_state)
			return new_state,scheduled_time


	def choose_one_state(self,state_dict):
		new_state=None
		p=0
		r=random.random()
		for state in state_dict.keys():
			p+=state_dict[state]
			if r<p:
				new_state=state 
				break
		
		if new_state==None:
			print('Error! State probabilities do not add to 1')
		return new_state



	
