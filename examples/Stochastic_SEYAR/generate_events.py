import random
import copy
import numpy as np

def write_to_file(filename,no_locations,no_agents):
	info_dict={}
	#ID enumerates from 0 to n-1
	header='Location Index:Agents'

	f=open(filename,'w')
	f.write(str(no_agents)+'\n')
	f.write(header+'\n')

	line=str(0)+':'
	for i in range(no_agents):
		line+=str(i)+','

	f.write(line)

write_to_file('one_event.txt',1,1000)
