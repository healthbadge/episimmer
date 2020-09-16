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
	def __init__(self,config_obj,agents_filename,model,interactionFiles_list):
		self.config_obj=config_obj
		self.agents_filename=agents_filename
		self.model=model
		self.interactionFiles_list=interactionFiles_list

	def one_world(self):

		days = self.config_obj.days

		sim_obj= Simulate.Simulate(self.config_obj,self.agents_filename,self.model)
		sim_obj.onStartSimulation()

		for i in range(days):
			interactions_filename=self.interactionFiles_list[days%len(self.interactionFiles_list)]

			sim_obj.onStartDay(interactions_filename)
			sim_obj.handleDayForAllAgents()
			sim_obj.endDay()

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
			tdict[state]=[0]*(self.config_obj.days+1)

		for i in range(self.config_obj.worlds):
			sdict= self.one_world()
			for state in self.model.individual_state_types:
				for j in range(len(tdict[state])):
					tdict[state][j]+=sdict[state][j]

		tdict=self.average(tdict,self.config_obj.worlds)

		for state in tdict.keys():
			plt.plot(tdict[state])

		plt.title('Averaged SEYAR plot')
		plt.legend(list(tdict.keys()),loc='upper right', shadow=True)
		plt.show()