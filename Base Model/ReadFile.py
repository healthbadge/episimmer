import Agent
import random
import re

class ReadConfiguration():
	def __init__(self,filename):
		self.worlds=None
		self.days=None
		self.starting_exposed_percentage=None
		self.agent_info_keys=None
		self.contact_info_keys=None

		self.f = open(filename,"r")

		self.worlds=(int)(self.get_value())
		self.days=(int)(self.get_value())
		self.starting_exposed_percentage=(float)(self.get_value())
		self.agent_info_keys=self.get_value()
		self.contact_info_keys=self.get_value()

		if 'Agent Index' not in self.agent_info_keys.split(':'):
			print("Error! Agent file  does not contain parameter \'Agent Index\'")

		if 'Agent Index' not in self.contact_info_keys.split(':') or 'Interacting Agent Index' not in self.contact_info_keys.split(':'):
			print("Error! Contact/Interaction List does not contain parameter \'Agent Index\' or parameter \'Interacting Agent Index\'")
			return None

		if self.starting_exposed_percentage>1:
			print('Error! Not valid starting percentages')

	def get_value(self):
		line=self.f.readline()
		l = re.findall("\<.*?\>", line)
		if len(l)!=1:
			print("Error! Invalid entry in config.txt")
			return None
		value=(((l[0])[1:])[:-1])
		return value

class ReadAgents():
	def __init__(self,filename,config_obj):
		f=open(filename,'r')
		self.n=int(self.get_value(f.readline()))
		agent_info_keys=self.get_value(f.readline())
		if agent_info_keys != config_obj.agent_info_keys:
			print("Error! Agent Information parameters donot match the config.txt file")
			return None
		self.parameter_keys=agent_info_keys.split(':')
		self.agents={}

		for i in range(self.n):
			info_dict=self.create_info_dict(self.get_value(f.readline()).split(':'))
			state='Susceptible'
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

class ReadInteractionFilesList():
	def __init__(self,filename):
		self.file_list=[]
		f=open(filename,'r')
		lines=f.readlines()
		separator=' '
		text=separator.join(lines)
		l = re.findall("\<.*?\>", text)
		for filename in l:
			self.file_list.append(((filename)[1:])[:-1])


class ReadInteractions():
	def __init__(self,filename,config_obj,agents_obj):
		self.config_obj=config_obj
		self.agents_obj=agents_obj
		f=open(filename,'r')
		self.no_interactions=int(self.get_value(f.readline()))
		contact_info_keys=self.get_value(f.readline())
		if contact_info_keys != config_obj.contact_info_keys:
			print("Error! Contact parameters donot match the config.txt file")
			return None
		self.parameter_keys=contact_info_keys.split(':')

		for i in range(self.no_interactions):
			parameter_list=(self.get_value(f.readline())).split(':')
			agent_index,info_dict=self.get_interaction(parameter_list)
			agents_obj.agents[agent_index].add_contact(info_dict)

	def get_interaction(self,parameter_list):
		info_dict={}
		agent_index=None
		contact_agent_index=None
		for i,key in enumerate(self.parameter_keys):
			if key=='Agent Index':
				agent_index=parameter_list[i]
			else:
				info_dict[key]=parameter_list[i]

		return agent_index,info_dict

	def get_value(self,line):
		if line.endswith('\n'):
			line=line[:-1]
		return line


		





