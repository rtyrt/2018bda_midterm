import get_news_dataset as news_dataset
import stock as stock
import get_keyword as keyword
import pickle

# ---------------- Functions ----------------


#--------------------------------------------


# --------------- Main code ---------------

# Input variables
input_firm = "asus"
total_keyword_num = 166

# Load total news dataset
total_news_dataset = news_dataset.load_news_data()

# Get keywords of both rising and falling news
news_keyword = keyword.get_news_keyword(total_news_dataset,input_firm,total_keyword_num)
print(news_keyword)

# Use RandomForest predict the new news

# Get the input_firm's keyword
# firm_keyword = keyword.get_firm_keyword(total_news_dataset,input_firm)

# Use the result of RandomForest's prediction to conclude whether the day will rise or fall

# total_data={}
# filename = "./falling_keyword.p"
# fileObject = open(filename,'rb')
# total_data = pickle.load(fileObject)
# print(total_data)


# -----------------------------------------
