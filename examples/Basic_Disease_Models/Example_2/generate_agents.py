import random
import copy
import numpy as np

def write_to_file(filename,n):
	info_dict={}
	#ID enumerates from 0 to n-1
	header='Agent Index:Type:Residence:HLA Type'
	info_dict['Type']=['Student','Teacher','Administration','Staff','Visitor']
	info_dict['Residence']=['Dorm A','Dorm B','Outside','Teacher Dorm']
	info_dict['HLA Type']=['A','B','C']

	f=open(filename,'w')
	f.write(str(n)+'\n')
	f.write(header+'\n')

	for i in range(n):
		f.write(str(i))
		for j in info_dict.keys():
			f.write(':'+random.choice(info_dict[j]))
		f.write('\n')


write_to_file('agents.txt',100)
