#Generate <hostel_mess.txt> from \Data\student.csv
from csv import reader

# read csv file as a list of lists
list_of_rows=None
with open('Data/student.csv', 'r') as read_obj:
    # pass the file object to reader() to get the reader object
    csv_reader = reader(read_obj)
    # Pass reader object to list() to get a list of lists
    list_of_rows = list(csv_reader)

hostel_dict={}
mess_dict={}

for row in list_of_rows[1:]:
    agent_id = row[0]
    hostel_id = row[2]
    mess_id = row[3]

    try :
        hostel_dict[hostel_id].append(agent_id)
    except :
        hostel_dict[hostel_id]=[agent_id]

    try :
        mess_dict[mess_id].append(agent_id)
    except :
        mess_dict[mess_id]=[agent_id]


filename = 'hostel_mess.txt'
header='Location Index:Event ID:Agents:Type'
f=open(filename,'w')
f.write(str(len(hostel_dict.keys())+len(mess_dict.keys())+1)+'\n')
f.write(header+'\n')

for event_id in hostel_dict:
    line = '0:'+event_id+':'
    for agent_id in hostel_dict[event_id]:
        line+=agent_id+','
    line=line[:-1]
    line+=':Hostel\n'
    f.write(line)

for event_id in mess_dict:
    line = '0:'+event_id+':'
    for agent_id in mess_dict[event_id]:
        line+=agent_id+','
    line=line[:-1]
    line+=':Mess\n'
    f.write(line)

line = '0:'+'campus'+':'
for agent_id in range(1241):
    line+=str(agent_id)+','
line=line[:-1]
line+=':Campus\n'
f.write(line)
