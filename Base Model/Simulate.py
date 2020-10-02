import random
import copy
import numpy as np
import ReadFile

class Simulate():
	def __init__(self,config_obj,model,agents_filename,locations_filename):
		self.agents_filename=agents_filename
		self.locations_filename=locations_filename
		self.model=model
		self.config_obj=config_obj

	def onStartSimulation(self):
		#Initialize agents
		self.agents_obj=ReadFile.ReadAgents(self.agents_filename,self.config_obj)

		#Intialize locations
		self.locations_obj=ReadFile.ReadLocations(self.locations_filename,self.config_obj)

		#Intitialize state list
		self.state_list={}
		self.state_history={}
		for state in self.model.individual_state_types:
			self.state_list[state]=[]
			self.state_history[state]=[]

		#Starting Prevalence as described by config.txt
		for agent in self.agents_obj.agents.values():
			r=random.random()
			if r<self.config_obj.starting_variable_state_percentage:
				agent.state=self.config_obj.initial_variable_state
				agent.scheduled_time_left=None

		#Update State list
		for agent in self.agents_obj.agents.values():
			self.state_list[agent.state].append(agent.index)

		#Store state list
		self.store_state()

	def onStartDay(self,interactions_filename,events_filename):
		for agent in self.agents_obj.agents.values():
			agent.new_day()

		for location in self.locations_obj.locations.values():
			location.new_day()

		#Add Interactions to agents
		if interactions_filename!=None:
			ReadFile.ReadInteractions(interactions_filename,self.config_obj,self.agents_obj)
		
		#Add events to locations
		if events_filename!=None:
			ReadFile.ReadEvents(events_filename,self.config_obj,self.locations_obj)

			#Update event info to agents from location
			for location in self.locations_obj.locations.values():
				for event_info in location.events:
					self.model.update_event_infection(event_info,location,self.agents_obj)


	def handleDayForAllAgents(self):
		#Too ensure concurrency we update agent.next_state in method handleDayAsAgent
		#After every agent has updated next_state we update states of all agents in method handleDay() 

		for agent in self.agents_obj.agents.values():
			self.handleDayAsAgent(agent)

		for agent in self.agents_obj.agents.values():
			self.convert_state(agent)

	def handleDayAsAgent(self,agent):
		#Too ensure concurrency we update agent.next_state in method handleDayAsAgent
		#After every agent has updated next_state we update states of all agents in method handleDay()


		#Finding next_state
		agent.set_next_state(self.model.find_next_state(agent,self.agents_obj.agents)) 

	def endDay(self):
		self.store_state()

	def endSimulation(self):
		return self.state_history

	def store_state(self):
		for state in self.state_history.keys():
			self.state_history[state].append(len(self.state_list[state]))

	def convert_state(self,agent):
		self.state_list[agent.state].remove(agent.index)
		agent.update_state()
		self.state_list[agent.state].append(agent.index)
