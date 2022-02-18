import random

import numpy as np


def write_to_file(filename,n):
	info_dict={}
	#ID enumerates from 0 to n-1
	header='Agent Index:Type'
	info_dict['Type']=['Student','Teacher']

	f=open(filename,'w')
	f.write(str(n)+'\n')
	f.write(header+'\n')

	for i in range(n):
		f.write(str(i))
		for j in info_dict.keys():
			f.write(':'+random.choice(info_dict[j]))
		f.write('\n')


write_to_file('agents.txt',100)
