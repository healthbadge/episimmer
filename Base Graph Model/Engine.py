import random
import copy
import sys
import matplotlib.pyplot as plt
from matplotlib import colors
import numpy as np
import Agent
import Simulate

def engine(agents,days, transmission_prob,individual_types):

	sim_obj=Simulate.Simulate(agents,transmission_prob,individual_types)
	sim_obj.simulate_days(days)
	return sim_obj.state_history

#Average number time series
def average(tdict,number):
	for k in tdict.keys():
		l=tdict[k]
		for i in range(len(l)):
			tdict[k][i]/=number

	return tdict

#Averages number of simulations and plots a single plot
def worlds(config_obj,graph_obj):
	
	individual_types=['Susceptible','Exposed','Asymptomatic','Symptomatic','Recovered']

	#Probability of infecting a neighbour
	def p_infection(p1,p2):  
		def p_fn(my_agent,neighbour_agents):
			p_inf_symp=p1
			p_inf_asymp=p2
			p_not_inf=1
			for nbr_agent in neighbour_agents:
				if nbr_agent.state=='Symptomatic':
					p_not_inf*=(1-p_inf_symp)
				if nbr_agent.state=='Asymptomatic':
					p_not_inf*=(1-p_inf_asymp)
			return 1 - p_not_inf
		return p_fn


	def p_standard(p):
		def p_fn(my_agent,neighbour_agents):
			return p
		return p_fn

	transmission_prob={}
	for t in individual_types:
		transmission_prob[t]={}

	for t1 in individual_types:
		for t2 in individual_types:
			transmission_prob[t1][t2]=p_standard(0)

	transmission_prob['Susceptible']['Exposed']= p_infection(0.3,0.3)
	transmission_prob['Exposed']['Symptomatic']= p_standard(0.15)
	transmission_prob['Exposed']['Asymptomatic']= p_standard(0.2)
	transmission_prob['Symptomatic']['Recovered']= p_standard(0.2)
	transmission_prob['Asymptomatic']['Recovered']= p_standard(0.2)
	transmission_prob['Recovered']['Susceptible']= p_standard(0)

	tdict={}
	for state in individual_types:
		tdict[state]=[0]*(config_obj.days+1)

	for i in range(config_obj.worlds):
		agents=graph_obj.create_agents(config_obj.starting_exposed_percentage,config_obj.starting_infected_percentage)
		sdict= engine(agents,config_obj.days,transmission_prob,individual_types)
		for state in individual_types:
			for j in range(len(tdict[state])):
				tdict[state][j]+=sdict[state][j]

	tdict=average(tdict,config_obj.worlds)

	for state in tdict.keys():
		plt.plot(tdict[state])

	plt.title('Averaged SEYAR plot')
	plt.legend(list(tdict.keys()),loc='upper right', shadow=True)
	plt.show()