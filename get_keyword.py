import re
import string
import collections
import math
import operator
import pickle
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
def get_news_keyword(total_news_dataset, input_firm, total_keyword_num):
	print("length of total_news_dataset: ",len(total_news_dataset))
	rising_news = []
	falling_news = []
	rising_news_keyword = []
	falling_news_keyword = []
	total_keywords = []
	stock_data = stock.load_stock_data(input_firm)
	# print(stock_data)
	for key in stock_data:
		current_date = key
		two_days_ago = compute_date(current_date,2)
		if total_news_dataset.__contains__(two_days_ago) == 1 and len(stock_data[current_date]) == 2:
			if stock_data[current_date][1] == 1:
				rising_news.extend(total_news_dataset[two_days_ago])
				
			elif stock_data[current_date][1] == 0:
				falling_news.extend(total_news_dataset[two_days_ago])
	rising_news_keyword = get_type_news_keyword(rising_news, total_keyword_num, "rising")
	falling_news_keyword = get_type_news_keyword(falling_news, total_keyword_num, "falling")
	total_keywords = list(set(rising_news_keyword + falling_news_keyword))

	print("length of rising_news_keyword: ",len(rising_news_keyword))
	print("length of falling_news_keyword: ",len(falling_news_keyword))
	print("length of total_keywords: ",len(total_keywords))
	filename = "./total_keyword.p"
	fread = open(filename, "wb")
	pickle.dump(total_keywords, fread)
	fread.close()
	return total_keywords

# Given news, find out the keywords for them
# 	input:
# 		news_dataset,a dict with date as key and news array as value
# 		news_dataset["2016-09-01"]=["news01", "news02", "...", ......]
# 	output:
# 		keyword_array, an array with each dataset's keywords
def get_type_news_keyword(news_dataset, total_keyword_num, keyword_type):
	grams_tupples = {}
	grams = {}
	df_tupples = []
	tf_tupples = []
	final_keyword = []

	count = 1
	print(len(news_dataset))
	# for news in news_dataset:
	for news in range(0,len(news_dataset)):
		grams_tupples[news] = []
		temp_tf_tupples = []

		# Get the terms with tf and df
		for n in range(2,5):
			grams = ngrams(news_dataset[news], n)
			check_status = 1
			for tupples in grams:
				for word in tupples:
					if word.isdigit() or isEnglish(word) or word in "[+——！：；，。？「」、~@#￥%……&*（）／]+":
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
			print("Start cleaning: ",count)
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
			print("Finish cleaning")
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
	# print(df_counter.most_common(20))
	# print(tf_counter.most_common(20))

	# Write into xls file
	merge_subterm(df_counter,tf_counter)
	final_keyword = get_final_key_word(df_counter,tf_counter,count-1,total_keyword_num,keyword_type)
	return final_keyword

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
def concat(term):
	concatterm=''
	for i in term:
		concatterm+=i
	return concatterm

def get_final_key_word(df_counter,tf_counter,count,keyword_num, keyword_type):

	total_keyword_array = {}
	final_keyword_array = []
	for terms in df_counter:
		# print(terms)
		# print(tf_counter[terms])
		# print(array_merge(terms))
		total_keyword_array[array_merge(terms)] = (1+math.log10(tf_counter[terms])) * math.log10(count/df_counter[terms])

	for index in range(0,keyword_num):
		temp_max_key_word = ""
		temp_max_key_word = max(total_keyword_array.items(), key=operator.itemgetter(1))[0]
		final_keyword_array.append(temp_max_key_word)
		del total_keyword_array[temp_max_key_word]

	filename = "./"+keyword_type+"_keyword.p"
	fread = open(filename, "wb")
	pickle.dump(final_keyword_array, fread)
	fread.close()

	return final_keyword_array

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

# load news keyword
# 	output:	an array with each dataset's keywords
def load_news_keyword():
	total_data={}
	filename = "./total_keyword.p"
	fileObject = open(filename,'rb')
	total_data = pickle.load(fileObject)
	return total_data

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
