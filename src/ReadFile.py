import Agent
import Location
import random
import re
import time
from csv import DictReader

class ReadConfiguration():
	def __init__(self,filename):
		self.worlds=None
		self.time_steps=None
		self.starting_exposed_percentage=None
		self.agent_info_keys=None
		self.interaction_info_keys=None

		self.f = open(filename,"r") # can be same for .csv?

		self.worlds=(int)(self.get_value())
		self.time_steps=(int)(self.get_value())

		self.agent_info_keys=self.get_value()
		self.agents_filename=self.get_value()
		self.interaction_info_keys=self.get_value()
		self.interactions_files_list=self.get_value()

		self.location_info_keys=self.get_value()
		self.locations_filename=self.get_value()
		self.event_info_keys=self.get_value()
		self.events_files_list=self.get_value()

		self.f.close()

		if 'Agent Index' not in self.agent_info_keys.split(':'):
			print("Error! Agent file  does not contain parameter \'Agent Index\'")
			return None

		if 'Agent Index' not in self.interaction_info_keys.split(':'):
			print("Interaction definition does not contain parameter \'Agent Index\'")


		if 'Interacting Agent Index' not in self.interaction_info_keys.split(':'):
			print("Interaction definition does not contain parameter \'Interacting Agent Index\'")


		if 'Location Index' not in self.location_info_keys.split(':'):
			print('Location file does not contain parameter \'Location Index\'')


		if 'Location Index' not in self.event_info_keys.split(':'):
			print('Event definition does not contain parameter \'Location Index\'')


		if 'Agents' not in self.event_info_keys.split(':'):
			print('Event definition does not contain parameter \'Agents\'')


	def get_value(self):
		line=self.f.readline()
		l = re.findall("\<.*?\>", line)
		if len(l)!=1:
			print("Error! Invalid entry in config.txt")
			return None
		value=(((l[0])[1:])[:-1])
		return value
# in csv each row is separated by line breaks

class ReadAgents():
	def __init__(self,filename,config_obj):

		f=open(filename,'r')
		if filename.endswith('.txt'):
			self.n=int(self.get_value(f.readline()))
			agent_info_keys=self.get_value(f.readline())
			if agent_info_keys != config_obj.agent_info_keys:
				print("Error! Agent Information parameters donot match the config.txt file")
				return None

			self.parameter_keys=agent_info_keys.split(':')
			self.agents={}

			for i in range(self.n):
				info_dict=self.create_info_dict(self.get_value(f.readline()).split(':'))
				state=None #config_obj.default_state
				agent=Agent.Agent(state,info_dict)
				self.agents[agent.index]=agent
			f.close()

		elif filename.endswith('.csv'):
			with open(filename,'r') as read_obj:
				csv_dict_reader=DictReader(read_obj)
				csv_list=list(csv_dict_reader)
				self.n=len(csv_list)
				

				# Assuming that we have a config file that is .txt file.
				agent_info_keys = ':'.join(csv_dict_reader.fieldnames)
				if agent_info_keys != config_obj.agent_info_keys:
					print("Error! Agent Information parameters donot match the config.txt file")
					return None



				self.parameter_keys=csv_list
				self.agents={}

				for i in range(self.n):
					info_dict=csv_list[i]
					state=None #config_obj.default_state
					agent=Agent.Agent(state,info_dict)
					self.agents[agent.index]=agent
			









		


	def create_info_dict(self,info_list):
		info_dict={}
		for i,key in enumerate(self.parameter_keys):
			info_dict[key]=info_list[i]

		return info_dict

	def get_value(self,line):
		if line.endswith('\n'):
			line=line[:-1]
		return line

class ReadFilesList():
	def __init__(self,filename):
		self.file_list=[]
		f=open(filename,'r')
		lines=f.readlines()
		separator=' '
		text=separator.join(lines)
		l = re.findall("\<.*?\>", text)
		for filename in l:
			self.file_list.append(((filename)[1:])[:-1])
		f.close()

class ReadInteractions():
	def __init__(self,filename,config_obj,agents_obj):
		self.config_obj=config_obj
		self.agents_obj=agents_obj
		if filename=="" or filename==None:
			return
		f=open(filename,'r')
		self.no_interactions=int(self.get_value(f.readline()))
		interaction_info_keys=self.get_value(f.readline())
		if interaction_info_keys != config_obj.interaction_info_keys:
			print("Error! Interaction parameters donot match the config.txt file")
			return None
		self.parameter_keys=interaction_info_keys.split(':')

		for i in range(self.no_interactions):
			parameter_list=(self.get_value(f.readline())).split(':')
			agent_index,info_dict=self.get_interaction(parameter_list)
			agents_obj.agents[agent_index].add_contact(info_dict)

		f.close()

	def get_interaction(self,parameter_list):
		info_dict={}
		agent_index=None
		contact_agent_index=None
		for i,key in enumerate(self.parameter_keys):
			if key=='Agent Index':
				agent_index=parameter_list[i]

			info_dict[key]=parameter_list[i]

		return agent_index,info_dict

	def get_value(self,line):
		if line.endswith('\n'):
			line=line[:-1]
		return line

class ReadLocations():
	def __init__(self,filename,config_obj):
		self.config_obj=config_obj
		self.locations={}
		if filename=="" or filename==None:
			return
		f=open(filename,'r')
		self.no_locations=int(self.get_value(f.readline()))
		location_info_keys=self.get_value(f.readline())
		if location_info_keys != config_obj.location_info_keys:
			print("Error! Location parameters donot match the config.txt file")
			return None
		self.parameter_keys=location_info_keys.split(':')

		for i in range(self.no_locations):
			info_dict=self.create_info_dict(self.get_value(f.readline()).split(':'))
			location=Location.Location(info_dict)
			self.locations[location.index]=location

		f.close()

	def create_info_dict(self,info_list):
		info_dict={}
		for i,key in enumerate(self.parameter_keys):
			info_dict[key]=info_list[i]

		return info_dict

	def get_value(self,line):
		if line.endswith('\n'):
			line=line[:-1]
		return line


class ReadEvents():
	def __init__(self,filename,config_obj,locations_obj):
		self.config_obj=config_obj
		self.locations_obj=locations_obj
		if filename=="" or filename==None:
			return
		f=open(filename,'r')
		self.no_events=int(self.get_value(f.readline()))
		event_info_keys=self.get_value(f.readline())
		if event_info_keys != config_obj.event_info_keys:
			print("Error! Event parameters donot match the config.txt file")
			return None
		self.parameter_keys=event_info_keys.split(':')

		for i in range(self.no_events):
			parameter_list=(self.get_value(f.readline())).split(':')
			location_index,info_dict=self.get_event(parameter_list)
			self.locations_obj.locations[location_index].add_event(info_dict)

		f.close()

	def get_event(self,parameter_list):
		info_dict={}
		location_index=None
		for i,key in enumerate(self.parameter_keys):
			if key=='Location Index':
				location_index=parameter_list[i]

			if key=='Agents':
				info_dict[key]=list(set(parameter_list[i].split(',')))
				if info_dict[key][-1]=='':
					info_dict[key]=info_dict[:-1]
			else:
				info_dict[key]=parameter_list[i]

		if location_index==None:
			print("Error! No event to read")
		return location_index,info_dict

	def get_value(self,line):
		if line.endswith('\n'):
			line=line[:-1]
		return line
