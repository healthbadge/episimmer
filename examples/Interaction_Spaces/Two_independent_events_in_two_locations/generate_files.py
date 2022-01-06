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

	f=open(filename,'w')
	f.write(str(2)+'\n')
	f.write(header+'\n')

	line=str(0)+':'	#location index 0
	for i in range(start_agent_index,int(end_agent_index/2)):
		line+=str(i)
		if i!=int(end_agent_index/2)-1:
			line+=','
	f.write(line+'\n')
	line=str(1)+':'	#location index 1
	for i in range(int(end_agent_index/2),end_agent_index):
		line+=str(i)
		if i!=end_agent_index-1:
			line+=','

	f.write(line)

number_of_agents=int(sys.argv[1])
write_agents('agents.txt',number_of_agents)
write_events('two_events.txt',0,number_of_agents)

