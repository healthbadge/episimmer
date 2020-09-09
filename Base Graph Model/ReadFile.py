import Agent
import random

class ReadConfiguration():
	def __init__(self,filename):
		self.worlds=None
		self.days=None
		self.starting_exposed_percentage=None
		self.starting_infected_percentage=None

		f = open(filename,"r")
		line=f.readline()
		self.worlds=(int)(self.get_value(line))
		line=f.readline()
		self.days=(int)(self.get_value(line))
		line=f.readline()
		self.starting_exposed_percentage=(float)(self.get_value(line))
		line=f.readline()
		self.starting_infected_percentage=(float)(self.get_value(line))

		if self.starting_infected_percentage+self.starting_exposed_percentage>1:
			print('Error! Not valid starting percentages')



	def get_value(self,line):
		value=line.split(':')[-1]
		if value.endswith('\n'):
			value=value[:-1]
		return value


class ReadSimpleGraph():
	def __init__(self,file_type,filename):
		self.file_type=file_type
		self.filename=filename
		self.n=None
		self.adj_list=[]

		if self.file_type=='Simple Adjacency List':
			self.read_adjacent_list_file()
		elif self.file_type=='Simple Edge List':
			self.read_edge_list_file()
		else:
			print('Error! Not a valid filetype')
			return None

	def read_adjacent_list_file(self):
		f = open(self.filename, "r")
		firstline=f.readline()
		self.n=(int)(firstline[:-1])
		for i in range(self.n):
			self.adj_list.append([])
		for line in f:
			if line.endswith('/n'):
				line=line[:-1]
			line_list=line.split(' ')
			node=int(line_list[0])

			for elem in line_list[1:]:
				self.adj_list[node].append(int(elem))

	def read_edge_list_file(self):
		f = open(self.filename, "r")
		firstline=f.readline()
		self.n=(int)(firstline[:-1])
		for i in range(self.n):
			self.adj_list.append([])
		for line in f:
			if line.endswith('/n'):
				line=line[:-1]
			line_list=line.split(' ')
			self.adj_list[int(line_list[0])].append(int(line_list[1]))

	def create_agents(self,starting_exposed_percentage,starting_infected_percentage):
		agents=[]
		#Intialize a percentage of agents as Exposed, Infected
		for i in range(self.n):
			state='Susceptible'
			r=random.random()
			if r<starting_exposed_percentage:
				state='Exposed'
			elif r<starting_exposed_percentage+starting_infected_percentage:
				state='Infected'
			agent=Agent.Agent(state,i)
			agents.append(agent)

		#Create a graph of agents from adj_list
		for indx,agent in enumerate(agents):
			agent.index=indx
			for j in self.adj_list[indx]:
				agent.neighbours.append(agents[j])

		return agents
		





