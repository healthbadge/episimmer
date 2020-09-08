import random
import copy
import matplotlib.pyplot as plt
from matplotlib import colors
import numpy as np
import Agent
import Graph
import Simulate

def main(n,p,starting_exposed_percentage,days,graph_obj):
	agents=[]
	for i in range(n):
		state='Susceptible'
		if random.random()<starting_exposed_percentage:
			state='Exposed'
		agent=Agent.Agent(state,i)
		agents.append(agent)

	#create graph of agents from graph_obj
	for indx,agent in enumerate(agents):
		agent.index=indx
		for j in graph_obj.adj_list[indx]:
			agent.neighbours.append(agents[j])

	individual_types=['Susceptible','Exposed','Asymptomatic','Symptomatic','Recovered']

	def p_infection(p1,p2):  # probability of infectiong neighbour
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

	sim_obj=Simulate.Simulate(graph_obj,agents,transmission_prob,individual_types)
	sim_obj.simulate_days(days)
	return sim_obj.state_history

def average(tdict,number):
	for k in tdict.keys():
		l=tdict[k]
		for i in range(len(l)):
			tdict[k][i]/=number

	return tdict

def worlds(number):
	n=1000
	p=0.003
	num_exp=0.01
	days=100
	individual_types=['Susceptible','Exposed','Asymptomatic','Symptomatic','Recovered']
	tdict={}
	for state in individual_types:
		tdict[state]=[0]*(days+1)

	for i in range(number):
		graph_obj = Graph.RandomGraph(n,p,True)
		#graph_obj = Graph.StratifiedGraph(n,[0.1,0.3,0.6,1],[0.02,0.008,0.003,0.002],True)
		sdict= main(n,p,num_exp,days,graph_obj)
		for state in individual_types:
			for j in range(len(tdict[state])):
				tdict[state][j]+=sdict[state][j]

	tdict=average(tdict,number)

	for state in tdict.keys():
		plt.plot(tdict[state])

	plt.title('Averaged SEYAR plot')
	plt.legend(list(tdict.keys()),loc='upper right', shadow=True)
	plt.show()

worlds(10)