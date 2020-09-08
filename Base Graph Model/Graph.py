import random
import copy
import matplotlib.pyplot as plt
from matplotlib import colors
import numpy as np


class RandomGraph():
	def __init__(self,n,p,connected=True):
		self.n=n
		self.p=p
		self.connected=connected

		self.adj_list=[]
		for i in range(n):
			self.adj_list.append([])

		for i in range(n):
			for j in range(i+1,n):
				if random.random()<p:
					self.adj_list[i].append(j)
					self.adj_list[j].append(i)

		if self.connected:
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

class StratifiedGraph():
	def __init__(self,n,cum_proportion_list,probability_list,connected=True):
		self.n=n
		self.cum_proportion_list=cum_proportion_list  #Eg [0.1,0.3,0.7,1]
		self.probability_list=probability_list		#corressponding eg [0.2,0.1,0.3,0.4]
		self.connected=connected

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

		if self.connected:
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