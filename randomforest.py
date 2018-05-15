import numpy as np
import pandas as pd
from sklearn import cross_validation, ensemble, preprocessing, metrics
import pickle
import math
from datetime import datetime, timedelta

# ---------------- Functions ----------------
def predict_by_randomforest(total_news_dataset,stock_data,news_keyword):
	
	# Get the dataframe
	total_news = get_total_news(total_news_dataset,stock_data,news_keyword)
	# news_train = get_dataframe(total_news,stock_data,news_keyword)
	news_train = pd.read_pickle("svm.p")

	# 建立x, y軸所需的資料
	# news_X = pd.DataFrame([news_train["Pclass"],news_train["Age"]]).T
	# news_x = news_train.drop('id','date','stock'], axis=1).T
	# news_y = news_train["stock"]
	# train_x, test_x, train_y, test_y = cross_validation.train_test_split(news_x, news_y, test_size = 0.3)

	# Use date to randomly split the training dataset
	date_index = pd.DataFrame(list(set(news_train["date"])))
	date_index.columns = ["date"]
	train_date, test_date = cross_validation.train_test_split(date_index, test_size = 0.3)

	# Get real training data and testing data
	train_index = news_train.loc[news_train["date"].isin(train_date["date"].tolist())]
	test_index = news_train.loc[news_train["date"].isin(test_date["date"].tolist())]
	train_x = train_index.drop(['id','date','stock'], axis=1)
	train_y = train_index["stock"]
	test_x = test_index.drop(['id','date','stock'], axis=1)
	test_y = test_index["stock"]

	print("length of train: ",len(train_y))
	print("length of test: ",len(test_y))

	# 建立 random forest 模型
	forest = ensemble.RandomForestClassifier(n_estimators = 5)
	forest_fit = forest.fit(train_x, train_y)
	# print(forest_fit)

	# 預測
	test_y_predicted = forest.predict(test_x)
	# print(test_y_predicted)

	# 績效
	accuracy = metrics.accuracy_score(test_y, test_y_predicted)
	print(accuracy)

	df_result = test_index[["id","date"]]
	df_result['predicted_stock'] = test_y_predicted
	# print(df_result.head(5))

	result_dict = {}
	for index, row in df_result.iterrows():
		if not result_dict.__contains__(row["date"]): 
			result_dict[row["date"]] = []
		temp_dict = {}
		temp_dict["content"] = total_news[row["id"]-1]["content"]
		temp_dict["predicted_stock"] = row["predicted_stock"]
		result_dict[row["date"]].append(temp_dict)
	return result_dict

def get_total_news(total_news_dataset,stock_data,news_keyword):
	total_news = []
	news_counter = 1
	for date in total_news_dataset:
		current_date = date
		two_days_after = compute_date_after(current_date,2)
		for news_index in range(0,len(total_news_dataset[date])):
			if stock_data.__contains__(two_days_after) and len(stock_data[two_days_after]) == 2:
				temp_news_array = {}
				temp_news_array["id"] = news_counter
				temp_news_array["date"] = date
				temp_news_array["content"] = total_news_dataset[date][news_index]
				temp_news_array["stock"] = stock_data[two_days_after][1]
				total_news.append(temp_news_array)
				news_counter += 1
	return total_news

def get_dataframe(total_news,stock_data,news_keyword):

	# initiate
	keyword_df = {}
	news_tfidf = {}

	# calculate df, tf, tf-idf
	keyword_df = get_keyword_df(total_news,news_keyword)
	news_tfidf = get_news_keyword_tfidf(total_news,news_keyword,keyword_df,len(total_news))
	return news_tfidf

# Compute the df of terms in keyword
#   input:
#       content, content of all news 
#       keyword, an array with the selected keywords believed to be influential on news
#	output:
#		keyword_df, a dict recording each keyword's df
#		keyword_df["鴻海"]=2066
def get_keyword_df(content,keyword):
	keyword_df = {}
	for term in keyword:
		keyword_df[term] = 0
		for news in content:
			if(term in news["content"]):
				keyword_df[term] += 1
	# print(keyword_df)
	return keyword_df

# Compute the tfidf of each keyword for all news
#   input:
#       content, content of all news 
#       keyword, an array with the selected keywords believed to be influential on news
#		keyword_df, a dict recording each keyword's df
#		N, number of total news
#	output:
#		news_tfidf, a dict recording each keyword's tfidf for the given news
#		news_tfidf[1]
#		news_tfidf[1]["鴻海"]=0.0000444252
def get_news_keyword_tfidf(content,keyword,keyword_df,N):
	# news_dataframe = {}
	print("Start get_news_keyword_tfidf")
	news_dict = {}
	news_dict["id"] = []
	news_dict["date"] = []
	news_dict["stock"] = []
	for news in content:
		# news_tfidf[news] = get_each_news_keyword_tfidf(content[news]["content"],keyword,keyword_df,N)
		temp_tfidf = get_each_news_keyword_tfidf(news["content"],keyword,keyword_df,N)
		news_dict["id"].append(news["id"])
		news_dict["date"].append(news["date"])
		news_dict["stock"].append(news["stock"])
		for temp_keyword in temp_tfidf:
			if not news_dict.__contains__(temp_keyword) or not temp_tfidf.__contains__(temp_keyword):
				news_dict[temp_keyword] = []
			news_dict[temp_keyword].append(temp_tfidf[temp_keyword])
		
	# return dataframe of news_dict
	print("Start turning into dataframe")
	news_dataframe = pd.DataFrame(news_dict)

	print("Start turning into pickle")
	news_dataframe.to_pickle("svm.p")
	return news_dataframe

# Compute the tfidf of each keyword for the given news
# *** Notice that the tfidf here is normalized in order to calculate cosine similarity eazier later 
def get_each_news_keyword_tfidf(content,keyword,keyword_df,N):
	news_tfidf = {}
	news_vector_length = 0
	normalized_tfidf = {}
	for term in keyword:
		keyword_tf = content.count(term)
		if keyword_tf == 0:
			news_tfidf[term] = 0
		else:
			news_tfidf[term] = (1 + math.log10(keyword_tf)) * math.log10(N/keyword_df[term])
			news_vector_length += news_tfidf[term] * news_tfidf[term]
	for term in keyword:
		if news_vector_length == 0:
			normalized_tfidf[term] = 0
		else:
			normalized_tfidf[term] = news_tfidf[term] / math.sqrt(news_vector_length)
	return normalized_tfidf

# get date string in following format, 2016-09-01
def get_date(date_time):
	return datetime.strftime(date_time,"%Y-%m-%d")

# compute date n days after
def compute_date_after(date,n):
	temp_date_time = datetime.strptime(date, "%Y-%m-%d")
	temp_date_time = temp_date_time + timedelta(days = n)
	return datetime.strftime(temp_date_time,"%Y-%m-%d")
#--------------------------------------------
