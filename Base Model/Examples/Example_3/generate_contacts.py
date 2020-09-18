import random
import copy
import numpy as np

def write_to_file(filename,n,no_contacts):
	info_dict={}
	#ID enumerates from 0 to n-1
	header='Agent Index:Interacting Agent Index:Room Ventilation'

	f=open(filename,'w')
	f.write(str(no_contacts)+'\n')
	f.write(header+'\n')

	for i in range(no_contacts):
		agent=random.randint(0,n-1)
		contact_agent=random.randint(0,n-1)
		room_ventilation=random.random()
		f.write(str(agent)+':'+str(contact_agent)+':'+str(room_ventilation)+'\n')


write_to_file('weekday_contacts.txt',300,500)
write_to_file('weekend_contacts.txt',100,200)

