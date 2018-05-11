import re
import pickle
import csv

#————————————————————————Functions——————————————————————————

def get_news_dataset():
	filename = ["2016_forum.csv", "2016_bbs.csv", "2016_news.csv", "2017_social.csv"]
	total_data = {}
	for each_filename in filename:
		with open(each_filename, 'r') as f:
			f_csv = csv.reader(f)
			for row in f_csv:
				if row[11] != "content":
					if each_filename == "2016_news.csv":
						if row[4] not in []:
							total_data[get_date(row[5])].append(row[11])
					else:
						total_data[get_date(row[5])].append(row[11])

				# print(row)
	filename = "./total_dataset.p"
	fread = open(filename, "wb")
	pickle.dump(total_data, fread)
	fread.close()

# load news dataset
# 	output:	dictionary file of such file
# 		total_data["2016-09-09"]=["first news","second news","third news",....]
def load_news_data():
	total_data={}
	filename = "./total_dataset.p"
	fileObject = open(filename,'rb')
	total_data = pickle.load(fileObject)
	return total_data

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
get_news_dataset()