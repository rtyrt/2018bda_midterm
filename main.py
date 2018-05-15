import get_news_dataset as news_dataset
import stock as stock
import get_keyword as keyword
import randomforest as randomforest
import create_firm_keyword as firms_keyword
import daily_stock_predict as daily_stock_predict
import pickle

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
print(news_keyword)

# Use RandomForest predict the new news
# predict_result = randomforest.predict_by_randomforest(total_news_dataset,stock_data,news_keyword)

# Get the input_firm's keyword
# firm_keyword = firms_keyword.get_firm_keyword(total_keyword_num,input_firm)
# firm_keyword = firm_keyword.load_firm_keyword(input_firm)
# firm_keyword_vector = firm_keyword.load_firm_keyword_vector(input_firm,firm_keyword)

# Use the result of RandomForest's prediction to conclude whether the day will rise or fall
# daily_predict_result = daily_stock_predict.predict(predict_result,total_news_dataset,stock_data,firm_keyword,firm_keyword_vector)
print(daily_predict_result)

# -----------------------------------------
