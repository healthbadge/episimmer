import random
import copy
import numpy as np

def write_to_file(filename,n):
	info_dict={}
	#ID enumerates from 0 to n-1
	header='Location Index:Type:Ventilation:Roomsize:Capacity'

	f=open(filename,'w')
	f.write(str(n)+'\n')
	f.write(header+'\n')

	for i in range(n):
		f.write(str(i))
		f.write(':'+random.choice(['Open Air','Lab','Classroom','Cafeteria','Library']))
		f.write(':'+str(random.random()))
		f.write(':'+str(random.randint(10,20)))
		f.write(':'+str(random.randint(30,40)))
		f.write('\n')


write_to_file('locations.txt',10)
