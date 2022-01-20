import random
from csv import DictWriter

with open('agents.csv', 'w', newline='') as file:
    fieldnames = ['Agent Index','Type']
    writer = DictWriter(file, fieldnames=fieldnames)
    writer.writeheader()
    for i in range(100):
        info_dict={}
        info_dict['Agent Index']=i
        info_dict['Type']=random.choice(['Student','Teacher'])
        writer.writerow(info_dict)
