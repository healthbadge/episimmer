import random
import copy
import numpy as np

def write_to_file(filename,n,no_contacts):
	info_dict={}
	#ID enumerates from 0 to n-1
	header='Agent Index:Interacting Agent Index:Time Interval:Intensity'

	f=open(filename,'w')
	f.write(str(no_contacts)+'\n')
	f.write(header+'\n')

	for i in range(no_contacts):
		agent=random.randint(0,n-1)
		contact_agent=random.randint(0,n-1)
		time=random.random()*10
		intensity=random.random()
		f.write(str(agent)+':'+str(contact_agent)+':'+str(time)+':'+str(intensity)+'\n')


write_to_file('monday_contacts.txt',100,300)
write_to_file('tuesday_contacts.txt',100,100)
write_to_file('wednesday_contacts.txt',100,500)
write_to_file('thursday_contacts.txt',100,200)
write_to_file('friday_contacts.txt',100,135)
write_to_file('saturday_contacts.txt',100,50)
write_to_file('sunday_contacts.txt',100,70)

