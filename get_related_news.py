import pickle

filename='total_dataset.p'
file=open(filename,'rb')
total_data=pickle.load(file)

stock_related_news={}
check_list=['華碩','和碩','華擎','施崇棠','沈振來','皮卡丘','石頭店','以卵擊石','子龍任務']

for date in total_data:
    stock_related_news[date]=[]
    for i in range(len(total_data[date])):
        if any(word in total_data[date][i] for word in check_list) :
            stock_related_news[date].append(total_data[date][i])
            

fileName="./asus_related_news.p"
fread=open(fileName,'wb')
pickle.dump(stock_related_news,fread)
fread.close()

# the output asus_related_news.p format would be: ['2016-09-01'] : ['news1','news2','news3']
# TRY change the keyword in check_list!!!!!
#if you would like to get acer news, just change '華碩' to '宏碁', and saved as './acer_related_news.p'
