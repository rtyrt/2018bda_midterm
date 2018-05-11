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
					if each_filename == "2017_social_utf8.csv":

						# Create the key
						if not total_data.__contains__(get_date(row[11])):
							total_data[get_date(row[11])] = []

						# Append content
						if (row[5] in ["yahoo股市","yahoo奇摩理財","聯合財經網","MoneyDJ理財網"]) or (row[5] == "Ptt" and row[6] in ["STOCK","PC_Shopping"]) or (row[5] == "mobile01" and row[6] in ["手機","筆電","電腦","蘋果"]) or (row[5] == "鉅亨網" and row[6] not in ["海外房產"]):
							# print(row[5])
							# print(row[6])
							total_data[get_date(row[11])].append(row[14])
					else:
						# Create the key
						if not total_data.__contains__(get_date(row[5])):
							total_data[get_date(row[5])] = []

						# Append content
						if (row[3] in ["yahoo股市","yahoo奇摩理財","聯合財經網","MoneyDJ理財網"]) or (row[3] == "Ptt" and row[4] in ["STOCK","PC_Shopping"]) or (row[3] == "mobile01" and row[4] in ["手機","筆電","電腦","蘋果"]) or (row[3] == "鉅亨網" and row[4] not in ["海外房產"]):
							# print(row[3])
							# print(row[4])
							total_data[get_date(row[5])].append(row[11])
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
# temp_data = load_news_data()
# for date in temp_data:
# 	print(date)
# 	print(temp_data[date])

# stock_data = stock.load_stock_data("asus")
# for key in stock_data:
# 	print(key)
# 	print(stock_data[key][1])