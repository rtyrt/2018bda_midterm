from datetime import datetime


def predict(predict_result,total_news_dataset,stock_data,firm_keyword,firm_keyword_vector):
	date_predict = {}
	test_len = len(predict_result)
	test_right = 0
	do_nothing = 0
	for date in predict_result:
		buy_score = 0
		sell_score = 0

		# Add buy_score and sell_score
		for news in range(0,len(predict_result[date])):
			strategy = 0
			if(news["predicted_stock"] == 1):
				buy_score += 1
				# buy_score += like_firm(news["content"],firm_keyword,firm_keyword_vector)
			else:
				sell_score += 1
				# sell_score += like_firm(news["content"],firm_keyword,firm_keyword_vector)

		#change condition to modify strategy
		if(buy_score>=sell_score*1.1):
			strategy = 1
		else if(sell_score>=buy_score*1.1)
			strategy = 0
		else
			do_nothing += 1

		# Current date's guess will result in stock of two days later
		current_date = date
		two_days_later = compute_date_after(current_date,2)

		# Check accuracy result
		if strategy == stock_data[two_days_later][1]:
			test_right += 1

		# Calculate final prediction - buy or not
		# if not date_predict.__contains__(date):
		# 	date_predict[date] = {}
		# 	date_predict[date]["rise"] = 0
		# 	date_predict[date]["fall"] = 0
		# 	date_predict[date]["none"] = 0

	return {"accuracy":test_right/test_len, "do_nothing": do_nothing}

# terms = [] of 166 Asus-like term, Asus_vector = [] of Asus 166 word count vector
def like_firm(doc,firm_keyword,firm_keyword_vector):
	v = []
	for term in range(0,len(firm_keyword)):
		v.append(doc.count(term))
	return cosine(v,firm_keyword_vector)

def cosine(vec1,vec2):
	cos = 0
	for i in range(0,len(vec1)):
		cos+=vec1[i]*vec2[i]
	return cos/sum(i**2 for i in vec1)**0.5/sum(i**2 for i in vec2)**0.5

# get date string in following format, 2016-09-01
def get_date(date_time):
	return datetime.strftime(date_time,"%Y-%m-%d")

# compute date n days after
def compute_date_after(date,n):
	temp_date_time = datetime.strptime(date, "%Y-%m-%d")
	temp_date_time = temp_date_time + timedelta(days = n)
	return datetime.strftime(temp_date_time,"%Y-%m-%d")
