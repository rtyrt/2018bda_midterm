import pickle

filename='total_dataset.p'
file=open(filename,'rb')
total_data=pickle.load(file)

stock_related_news={}
for date in total_data:
    stock_related_news[date]=[]
    for i in range(len(total_data[date])):
        if '華碩' in total_data[date][i]:
            stock_related_news[date].append(total_data[date][i])
            

fileName="./asus_related_news.p"
fread=open(fileName,'wb')
pickle.dump(stock_related_news,fread)
fread.close()

# the output asus_related_news.p format would be: ['2016-09-01'] : ['news1','news2','news3']
#if you would like to get acer news, just change '華碩' to '宏碁', and saved as './acer_related_news.p'
