import csv
import random


def write_agents(filename,no_agents):
	with open(filename, 'w', newline='') as file:
	    fieldnames = ['Agent Index']
	    writer = csv.DictWriter(file, fieldnames=fieldnames)

	    writer.writeheader()
	    for i in range(no_agents):
	    	writer.writerow({'Agent Index': i})


def write_interactions(filename,no_agents,p):
	agent_list=[]
	interacting_agent_list=[]
	for i in range(no_agents-1):
		for j in range(i+1,no_agents):
			if random.random()<p:
				agent_list.append(i)
				agent_list.append(j)
				interacting_agent_list.append(j)
				interacting_agent_list.append(i)

	with open(filename, 'w', newline='') as file:
	    fieldnames = ['Agent Index','Interacting Agent Index']
	    writer = csv.DictWriter(file, fieldnames=fieldnames)
	    writer.writeheader()
	    for i in range(len(agent_list)):
	        writer.writerow({'Agent Index':agent_list[i],'Interacting Agent Index':interacting_agent_list[i]})




write_agents('agents.csv',100)
write_interactions('interactions_list.csv', 100, 0.1)
