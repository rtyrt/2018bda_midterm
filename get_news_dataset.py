import re
import pickle
import csv
from datetime import datetime
#————————————————————————Functions——————————————————————————

def get_news_dataset():
	filename = ["2016_forum_utf8.csv", "2016_bbs_utf8.csv", "2016_news_utf8.csv", "2017_social_utf8.csv"]
	total_data = {}
	for each_filename in filename:
		with open(each_filename, 'r') as f:
			f_csv = csv.reader(f)
			for row in f_csv:
				if row[0] != "":

					# Create the key
					if not total_data.__contains__(get_date(row[5])):
						total_data[get_date(row[5])] = []
					
					# Create the key
					if each_filename == "2016_news_utf8.csv":
						if row[4] not in []:
							total_data[get_date(row[5])].append(row[11])
					else:
						total_data[get_date(row[5])].append(row[11])
	print(total_data)
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
	temp_date_time = datetime.strptime(date_time, "%Y-%m-%d %H:%M:%S")
	return datetime.strftime(temp_date_time,"%Y-%m-%d")

#————————————————————————Functions——————————————————————————


#————————————————————————Main Functions——————————————————————————
get_news_dataset()
# stock_data = stock.load_stock_data("asus")
# for key in stock_data:
# 	print(key)
# 	print(stock_data[key][1])