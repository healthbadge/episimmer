import pandas as pd

def check_roll(df):
	for index, row in df.iterrows():
		try:
			int(row["Roll_Number"])
		except:
			# print(row["Roll_Number"])
			pass

def prune_rows(df):
	ls = ["Project Staff", "CIvil Staff"]
	for x in ls:
		df = df[df.Roll_Number != x]
	return df

def simple_checks(before_df, after_df):
	check_roll(before_df)
	check_roll(after_df)
	assert len(list(before_df["Roll_Number"])) == len(set(before_df["Roll_Number"]))
	assert len(list(after_df["Roll_Number"])) == len(set(after_df["Roll_Number"]))

def get_union_students(before_df, after_df):
	set_before_roll = set(before_df["Roll_Number"])
	set_after_roll = set(after_df["Roll_Number"])
	union_students = set_before_roll.union(set_after_roll)
	return union_students

def write_agents_txt(filename, union_students):

	num_students = len(union_students)
	"""
	Faculty -
	Total Faculty = 55 (Taken from vaccination data.)
	40 on-campus, each has 3 other family members; 15 offcampus
	Total members = 15 + 40*4 = 175

	Staff
	Total Staff = 80 (Taken from vaccination data.)
	20 on-campus, 60 off-campus
	Total members = 80

	Others
	Total sum = 230 (Taken from vaccination data.)
	"""
	num_faculty = 175
	num_staff = 80
	num_others = 230

	header='Agent Index:Type'

	f=open(filename,'w')
	f.write(str(num_students+num_faculty+num_staff+num_others)+'\n')
	f.write(header+'\n')

	for st_roll in union_students:
		f.write(str(st_roll)+':Student\n')

	for i in range(num_faculty):
		f.write(str(i)+'F:Faculty\n')

	for i in range(num_staff):
		f.write(str(i)+'S:Staff\n')

	for i in range(num_others):
		f.write(str(i)+'O:Others\n')

	f.close()


# Read CSVs
before_df = pd.read_csv("iiith_before_lock.csv")
after_df = pd.read_csv("iiith_after_lock.csv")

# Prune rows that do not have identifier for Roll numbers
before_df = prune_rows(before_df)
after_df = prune_rows(after_df)

# Simple checks for valid roll numbers
simple_checks(before_df, after_df)

# Getting union of sets for students before and after lockdown (3 students came from outside after lockdown)
union_students = get_union_students(before_df, after_df)
num_of_students = len(union_students)
# print("Total number of students : ",num_of_students)
write_agents_txt("agents.txt", union_students)
