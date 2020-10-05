import random
import copy
import numpy as np

def write_to_file(filename,n):
	info_dict={}
	#ID enumerates from 0 to n-1
	header='Agent Index:Type:Susceptibility'
	info_dict['Type']=['Office Staff','Developer','Designer']
	info_dict['Susceptibility']=['0.7','0.5','1']

	f=open(filename,'w')
	f.write(str(n)+'\n')
	f.write(header+'\n')

	for i in range(n):
		f.write(str(i))
		for j in info_dict.keys():
			f.write(':'+info_dict[j][int(i/100)])
		f.write('\n')


write_to_file('agents.txt',300)
