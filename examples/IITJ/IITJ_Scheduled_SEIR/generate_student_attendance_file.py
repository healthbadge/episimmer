import pandas as pd
import numpy as np
import random
import pickle

def get_student_present_list(prev_students, num_students, cur_student_o_set, cur_student_i_set):
	# print(prev_students, num_students, len(cur_student_o_set), len(cur_student_i_set))
	if prev_students < num_students:
		st_to_add = set(random.sample(cur_student_o_set, num_students - prev_students))
		cur_student_o_set = cur_student_o_set.difference(st_to_add)
		cur_student_i_set = cur_student_i_set.union(st_to_add)

	elif prev_students > num_students:
		st_to_remove = set(random.sample(cur_student_i_set, prev_students - num_students))
		cur_student_i_set = cur_student_i_set.difference(st_to_remove)
		cur_student_o_set = cur_student_o_set.union(st_to_remove)

	else:
		pass

	return cur_student_i_set, cur_student_o_set


def update_hostel_attendance(st_list, bin_student_attendance, day_indx):
	for st in st_list:
		bin_student_attendance[st][day_indx] = 1
	return bin_student_attendance

def validate_table(bin_student_attendance, df_val):

	num_students = df_val.sum(axis=0)
	for day_indx in range(df_val.shape[1]):
		assert num_students[day_indx] == np.sum(bin_student_attendance[:,day_indx])

def update_full_attendance(df_val, df_hostel_name, hostel_student_dict, bin_student_attendance):
	for hostel_indx in range(df_val.shape[0]):

		cur_student_o_set = set(hostel_student_dict[df_hostel_name[hostel_indx]])
		cur_student_i_set = set()
		prev_students = 0

		for day_indx in range(df_val.shape[1]):
			num_students = df_val.iloc[hostel_indx, day_indx]
			cur_student_i_set, cur_student_o_set = get_student_present_list(prev_students, num_students, cur_student_o_set, cur_student_i_set)
			update_hostel_attendance(list(cur_student_i_set), bin_student_attendance, day_indx)
			prev_students = num_students

def main():
	path = "CRaaS-Simulation-Student-Count.csv"
	df = pd.read_csv(path)

	df_hostel_name = df.iloc[:,0]
	df_val = df.iloc[:,1:]
	print("Hostel name table\n", df_hostel_name)
	print("Hostel attendance values\n", df_val)

	# Max column
	max_col = df_val.max(axis=1)
	print("Hostel maximum attendance\n", max_col)

	# Total students = sum(max())
	total_students = max_col.sum()
	print("Total students : ",total_students)

	# Attendance - Binary (No. of students x No. of Days)
	bin_student_attendance = np.zeros([total_students, df_val.shape[1]])

	# Hostel - Students Dict
	hostel_student_dict = {}
	st_id = 0
	for i,name in enumerate(df_hostel_name):
		hostel_student_dict[name] = []
		for j in range(max_col[i]):
			hostel_student_dict[name].append(j+st_id)
		st_id +=  max_col[i]

	update_full_attendance(df_val, df_hostel_name, hostel_student_dict, bin_student_attendance)
	validate_table(bin_student_attendance, df_val)
	# np.savetxt('student_attendance.txt', bin_student_attendance)
	np.save('student_attendance.npy', bin_student_attendance)
	with open('hostel_student_dict.pickle', 'wb') as handle:
		pickle.dump(hostel_student_dict, handle, protocol=pickle.HIGHEST_PROTOCOL)


if __name__ == "__main__":
	random.seed(42)
	main()
