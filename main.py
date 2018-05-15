import get_news_dataset as news_dataset
import stock as stock
import get_keyword as keyword
import randomforest as randomforest
import pickle

# ---------------- Functions ----------------


#--------------------------------------------


# --------------- Main code ---------------

# Input variables
input_firm = "asus"
total_keyword_num = 300

# Load total news and stock dataset
total_news_dataset = news_dataset.load_news_data()
stock_data = stock.load_stock_data(input_firm)

# Get keywords of both rising and falling news
news_keyword = keyword.get_news_keyword(total_news_dataset,stock_data,input_firm,total_keyword_num)
# news_keyword = keyword.load_news_keyword()
# print(news_keyword)

# Use RandomForest predict the new news
# predict_result = randomforest.predict_by_randomforest(total_news_dataset,stock_data,news_keyword)

# Get the input_firm's keyword
# firm_keyword = keyword.get_firm_keyword(total_news_dataset,input_firm)

# Use the result of RandomForest's prediction to conclude whether the day will rise or fall

# total_data={}
# filename = "./falling_keyword.p"
# fileObject = open(filename,'rb')
# total_data = pickle.load(fileObject)
# print(total_data)


# -----------------------------------------
