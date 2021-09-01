import pandas as pd
import pickle

def get_day_num(date_str):
	ls = date_str.split('.')
	# print(ls)
	if int(ls[1])==3:
		return int(ls[0])-27
	elif int(ls[1])==4:
		return int(ls[0])+31-27
	elif int(ls[1])==5:
		return int(ls[0])+31+30-27
	elif int(ls[1])==6:
		return int(ls[0])+31+30+31-27
	print("Error!!")
	return -1

def create_dict(df):
	dict ={}
	for index, row in df.iterrows():
		day_num = get_day_num(row["Date"])
		dict[day_num] = {"Student":row["Student"], "Faculty":row["Faculty"], "Staff":row["Staff"], "Other":row["Other"]}
	return dict

path = "separate_testing.csv"
df = pd.read_csv(path)
dict = create_dict(df)
# print(dict)

with open('tests_dict.pickle', 'wb') as handle:
	pickle.dump(dict, handle, protocol=pickle.HIGHEST_PROTOCOL)
