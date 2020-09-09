import random
import copy
import matplotlib.pyplot as plt
from matplotlib import colors
import numpy as np


class RandomGraph():
	def __init__(self,n,p,make_connected=True):
		self.n=n
		self.p=p
		self.make_connected=make_connected

		self.adj_list=[]
		for i in range(n):
			self.adj_list.append([])

		for i in range(n):
			for j in range(i+1,n):
				r=random.random()
				if r<p:
					self.adj_list[i].append(j)
					self.adj_list[j].append(i)

		if self.make_connected:
			for i in range(n):
				if self.adj_list[i]==[]:
					allowed_values = list(range(0, n))
					allowed_values.remove(i)
					j = random.choice(allowed_values)
					self.adj_list[i].append(j)
					self.adj_list[j].append(i)

		dsum=0
		for i in range(n):
			dsum+=len(self.adj_list[i])
		self.average_degree=2*dsum/n

	def write_to_simple_adjacency_list_file(self):
		#This file type has the following format
		#First line contains the number of vertices (n) labelled as 0 to n-1
		#Every following line contains vertex number followed by neighbours separated by space
		#Example
		#3
		#0 1 2
		#1 0
		#2 0
		filename='simple_adjacency_list_file_G('+str(self.n)+','+str(self.p)+').txt'
		f = open(filename, "w")
		f.write(str(self.n)+'\n')
		for i in range(self.n):
			line=str(i)
			for j in self.adj_list[i]:
				line+=' '+str(j)
			line+='\n'
			f.write(line)

	def write_to_simple_edge_list_file(self):
		#This file type has the following format
		#First line contains the number of vertices (n) labelled as 0 to n-1
		#Every following line represents an directed edge(s->t) and contains two vertices(s t) separated by a space
		#Example
		#3
		#0 1 
		#1 0
		#2 0
		#0 2
		#2 1
		#1 2
		filename='simple_edge_list_file_G('+str(self.n)+','+str(self.p)+').txt'
		f = open(filename, "w")
		f.write(str(self.n)+'\n')
		for i in range(self.n):
			for j in self.adj_list[i]:
				line=str(i)+' '+str(j)+'\n'
				f.write(line)


class StratifiedGraph():
	def __init__(self,n,cum_proportion_list,probability_list,make_connected=True):
		self.n=n
		self.cum_proportion_list=cum_proportion_list  #Eg [0.1,0.3,0.7,1]
		self.probability_list=probability_list		#corressponding eg [0.2,0.1,0.3,0.4]
		self.make_connected=make_connected

		self.adj_list=[]
		for i in range(n):
			self.adj_list.append([])

		for i in range(n):
			r = random.random()
			p=None
			for indx,cum_prob in enumerate(self.cum_proportion_list):
				if r<=cum_prob:
					p=self.probability_list[indx]
			for j in range(i+1,n):
				if random.random()<p:
					self.adj_list[i].append(j)
					self.adj_list[j].append(i)

		if self.make_connected:
			for i in range(n):
				if self.adj_list[i]==[]:
					allowed_values = list(range(0, n))
					allowed_values.remove(i)
					j = random.choice(allowed_values)
					self.adj_list[i].append(j)
					self.adj_list[j].append(i)

		dsum=0
		for i in range(n):
			dsum+=len(self.adj_list[i])
		self.average_degree=2*dsum/n

class FamilyGraph():
	def __init__(self,n,p,family_sizes,make_connected=True):
		#family_sizes is cumulative percentage 
		#30% size 1 families and 70% size 4 => [0.3,0.3,0.3,1]
		self.n=n
		self.p=p
		self.make_connected=make_connected

		self.adj_list=[]
		for i in range(n):
			self.adj_list.append([])

		for i in range(n):
			for j in range(i+1,n):
				if random.random()<p:
					self.adj_list[i].append(j)
					self.adj_list[j].append(i)

		r=random.random()
		f_size=-1
		for fs,p in enumerate(family_sizes):
			if r<p:
				f_size=fs+1
				break
		index_so_far=0
		while index_so_far+f_size<=n:
			family_list=range(index_so_far,index_so_far+f_size)
			index_so_far+=f_size
			self.connect_family(family_list)
		if index_so_far<n-1:
			self.connect_family(range(index_so_far,n))

		if self.make_connected:
			for i in range(n):
				if self.adj_list[i]==[]:
					allowed_values = list(range(0, n))
					allowed_values.remove(i)
					j = random.choice(allowed_values)
					self.adj_list[i].append(j)
					self.adj_list[j].append(i)

		for i in range(n):
			self.adj_list[i]=list(set(self.adj_list[i]))

		dsum=0
		for i in range(n):
			dsum+=len(self.adj_list[i])
		self.average_degree=2*dsum/n

	def connect_family(self,family_list):
		for i in range(len(family_list)-1):
			for j in range(i+1,len(family_list)):
				self.adj_list[family_list[i]].append(family_list[j])
				self.adj_list[family_list[j]].append(family_list[i])
