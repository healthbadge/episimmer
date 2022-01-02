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

def write_events(filename,no_locations,no_agents):
	info_dict={}
	#ID enumerates from 0 to n-1
	header='Location Index:Agents'

	f=open(filename,'w')
	f.write(str(1)+'\n')
	f.write(header+'\n')

	line=str(0)+':'
	for i in range(no_agents):
		line+=str(i)
		if i!=no_agents-1:
			line+=','

	f.write(line)

number_of_agents=int(sys.argv[1])
write_agents('agents.txt',number_of_agents)
write_events('one_event.txt',1,number_of_agents)

