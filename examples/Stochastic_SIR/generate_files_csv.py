from csv import DictWriter
with open('agents.csv', 'w', newline='') as file:
    fieldnames = ['Agent Index']
    writer = DictWriter(file, fieldnames=fieldnames)

    writer.writeheader()
    for i in range(1000):
    	writer.writerow({'Agent Index': i})
  
