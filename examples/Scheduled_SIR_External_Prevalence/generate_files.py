import random
import copy
import numpy as np
import sys

def write_agents(filename,n):
	info_dict={}
	#ID enumerates from 0 to n-1
	header='Agent Index:Compliance'
	info_dict['Compliance']=['High','Low','Medium']

	f=open(filename,'w')
	f.write(str(n)+'\n')
	f.write(header+'\n')

	for i in range(n):
		f.write(str(i))
		for j in info_dict.keys():
			f.write(':'+random.choice(info_dict[j]))
		f.write('\n')

number_of_agents=int(sys.argv[1])
write_agents('agents.txt',number_of_agents)
