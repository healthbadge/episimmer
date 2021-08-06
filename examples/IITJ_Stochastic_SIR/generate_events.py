import pickle
import numpy as np


def write_events(filename,hostel_student_dict):
	header='Location Index:Agents'
	f=open(filename,'w')
	f.write(str(len(hostel_student_dict.keys()))+'\n')
	f.write(header+'\n')
	for i,hostel in enumerate(hostel_student_dict.keys()):
		info_dict={}
		line=str(i)+':'
		for j,agent_indx in enumerate(hostel_student_dict[hostel]):
			line+=str(agent_indx)
			if j!=len(hostel_student_dict[hostel])-1:
				line+=','
		f.write(line+"\n")
	f.close()

fp = open('hostel_student_dict.pickle', 'rb')
hostel_student_dict = pickle.load(fp)
write_events('one_event.txt',hostel_student_dict)
