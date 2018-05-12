import re
import string
import collections
import math
from nltk import ngrams
from datetime import datetime, timedelta
import stock as stock

# ---------------- Functions ----------------

# Given news, find out the keywords for them
# 	input:
# 		news_dataset,a dict with date as key and news array as value
# 		news_dataset["2016-09-01"]=["news01", "news02", "...", ......]
# 	output:
# 		keyword_array, an array with each dataset's keywords
def get_news_keyword(total_news_dataset, input_firm):
	rising_news = []
	falling_news = []
	rising_news_keyword = []
	falling_news_keyword = []
	total_keywords = []
	stock_data = stock.load_stock_data(input_firm)
	for key in stock_data:
		current_date = get_date(key)
		# current_date = key
		two_days_ago = compute_date(current_date,2)
		print(stock_data[key])
		if total_news_dataset.__contains__(two_days_ago) == 1:
			if stock_data[key][1] == 1:
				rising_news.extend(total_news_dataset[two_days_ago])
				
			elif stock_data[key][1] == 0:
				falling_news.extend(total_news_dataset[two_days_ago])
	rising_news_keyword = get_type_news_keyword(rising_news)
	falling_news_keyword = get_type_news_keyword(falling_news)
	total_keywords = list(set(rising_news_keyword + falling_news_keyword))

	print("length of rising_news_keyword: ",len(rising_news_keyword))
	print("length of falling_news_keyword: ",len(falling_news_keyword))
	print("length of total_keywords: ",len(total_keywords))
	return total_keywords

# Given news, find out the keywords for them
# 	input:
# 		news_dataset,a dict with date as key and news array as value
# 		news_dataset["2016-09-01"]=["news01", "news02", "...", ......]
# 	output:
# 		keyword_array, an array with each dataset's keywords
def get_type_news_keyword(news_dataset):
	pass


def get_ngram_tupples(content):
	grams_tupples = {}
	grams = {}
	df_tupples = []
	tf_tupples = []

	count = 1
	print(len(content))
	for news in content:
		print(news)
		grams_tupples[news] = []
		temp_tf_tupples = []

		# Get the terms with tf and df
		for n in range(2,7):
			grams = ngrams(content[news]["content"], n)
			check_status = 1
			for tupples in grams:
				for word in tupples:
					if word.isdigit() or isEnglish(word) or word in "[+——！：；，。？「」、~@#￥%……&*（）]+":
						check_status = 0
				if(check_status):
					grams_tupples[news].append(tupples)
					temp_tf_tupples.append(tupples)
					df_tupples.append(tupples)
				check_status = 1
		
		# df means to collect the set of each terms in one news
		for tmp_tupples in set(temp_tf_tupples):
			tf_tupples.append(tmp_tupples)

		# Select terms every 5000 news
		if count%5000 == 0:
			temp_df_counter = collections.Counter(df_tupples)
			temp_tf_counter = collections.Counter(tf_tupples)
			print("temp_df_counter"+str(len(temp_df_counter)))
			print("temp_tf_counter"+str(len(temp_tf_counter)))
			temp_df_tupples_cleaner = []
			temp_tf_tupples_cleaner = []
			for collect in temp_tf_counter.most_common(1000):
				temp_df_tupples_cleaner += [collect[0] for i in range(0,temp_df_counter[collect[0]])]
				temp_tf_tupples_cleaner += [collect[0] for i in range(0,collect[1])]
			df_tupples = temp_df_tupples_cleaner
			tf_tupples = temp_tf_tupples_cleaner
			# for collect in temp_df_counter.most_common()[:-5001:-1]:
			# 	df_tupples = [tupple for tupple in df_tupples if not collect[0]]
			# 	tf_tupples = [tupple for tupple in tf_tupples if not collect[0]]
		
		# Count for times it runs
		count += 1
		# if count == 50: 
		# 	break

	# Select terms at the end, same thing as above "Select terms every 5000 news", better to make it into a function
	temp_df_counter = collections.Counter(df_tupples)
	temp_tf_counter = collections.Counter(tf_tupples)
	print("temp_df_counter"+str(len(temp_df_counter)))
	print("temp_tf_counter"+str(len(temp_tf_counter)))
	temp_df_tupples_cleaner = []
	temp_tf_tupples_cleaner = []
	for collect in temp_tf_counter.most_common(1000):
		temp_df_tupples_cleaner += [collect[0] for i in range(0,temp_df_counter[collect[0]])]
		temp_tf_tupples_cleaner += [collect[0] for i in range(0,collect[1])]
	df_tupples = temp_df_tupples_cleaner
	tf_tupples = temp_tf_tupples_cleaner

	# Print out the most common terms
	df_counter = collections.Counter(df_tupples)
	tf_counter = collections.Counter(tf_tupples)
	print(df_counter.most_common(20))
	print(tf_counter.most_common(20))

	# Write into xls file
	merge_subterm(df_counter,tf_counter)
	write_into_xls(df_counter,tf_counter,count-1)

def concat(term):
	concatterm=''
	for i in term:
		concatterm+=i
	return concatterm

def merge_subterm(df_counter,tf_counter):
	ngram_term=[[],[],[],[],[]]
	for term in df_counter:
		ngram_term[len(term)-2].append(term)

	for i in range(4):
		for subterm in ngram_term[i]:
			ckeck = False
			st = concat(subterm)
			for term in ngram_term[i+1]:
				t = concat(term)
				if st in t:
					#print(df_counter[subterm]/df_counter[term])
					if df_counter[subterm]/df_counter[term]<1.05 :
						ckeck = True
						break
			if ckeck:
				df_counter.pop(subterm)
				tf_counter.pop(subterm)


def write_into_xls(df_counter,tf_counter,count):

	wb = Workbook()
	new_ws = wb.create_sheet(title='bank')
	new_ws.cell(row=1, column=1).value = count
	new_ws.cell(row=1, column=2).value = "doc_num"
	new_ws.cell(row=2, column=1).value = "term"
	new_ws.cell(row=2, column=2).value = "tf"
	new_ws.cell(row=2, column=3).value = "df"
	new_ws.cell(row=2, column=4).value = "tf-idf"

	row = 3
	for terms in df_counter:
		# print(terms)
		# print(tf_counter[terms])
		# print(array_merge(terms))
		new_ws.cell(row=row, column=1).value = array_merge(terms)
		new_ws.cell(row=row, column=2).value = tf_counter[terms]
		new_ws.cell(row=row, column=3).value = df_counter[terms]
		new_ws.cell(row=row, column=4).value = (1+math.log10(tf_counter[terms])) * math.log10(count/df_counter[terms])

		row += 1
	wb.save(filename='bda_hw01_group.xlsx')

def isEnglish(s):
    try:
        s.encode(encoding='utf-8').decode('ascii')
    except UnicodeDecodeError:
        return False
    else:
        return True

def array_merge(terms):
	result = ""
	for text in terms:
		result += text
	return result

# get date string in following format, 2016-09-01
def get_date(date_time):
	return datetime.strftime(date_time,"%Y-%m-%d")

# compute date n days ago
def compute_date(date,n):
	temp_date_time = datetime.strptime(date, "%Y-%m-%d")
	temp_date_time = temp_date_time - timedelta(days = n)
	return datetime.strftime(temp_date_time,"%Y-%m-%d")

#--------------------------------------------


# --------------- Main code ---------------
# print("Get ngram tupples")
# get_ngram_tupples(content)


# -----------------------------------------
