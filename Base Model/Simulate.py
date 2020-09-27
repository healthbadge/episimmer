import random
import copy
import matplotlib.pyplot as plt
from matplotlib import colors
import numpy as np

class Simulate():
	def __init__(self,agents,transmission_probability,individual_state_types):
		self.agents=agents
		self.transmission_probability=transmission_probability
		self.individual_state_types=individual_state_types
		self.state_list={}
		self.state_history={}

		for state in transmission_probability.keys():
			self.state_list[state]=[]
			self.state_history[state]=[]

		for agent in self.agents:
			self.state_list[agent.state].append(agent.index)

		self.update()

	def simulate_day(self):
		self.spread()
		self.update()

	def simulate_days(self,days):
		for i in range(days):
			self.simulate_day()

	def find_new_state(self,agent):
		agent.next_state=agent.state
		r=random.random()
		p=0
		for new_state in self.individual_state_types:
			p+=self.transmission_probability[agent.state][new_state](agent,agent.neighbours)
			if r<p:
				agent.next_state=new_state
				break

	def spread(self):
		for agent in self.agents:
			agent.new_state=self.find_new_state(agent)

		for agent in self.agents:
			self.convert_state(agent,agent.next_state,1)

	def update(self):
		for state in self.state_history.keys():
			self.state_history[state].append(len(self.state_list[state]))

	def convert_state(self,agent,new_state,p):
		if random.random()<p:
			self.state_list[agent.state].remove(agent.index)
			agent.state=new_state
			self.state_list[agent.state].append(agent.index)
		agent.next_state=None

	def plot(self):
		for state in self.state_history.keys():
			plt.plot(self.state_history[state])

		plt.title('***')
		plt.legend(list(self.state_history.keys()),loc='upper right', shadow=True)
		plt.show()