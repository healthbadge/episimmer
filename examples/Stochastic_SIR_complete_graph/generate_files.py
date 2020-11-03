import random
import copy
import numpy as np
import sys

def write_agents(filename,n):
	header='Agent Index'

	f=open(filename,'w')
	f.write(str(n)+'\n')
	f.write(header+'\n')

	for i in range(n):
		f.write(str(i)+'\n')

def write_interactions(filename,no_agents):
	info_dict={}
	#ID enumerates from 0 to n-1
	no_interactions=no_agents*(no_agents-1)
	header='Agent Index:Interacting Agent Index'

	f=open(filename,'w')
	f.write(str(no_interactions)+'\n')
	f.write(header+'\n')

	for i in range(no_agents):
		for j in range(no_agents):
			if i!=j:
				f.write(str(i)+':'+str(j)+'\n')

number_of_agents=int(sys.argv[1])
write_agents('agents.txt',number_of_agents)
write_interactions('complete_interactions_list.txt',number_of_agents)
