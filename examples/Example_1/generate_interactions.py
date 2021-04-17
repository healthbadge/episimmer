import csv
import random

def write_interactions(filename,n,no_contacts):
	with open(filename, 'w', newline='') as file:
		fieldnames = ['Agent Index', 'Interacting Agent Index', 'Time Interval', 'Intensity']
		writer = csv.DictWriter(file, fieldnames=fieldnames)
		writer.writeheader()
		for i in range(no_contacts):
			agent=random.randint(0,n-1)
			contact_agent=random.randint(0,n-1)
			time=random.random()*10
			intensity=random.random()
			writer.writerow({'Agent Index':agent, 'Interacting Agent Index':contact_agent, 'Time Interval':time, 'Intensity':intensity})


write_interactions('monday_contacts.csv',100,300)
write_interactions('tuesday_contacts.csv',100,100)
write_interactions('wednesday_contacts.csv',100,500)
write_interactions('thursday_contacts.csv',100,200)
write_interactions('friday_contacts.csv',100,135)
write_interactions('saturday_contacts.csv',100,50)
write_interactions('sunday_contacts.csv',100,70)
