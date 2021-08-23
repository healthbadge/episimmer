import pandas as pd

def prune_rows(df):
	ls = ["Project Staff", "CIvil Staff"]
	for x in ls:
		df = df[df.Roll_Number != x]
	return df

def get_subset_df(df, key, value):
	return df[df[key]==value]

def add_agent_events(df):
	event_list = []

	# All Student Event
	event_list.append({"level":"Student_Level", "Agents":list(df["Roll_Number"])})

	# Hostel - Type Events
	hostel_set = set(df["Hostel "])
	for hostel_name in hostel_set:
		df_hostel = get_subset_df(df, "Hostel ", hostel_name)
		# Hostel level events
		event_list.append({"level":"Hostel_Level", "Agents":list(df_hostel["Roll_Number"])})

		floor_set = set(df_hostel["Floor Number"])
		for floor_no in floor_set:
			df_floor = get_subset_df(df_hostel, "Floor Number", floor_no)
			# Floor level events
			event_list.append({"level":"Floor_Level", "Agents":list(df_floor["Roll_Number"])})

			room_set = set(df_floor["Room Number"])
			for room_no in room_set:
				df_room = get_subset_df(df_floor, "Room Number", room_no)
				# Room level events
				event_list.append({"level":"Room_Level", "Agents":list(df_room["Roll_Number"])})

	# Mess - Type Events
	mess_set = set(df["Mess "])
	for mess_name in mess_set:
		df_mess = get_subset_df(df, "Mess ", mess_name)
		# Mess level events
		event_list.append({"level":"Mess_Level", "Agents":list(df_mess["Roll_Number"])})


	return event_list


"""
Faculty -
Total Faculty = 55 (Taken from vaccination data.)
40 on-campus, each has 3 other family members; 15 offcampus
Total members = 15 + 40*4 = 175

Staff
Total Staff = 80 (Taken from vaccination data.)
20 on-campus, 60 off-campus
Total members = 80
"""

def add_faculty_events():
	event_list = []
	num_faculty = 175
	# Flat level
	for i in range(0,160,4):
		ls = []
		for j in range(4):
			ls.append(str(i+j)+"F")
		event_list.append({"level":"Flat_Level", "Agents":ls})

	# Quarter level
	ls1 = []
	for i in range(40):
		ls1.append(str(i)+"F")

	ls2 = []
	for i in range(40,80):
		ls2.append(str(i)+"F")

	event_list.append({"level":"Quarter_Level", "Agents":ls1})
	event_list.append({"level":"Quarter_Level", "Agents":ls2})


	return event_list

def add_staff_events():
	event_list = []
	num_staff = 80
	# Flat level
	for i in range(0,20,4):
		ls = []
		for j in range(4):
			ls.append(str(i+j)+"S")
		event_list.append({"level":"Flat_Level", "Agents":ls})

	# Quarter level
	ls1 = []
	for i in range(20):
		ls1.append(str(i)+"S")
	event_list.append({"level":"Staff_Level", "Agents":ls1})

	return event_list


def add_others_events():
	event_list = []
	num_others = 230

	# Others level
	ls1 = []
	for i in range(num_others):
		ls1.append(str(i)+"O")
	event_list.append({"level":"Others_Level", "Agents":ls1})

	return event_list


def write_events(filename, mode, df):


	event_list = []
	event_list += add_agent_events(df)
	event_list += add_faculty_events()
	event_list += add_staff_events()
	event_list += add_others_events()

	all_agents = []
	for event in event_list:
		for agent in event["Agents"]:
			all_agents.append(agent)
	all_agents = list(set(all_agents))
	event_list.append({"level":"Campus_Level", "Agents":all_agents})

	#ID enumerates from 0 to n-1
	header='Event Index:Location Index:Period:Level:Agents'

	f=open(filename,'w')
	f.write(str(len(event_list))+'\n')
	f.write(header+'\n')
	for i,event in enumerate(event_list):
		agent_str = ""
		for j,agent_roll in enumerate(event["Agents"]):
			if j == len(event["Agents"])-1:
				agent_str += agent_roll
			else:
				agent_str += agent_roll + ","
		f.write(str(i)+":"+str(0)+":"+mode+":"+event["level"]+":"+agent_str+"\n")


	f.close()


# Read CSVs
before_df = pd.read_csv("iiith_before_lock.csv")
after_df = pd.read_csv("iiith_after_lock.csv")

# Prune rows that do not have identifier for Roll numbers
before_df = prune_rows(before_df)
after_df = prune_rows(after_df)

write_events("before_lockdown_events.txt", "Pre-Lockdown", before_df)
write_events("after_lockdown_events.txt", "Post-Lockdown", after_df)
