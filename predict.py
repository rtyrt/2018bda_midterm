from datetime import datetime, timedelta


def predict(predict_result,total_news_dataset,stock_data,firm_keyword,firm_keyword_vector,threshold):
	date_predict = {}
	test_len = len(predict_result)
	test_right = 0
	do_nothing = 0
	for date in predict_result:
		print(date)
		
		# predict each date
		date_strategy = predict_each_date(predict_result[date],firm_keyword,firm_keyword_vector,threshold)

		# Current date's guess will result in stock of two days later
		current_date = date
		two_days_later = compute_date_after(current_date,2)

		# Check accuracy result
		if date_strategy == -1:
			do_nothing += 1
		elif date_strategy == stock_data[two_days_later][1]:
			test_right += 1
		print("date_strategy: ",date_strategy)
		print("real_strategy: ",stock_data[two_days_later][1])

	return {"accuracy":test_right/test_len,"total_test":test_len,"do_nothing": do_nothing}


def predict_each_date(docs,terms,vector,threshold):
	buy_score = 0
	sell_score = 0
	for doc in docs:
		strategy = doc["predicted_stock"]
		weight = likelyhood(doc["content"],terms,vector)
		print(weight)
		# weight = 1
		if strategy == 1:
			buy_score += weight
		else:
			sell_score += weight
	print("buy_score: ",buy_score)
	print("sell_score: ",sell_score)
	#change condition to modify strategy
	if(buy_score>=sell_score*threshold):
		return 1; #buy
	elif(sell_score>=buy_score*threshold):
		return 0; #sell
	else:
		return -1; #do nothing

# terms = [] of 166 Asus-like term, vector = [] of Asus 166 word count vector
def likelyhood(doc,terms,vector):
	v = []
	for i in range(0,len(terms)):
		v.append(doc.count(terms[i]))
	return cosine(v,vector)

def cosine(vec1,vec2):
	cos = 0
	for i in range(0,len(vec1)):
		cos+=vec1[i]*vec2[i]
	sum_vec1 = sum(i**2 for i in vec1)
	print("sum_vec1: ",sum_vec1,end=" ")
	sum_vec2 = sum(i**2 for i in vec2)
	print("sum_vec2: ",sum_vec2)
	if sum_vec1 == 0 or sum_vec2 == 0:
		return 0
	else:
		return cos/sum_vec1**0.5/sum_vec2**0.5

# get date string in following format, 2016-09-01
def get_date(date_time):
	return datetime.strftime(date_time,"%Y-%m-%d")

# compute date n days after
def compute_date_after(date,n):
	temp_date_time = datetime.strptime(date, "%Y-%m-%d")
	temp_date_time = temp_date_time + timedelta(days = n)
	return datetime.strftime(temp_date_time,"%Y-%m-%d")

