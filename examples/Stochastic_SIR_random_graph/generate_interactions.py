import csv
import random

number_of_agents=100 
p=0.3    

def write_interactions(filename,no_agents,p):

	agent_list=[]
    interacting_agent_list=[]
    for i in range(no_agents-1):
        for j in range(i+1,no_agents):
            if random.random()<p:
                agents_list.append(i)
                agents_list.append(j)
				interacting_agent_list.append(j)
                interacting_agent_list.append(i)
    
write_interactions('interactions.csv',number_of_agents,p)

with open('agents.csv', 'w', newline='') as file:
    fieldnames = ['Agent Index','Interacting Agent Index']
    writer = DictWriter(file, fieldnames=fieldnames)
    writer.writeheader()
    for i in range(100):
        writer.writerow({'Agent index':agent_list[i],'Interacting Agent Index':interacting_agent_list[i])

  
