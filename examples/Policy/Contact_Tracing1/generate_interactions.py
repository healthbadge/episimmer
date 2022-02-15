import random
import sys

import numpy as np


def write_to_file(filename,n,no_contacts):
	#ID enumerates from 0 to n-1
	header='Agent Index:Interacting Agent Index'

	f=open(filename,'w')
	f.write(str(no_contacts)+'\n')
	f.write(header+'\n')

	for i in range(no_contacts):
		agent=random.randint(0,n-1)
		contact_agent=random.randint(0,n-1)
		f.write(str(agent)+':'+str(contact_agent)+'\n')


n = int(sys.argv[1])
num_interactions = int(sys.argv[2])
write_to_file('simple_interactions.txt',n,num_interactions)
