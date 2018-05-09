from openpyxl import load_workbook
import operator
import re
import string
import collections
import math
import numpy as np
import pickle

#————————————————————————FUNCTIONS——————————————————————————

#input:(name,table)=(stock name string, excel sheet)
#output:dictionary in the form of{date time:price}
#
def get_stock_data(name,table):
    stock={}
    for row in table:
        if (row[0].value==name):
            stock[row[1].value]=[]
            stock[row[1].value].append(row[2].value)

    filename = "./stock_data_"+name.split(" ")[0]+".p"
    fread = open(filename, "wb")
    pickle.dump(stock, fread)
    fread.close()
    return stock

#input:(name,table)=(stock name string, excel sheet)
#output:dictionary in the form of{date time:price}
#
def load_stock_data(name):
    stock={}
    filename = "./stock_data_"+name.split(" ")[0]+".p"
    fileObject = open(filename,'rb')
    stock = pickle.load(fileObject)
    return stock

#input:(name)=dictionary in the form of{date time:price}
#output: a list of daily_return
#
def get_return(name):   
    price=list(name.values())
    daily_return=[]
    for i in range(len(price)):
        if i<(len(price)-1):
            r=(price[i][0]-price[i+1][0])/price[i+1][0]
            daily_return.append(r)

    return daily_return


#input: a single list of daily_return
#output: a list of 3 element[25%,50%,75%]百分位數
#
def return_para(return_list):
    rr_list=np.array(return_list)
    median=np.percentile(rr_list, 50)
    third_quartile=np.percentile(rr_list,75)
    first_quartile=np.percentile(rr_list,25)
    
    para=[first_quartile,median,third_quartile]
    return para


#input:(return_list,para,name)=(a single list of daily_return,a list of 3 element[25%,50%,75%],dictionary in the form of{date time:price})
#output: dictionary in the form of{date time:price,1/0/-1}
#
def assign_return_value(return_list,para,name):
    for each_daily_return in return_list:
        if (each_daily_return>0 or each_daily_return>para[2]):
            each_daily_return=1
        elif (each_daily_return<0 or each_daily_return<para[0]):
            each_daily_return=-1
        else:
            each_daily_return=0
    
    for key,i in zip(name,return_list):
        name[key].append(each_daily_return)
        
    return name


#load excel file 2016 stock 
# wb = load_workbook(filename=r'2016_stock_data.xlsx')
# ws = wb.worksheets[0]
# table_row=ws.rows


#filter out targeted stock info
# asus=get_stock_data("2357 華碩",table_row)
asus=load_stock_data("2357 華碩")
#acer=get_stock_data("2353 宏碁",table_row)
# acer=load_stock_data("2353 宏碁")

#calculate return for each stock
stock_asus_return=get_return(asus)
#stock_acer_return=get_return(acer)

#calculate 百分位數
asus_return_para=return_para(stock_asus_return)
#acer_return_para=return_para(stock_acer_return)


#assign value 1/0/-1 to daily return
stock_asus=assign_return_value(stock_asus_return,asus_return_para,asus)
#stock_acer=assign_return_value(stock_asus_return,acer)


#save as pickle file
file=open('2016_stock_return.p', 'wb')
pickle.dump(stock_asus, file)
#pickle.dump(stock_acer, file)
file.close()
