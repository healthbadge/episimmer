from csv import DictWriter
with open('interactions.csv', 'w', newline='') as file:
    fieldnames = ['Agent Index','Interacting Agent']
    writer = DictWriter(file, fieldnames=fieldnames)

    writer.writeheader()
    for i in range(1000):
    	if i!=10:
    		writer.writerow({'Agent Index': i,'Interacting Agent':i+1})
  
