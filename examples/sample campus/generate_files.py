import random
import copy
import numpy as np
from itertools import combinations

def write_to_file():
	info_dict={}
	#ID enumerates from 0 to n-1
	header='Agent Index:Type:Grade'

	f=open('locations.txt','w')
	f.write(str(3)+'\n')
	f.write('Location Index'+'\n')
	for i in range(3):
		f.write(str(i)+'\n')

	f=open('agents.txt','w')
	f.write(str(315)+'\n')
	f.write(header+'\n')

	classes=[]
	for i in range(15):
		classes.append([])

	for i in range(300):
		f.write(str(i))
		grade=int(i/100 )+ 1
		f.write(':Student:Grade '+str(grade))
		class_list=random.choice(list(combinations([5*(grade-1),5*(grade-1)+1,5*(grade-1)+2,5*(grade-1)+3,5*(grade-1)+4],random.choice([1,2,3]))))
		for j in class_list:
			classes[j].append(i)
		f.write('\n')

	for i in range(15):
		f.write(str(i + 300))
		grade=int(i/5 )+ 1
		f.write(':Teacher:Grade '+str(grade))
		classes[i].append(300+i)
		f.write('\n')

	event_header='Location Index:Agents'
	for filename in ['saturday.txt','sunday.txt']:
		f=open(filename,'w')
		f.write(str(0)+'\n')
		f.write(event_header+'\n')
	for index,filename in enumerate(['monday.txt','tuesday.txt','wednesday.txt','thursday.txt','friday.txt']):
		f=open(filename,'w')
		f.write(str(3)+'\n')
		f.write(event_header+'\n')
		for j in range(3):
			line=str(j)+':'
			for agent_index in classes[index+5*j]:
				line+=str(agent_index)+','
			f.write(line[:-1]+'\n')


write_to_file()
