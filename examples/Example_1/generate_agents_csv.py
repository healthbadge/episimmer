from csv import DictWriter
import random

with open('agents.csv', 'w', newline='') as file:
    fieldnames = ['Agent Index','Type','Residence','HLA Type']
    writer = DictWriter(file, fieldnames=fieldnames)
    writer.writeheader()
    for i in range(100):
        info_dict={}
        info_dict['Agent Index']=i
        info_dict['Type']=random.choice(['Student','Teacher','Administration','Staff','Visitor'])
        info_dict['Residence']=random.choice(['Dorm A','Dorm B','Outside','Teacher Dorm'])
        info_dict['HLA Type']=random.choice(['A','B','C'])
        writer.writerow(info_dict)
