import random

import numpy as np


def write_to_file(filename,n):
	info_dict={}
	#ID enumerates from 0 to n-1
	header='Location Index'

	f=open(filename,'w')
	f.write(str(n)+'\n')
	f.write(header+'\n')

	for i in range(n):
		f.write(str(i))
		f.write('\n')


write_to_file('locations.txt',10)
