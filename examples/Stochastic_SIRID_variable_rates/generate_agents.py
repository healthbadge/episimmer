import random
import copy
import numpy as np

def write_to_file(filename,n):
	header='Agent Index'

	f=open(filename,'w')
	f.write(str(n)+'\n')
	f.write(header+'\n')

	for i in range(n):
		f.write(str(i)+'\n')


write_to_file('agents.txt',1000)
