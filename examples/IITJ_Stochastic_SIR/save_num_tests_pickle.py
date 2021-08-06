import pandas as pd
import pickle

def get_day_num(date_str):
	ls = date_str.split('/')
	# print(ls)
	if int(ls[0])==3:
		return int(ls[1])-1
	elif int(ls[0])==4:
		return int(ls[1])+31-1
	elif int(ls[0])==5:
		return int(ls[1])+61-1
	print("Error!!")
	return -1

def create_dict(df):
	dict ={}
	for index, row in df.iterrows():
		if(row["Date of Testing"] != 'Total'):
			day_num = get_day_num(row["Date of Testing"])
			dict[day_num] = {"num_st_tested":row["Number of Student's Tested"], "num_positive":row["No of Student Positive"]}
	return dict

path = "CRaaS-Simulation-Data.csv"
df = pd.read_csv(path)
dict = create_dict(df)
# print(dict)

with open('tests_dict.pickle', 'wb') as handle:
	pickle.dump(dict, handle, protocol=pickle.HIGHEST_PROTOCOL)
