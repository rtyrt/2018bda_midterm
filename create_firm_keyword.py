import pickle
import re
import string
import collections
import math
import operator
import pickle
import jieba
from nltk import ngrams
from datetime import datetime, timedelta

#-----------------------Functions--------------------------------------------
def get_firm_keyword(total_keyword_num,firm_name):
	filename=firm_name+"_related_news.p"
	f=open(filename,'rb')
	firm_news=pickle.load(f)
	firm_news = one_array_list(firm_news)
	result = get_type_news_keyword(firm_news,total_keyword_num,firm_name)
	print(result)
	return result

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

		news_dataset[news] = re.sub("[A-Za-z0-9\[\`\~\。\，\「\」\！\：\!\@\#\$\^\&\*\(\)\=\|\{\}\'\:\;\'\,\[\]\.\<\>\/\?\~\！\@\#\\\&\*\%]", "", news_dataset[news])
		grams = jieba.cut(news_dataset[news], cut_all=False)
		for tupples in grams:
			if len(tupples) > 1 and len(tupples) <= 4:
				grams_tupples[news].append(tupples)
				temp_tf_tupples.append(tupples)

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

# load firm keyword
# 	output:	an array with each dataset's keywords
def load_firm_keyword(firm_name):
	total_data={}
	filename = "./"+firm_name+"_keyword.p"
	fileObject = open(filename,'rb')
	total_data = pickle.load(fileObject)
	return total_data

# load firm keyword vector
# 	output:	an array with each keywords' tf in such firm's dataset
def load_firm_keyword_vector(firm_name,firm_keyword):
	total_data={}
	filename=firm_name+"_related_news.p"
	f=open(filename,'rb')
	firm_news=pickle.load(f)
	firm_news = one_array_list(firm_news)
	vector = []
	for term in range(0,len(firm_keyword)):
		for news in firm_news:
			vector.append(news.count(firm_keyword[term]))
	
	return vector
