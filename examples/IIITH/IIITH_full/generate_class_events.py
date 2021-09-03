#generate an event for each class
from csv import reader

filename1 = 'Data/classes.csv'
filename2 = 'Data/timetable.csv'

event_files=['Monday.txt','Tuesday.txt','Wednesday.txt','Thursday.txt','Friday.txt','Saturday.txt','Sunday.txt']

#event id -- agents mapping
event_dict={}
#event id -- day mapping
event_occurance={'7':[]}

# read csv file as a list of lists
list_of_rows=None
with open('Data/timetable.csv', 'r') as read_obj:
    # pass the file object to reader() to get the reader object
    csv_reader = reader(read_obj)
    # Pass reader object to list() to get a list of lists
    list_of_rows = list(csv_reader)

for row in list_of_rows:
    agent_id = row[0]
    for class_id in row[1:]:
        try :
            event_dict[class_id].append(agent_id)
        except:
            event_dict[class_id]=[agent_id]


list_of_rows=None
with open('Data/classes.csv', 'r') as read_obj:
    # pass the file object to reader() to get the reader object
    csv_reader = reader(read_obj)
    # Pass reader object to list() to get a list of lists
    list_of_rows = list(csv_reader)

for row in list_of_rows[1:]:
    class_id = row[0]
    days = row[-1].split('-')
    for day in days:
        try :
            event_occurance[day].append(class_id)
        except:
            event_occurance[day]=[class_id]

def write_2_file(day, event_occurance, event_dict):
    filename = event_files[int(day)-1]
    header='Location Index:Event ID:Agents:Type'
    f=open(filename,'w')
    f.write(str(len(event_occurance[day]))+'\n')
    f.write(header+'\n')

    for event_id in event_occurance[day]:
        line = '0:'+event_id+':'
        for agent_id in event_dict[event_id]:
            line+=agent_id+','
        line=line[:-1]
        line+=':Class\n'
        f.write(line)


for day in event_occurance.keys():
    write_2_file(day, event_occurance, event_dict)
