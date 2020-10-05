import random
import copy
import numpy as np

def write_to_file(filename,no_locations,no_agents):
	info_dict={}
	#ID enumerates from 0 to n-1
	header='Location Index:Agents:Time Interval'
	n=random.randint(10,20)
	f=open(filename,'w')
	f.write(str(n)+'\n')
	f.write(header+'\n')

	for i in range(n):
		line=str(random.randint(0,no_locations-1))+':'
		for i in range(random.randint(0,20)):
			line+=str(random.randint(0,no_agents-1))+','
		line+=str(random.randint(0,no_agents-1))
		line+=':'+str(random.choice([10,30,45,60]))+'\n'

		f.write(line)

write_to_file('monday_events.txt',10,100)
write_to_file('tuesday_events.txt',10,100)
write_to_file('wednesday_events.txt',10,100)
write_to_file('thursday_events.txt',10,100)
write_to_file('friday_events.txt',10,100)
write_to_file('saturday_events.txt',15,100)
write_to_file('sunday_events.txt',2,100)
