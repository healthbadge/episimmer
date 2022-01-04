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

def write_events(filename,start_agent_index, end_agent_index):
	info_dict={}
	#ID enumerates from 0 to n-1
	header='Location Index:Agents'
	no_agents=end_agent_index-start_agent_index

	f=open(filename,'w')
	f.write(str(1)+'\n')
	f.write(header+'\n')

	line=str(0)+':'
	for i in range(start_agent_index,end_agent_index):
		line+=str(i)
		if i!=end_agent_index-1:
			line+=','

	f.write(line)

number_of_agents=int(sys.argv[1])
write_agents('agents.txt',number_of_agents)
write_events('first_event.txt',0,int(number_of_agents/2))
write_events('second_event.txt',int(number_of_agents/2),number_of_agents)

