import re
import pickle
import csv

#————————————————————————Functions——————————————————————————

def get_news_dataset():
	filename = ["2016_forum_new.csv", "2016_bbs_new.csv", "2016_news_new.csv", "2017_social_new.csv"]
	total_data = []
	for each_filename in filename:
		with open(each_filename, 'r', encoding='utf-8', newline='' ) as f:
			f_csv = csv.reader(f)
			for row in f_csv:
				temp_array = {}
				if row[11] != "content":
					if each_filename == "2016_news_new.csv":
						if row[4] not in []:
							temp_array["date"] = get_date(row[5])
							temp_array["content"] = row[11]
							total_data.append(temp_array)
					else:
						temp_array["date"] = get_date(row[5])
						temp_array["content"] = row[11]
						total_data.append(temp_array)

	filename = "./total_dataset.p"
	fread = open(filename, "wb")
	pickle.dump(stock, fread)
	fread.close()

# load news dataset
# 	input:	name, the filename of the data
# 	output:	dictionary file of such file
def load_news_data():
	stock={}
	filename = "./total_dataset.p"
	fileObject = open(filename,'rb')
	stock = pickle.load(fileObject)
	return stock

# get date string in following format, 2016-09-01
def get_date(date_time):
	temp_date = date_time.split(" ")[0]
	return add_zero(temp_date.split("/")[0])+"-"+add_zero(temp_date.split("/")[1])+"-"+add_zero(temp_date.split("/")[2])

def add_zero(time):
	if len(time) == 4:
		return str(time)
	elif len(time) == 2:
		return str(time)
	elif len(time) == 1:
		return "0"+str(time)

#————————————————————————Functions——————————————————————————


#————————————————————————Main Functions——————————————————————————
# get_news_dataset()