import random
import copy
import sys
import matplotlib.pyplot as plt
from matplotlib import colors
import numpy as np
import Agent
import Simulate
import math
import ReadFile

class World():
	def __init__(self,config_obj,model,policy_list,event_restriction_fn,agents_filename,interactionFiles_list,locations_filename,eventFiles_list):
		self.config_obj=config_obj
		self.policy_list=policy_list
		self.event_restriction_fn=event_restriction_fn
		self.agents_filename=agents_filename
		self.locations_filename=locations_filename
		self.model=model
		self.interactionFiles_list=interactionFiles_list
		self.eventFiles_list=eventFiles_list

	def one_world(self):

		time_steps = self.config_obj.time_steps

		#Initialize agents
		agents_obj=ReadFile.ReadAgents(self.agents_filename,self.config_obj)

		#Intialize locations
		locations_obj=ReadFile.ReadLocations(self.locations_filename,self.config_obj)

		sim_obj= Simulate.Simulate(self.config_obj,self.model,self.policy_list,self.event_restriction_fn,agents_obj,locations_obj)
		sim_obj.onStartSimulation()

		for i in range(time_steps):
			if self.interactionFiles_list==[] or self.interactionFiles_list==None:
				interactions_filename=None
			else:
				interactions_filename=self.interactionFiles_list[i%len(self.interactionFiles_list)]
			if self.eventFiles_list==[] or self.eventFiles_list==None:
				events_filename=None
			else:
				events_filename=self.eventFiles_list[i%len(self.eventFiles_list)]

			sim_obj.onStartTimeStep(interactions_filename,events_filename,i)
			sim_obj.handleTimeStepForAllAgents()
			sim_obj.endTimeStep()

		end_state=sim_obj.endSimulation()
		return end_state

	#Average number time series
	def average(self,tdict,number):
		for k in tdict.keys():
			l=tdict[k]
			for i in range(len(l)):
				tdict[k][i]/=number

		return tdict

	#Averages multiple simulations and plots a single plot
	def simulate_worlds(self):

		tdict={}
		for state in self.model.individual_state_types:
			tdict[state]=[0]*(self.config_obj.time_steps+1)

		for i in range(self.config_obj.worlds):
			sdict= self.one_world()
			for state in self.model.individual_state_types:
				for j in range(len(tdict[state])):
					tdict[state][j]+=sdict[state][j]

		tdict=self.average(tdict,self.config_obj.worlds)

		for state in tdict.keys():
			plt.plot(tdict[state])

		plt.title(self.model.name+' plot')
		plt.legend(list(tdict.keys()),loc='upper right', shadow=True)
		plt.show()