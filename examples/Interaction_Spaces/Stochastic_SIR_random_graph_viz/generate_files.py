# This code require two inputs, 'number of agents' and 'probability of edge'
# To run <python generate_files.py 100 0.1>

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

def write_interactions(filename,no_agents,p):
	info_dict={}
	#Agent ID enumerates from 0 to n-1
	header='Agent Index:Interacting Agent Index'
	lines=[]
	for i in range(no_agents-1):
		for j in range(i+1,no_agents):
			if random.random()<p:
				lines.append(str(i)+':'+str(j)+'\n')
				lines.append(str(j)+':'+str(i)+'\n')

	f=open(filename,'w')
	f.write(str(len(lines))+'\n')
	f.write(header+'\n')

	for line in lines:
		f.write(line)

number_of_agents=int(sys.argv[1])
p=float(sys.argv[2])
write_agents('agents.txt',number_of_agents)
write_interactions('interactions_list.txt',number_of_agents,p)
