import random
import Agent
import copy
from functools import partial

class StochasticModel():
	def __init__(self,individual_state_types,infected_states,state_proportion):
		self.individual_state_types=individual_state_types
		self.infected_states=infected_states
		self.state_proportion=state_proportion
		self.name='Stochastic Model'

		self.reset()

	def reset(self):
		self.transmission_prob={}
		for t in self.individual_state_types:
			self.transmission_prob[t]={}

		for t1 in self.individual_state_types:
			for t2 in self.individual_state_types:
				self.transmission_prob[t1][t2]=self.p_standard(0)

	def initalize_states(self,agents):
		proportion_sum=0
		for p in self.state_proportion.values():
			proportion_sum+=p
		if proportion_sum!=1:
			print("Error! Starting state proportions don't add up to 1")
			return None

		list_agent_indices= list(agents.keys())
		random.shuffle(list_agent_indices)
		cum_proportion=0
		for state in self.state_proportion.keys():
			proportion=self.state_proportion[state]
			for i in range(int(cum_proportion*len(list_agent_indices)),int((cum_proportion+proportion)*len(list_agent_indices))):
				agent=agents[list_agent_indices[i]]
				agent.state=state
				agent.schedule_time_left=None
			cum_proportion+=proportion


	def find_next_state(self,agent,agents,current_time_step):
		scheduled_time=None
		r=random.random()
		p=0
		for new_state in self.individual_state_types:
			p+=self.transmission_prob[agent.state][new_state](agent,agents,current_time_step)
			if r<p:
				return new_state,scheduled_time
				break
		return agent.state,scheduled_time

	def full_p_standard(self,p,agent,agents,current_time_step):
		return p

	def p_standard(self,p):
		return partial(self.full_p_standard,p)

	def full_p_function(self,fn,agent,agents,current_time_step):
		return fn(current_time_step)

	def p_function(self,fn):
		return partial(self.full_p_function,fn)

	def full_p_infection(self,fn, p_infected_states_list,agent,agents,current_time_step):
			p_not_inf=1
			for c_dict in agent.contact_list:
				contact_index=c_dict['Interacting Agent Index']
				contact_agent=agents[contact_index]
				p_not_inf*=(1-fn(p_infected_states_list,contact_agent,c_dict,current_time_step))
				
			for p in agent.event_probabilities:
				p_not_inf*=(1-p)	
			return 1 - p_not_inf

	def p_infection(self,p_infected_states_list,fn):  
		return partial(self.full_p_infection,fn,p_infected_states_list)

	def set_transition(self,s1,s2,fn):
		self.transmission_prob[s1][s2]= fn

	def set_event_contribution_fn(self,fn):
		self.contribute_fn=fn

	def set_event_recieve_fn(self,fn):
		self.recieve_fn=fn

	def update_event_infection(self,event_info,location,agents_obj,current_time_step,event_restriction_fn):
		ambient_infection=0
		for agent_index in event_info['Agents']:
			agent=agents_obj.agents[agent_index]
			if event_restriction_fn(agent,event_info,current_time_step):
				continue
			ambient_infection+=self.contribute_fn(agent,event_info,location,current_time_step)

		for agent_index in event_info['Agents']:
			agent=agents_obj.agents[agent_index]
			if event_restriction_fn(agent,event_info,current_time_step):
				continue
			p=self.recieve_fn(agent,ambient_infection,event_info,location,current_time_step)
			agent.add_event_result(p)


class ScheduledModel():
	def __init__(self):
		self.individual_state_types=[]
		self.state_transition_fn={}	#One of Scheduled or Dependant
		self.state_mean={}
		self.state_vary={}
		self.infected_states=[]
		self.state_proportion={}
		self.name='Scheduled Model'
	
	def insert_state(self, state, mean, vary, transition_fn,infected_state,proportion):
		if infected_state:
			self.infected_states.append(state)
		self.individual_state_types.append(state)
		self.state_transition_fn[state]=transition_fn
		self.state_mean[state]=mean
		self.state_vary[state]=vary
		self.state_proportion[state]=proportion

	def initalize_states(self,agents):
		proportion_sum=0
		for p in self.state_proportion.values():
			proportion_sum+=p
		if proportion_sum!=1:
			print("Error! Starting state proportions don't add up to 1")
			return None

		list_agent_indices= list(agents.keys())
		random.shuffle(list_agent_indices)
		cum_proportion=0
		for state in self.state_proportion.keys():
			proportion=self.state_proportion[state]
			for i in range(int(cum_proportion*len(list_agent_indices)),int((cum_proportion+proportion)*len(list_agent_indices))):
				agent=agents[list_agent_indices[i]]
				agent.state=state
				agent.schedule_time_left=None
			cum_proportion+=proportion

	def find_scheduled_time(self,state):
		mean=self.state_mean[state]
		vary=self.state_vary[state]
		if mean==None or vary==None:
			scheduled_time=None
		else:
			scheduled_time= random.randint(mean-vary,mean+vary)
		return scheduled_time

	def find_next_state(self,agent,agents,current_time_step):
		if agent.schedule_time_left==None:
			return self.state_transition_fn[agent.state](agent,agents,current_time_step)

		return agent.state,agent.schedule_time_left

	def full_scheduled(self,new_states, agent,agents,current_time_step):
		new_state=self.choose_one_state(new_states)
		scheduled_time=self.find_scheduled_time(new_state)
		return new_state,scheduled_time

	def scheduled(self,new_states):
		return partial(self.full_scheduled,new_states)

	def p_infection(self,p_infected_states_list,fn,new_states):
		return partial(self.full_p_infection,fn,p_infected_states_list,new_states)

	def full_p_infection(self,fn, p_infected_states_list,new_states,agent,agents,current_time_step):
			new_state=self.choose_one_state(new_states)
			p_not_inf=1
			for c_dict in agent.contact_list:
				contact_index=c_dict['Interacting Agent Index']
				contact_agent=agents[contact_index]
				p_not_inf*=(1-fn(p_infected_states_list,contact_agent,c_dict,current_time_step))
				
			for p in agent.event_probabilities:
				p_not_inf*=(1-p)

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

	def set_event_contribution_fn(self,fn):
		self.contribute_fn=fn

	def set_event_recieve_fn(self,fn):
		self.recieve_fn=fn

	def update_event_infection(self,event_info,location,agents_obj,current_time_step,event_restriction_fn):
		ambient_infection=0
		for agent_index in event_info['Agents']:
			agent=agents_obj.agents[agent_index]
			if event_restriction_fn(agent,event_info,current_time_step):
				continue
			ambient_infection+=self.contribute_fn(agent,event_info,location,current_time_step)

		for agent_index in event_info['Agents']:
			agent=agents_obj.agents[agent_index]
			if event_restriction_fn(agent,event_info,current_time_step):
				continue
			p=self.recieve_fn(agent,ambient_infection,event_info,location,current_time_step)
			agent.add_event_result(p)



	
