import pickle
import re
import string
import collections
import math
import operator
import pickle
from nltk import ngrams
from datetime import datetime, timedelta


filename='asus_related_news.p'
file=open(filename,'rb')
asus_news=pickle.load(file)

asus_news=one_array_list(asus_news)
get_type_news_keyword(asus_news,166,'asus')

#-----------------------Functions--------------------------------------------

#input : [data]:['news1','news2','news3']
#output : ['news1','news2','news3']
def one_array_list(data):
    data_list=[]
    for key in data:
        for i in range(len(data[key])):
            data_list.append(data[key][i])
            
    return data_list

# THE FOLLOWING CODE IS COPIED FROM GET_KEYWORD.PY(TF-IDF) AND MODIFIED AS TF 
def get_type_news_keyword(news_dataset, total_keyword_num, keyword_type):
	grams_tupples = {}
	grams = {}
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
				check_status = 1

		# df means to collect the set of each terms in one news
		for tmp_tupples in set(temp_tf_tupples):
			tf_tupples.append(tmp_tupples)

		# Select terms every 5000 news
		if count%5000 == 0:
			print("Start cleaning: ",count)
			temp_tf_counter = collections.Counter(tf_tupples)
			print("temp_tf_counter"+str(len(temp_tf_counter)))
			temp_tf_tupples_cleaner = []
			for collect in temp_tf_counter.most_common(1000):
				temp_tf_tupples_cleaner += [collect[0] for i in range(0,collect[1])]
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
	temp_tf_counter = collections.Counter(tf_tupples)
	print("temp_tf_counter"+str(len(temp_tf_counter)))
	temp_tf_tupples_cleaner = []
	for collect in temp_tf_counter.most_common(1000):
		temp_tf_tupples_cleaner += [collect[0] for i in range(0,collect[1])]
	tf_tupples = temp_tf_tupples_cleaner

	# Print out the most common terms
	tf_counter = collections.Counter(tf_tupples)
	# print(df_counter.most_common(20))
	# print(tf_counter.most_common(20))

	# Write into xls file
	final_keyword = get_final_key_word(tf_counter,count-1,total_keyword_num,keyword_type)
	return final_keyword
  
  def get_final_key_word(tf_counter,count,keyword_num, keyword_type):

	total_keyword_array = {}
	final_keyword_array = []
	for terms in tf_counter:
		total_keyword_array[array_merge(terms)] = tf_counter[terms]
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

def array_merge(terms):
	result = ""
	for text in terms:
		result += text
	return result

def isEnglish(s):
    try:
        s.encode(encoding='utf-8').decode('ascii')
    except UnicodeDecodeError:
        return False
    else:
        return True

