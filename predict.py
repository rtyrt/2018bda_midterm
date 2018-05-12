def tell_me_buy_or_sell(doc):
    #do something
    #return 1:buy -1:sell 0:not sure

# docs = ["doc1","doc2",...] the set of news in a day
def predict(docs):
    buy_score = 0
    sell_score = 0
    for doc in docs:
        strategy = tell_me_buy_or_sell(doc)
        if strategy:
            weight = like_Asus(doc)
            if strategy == 1:
                buy_score += weight
            else:
                sell_score += weight

    #change condition to modify strategy
    if(buy_score>=sell_score*1.1):
        return 1; #buy
    else if(sell_score>=buy_score*1.1)
        return -1; #sell
    else
        return 0; #do nothing

# terms = [] of 166 Asus-like term, Asus_vector = [] of Asus 166 word count vector

def like_Asus(doc):
    v = []
    for i in range(0,len(terms)):
        v.append(doc.count(terms[i]))
    return cosine(v,Asus_vector)

def cosine(vec1,vec2):
    cos = 0
    for i in range(0,len(vec1)):
        cos+=vec1[i]*vec2[i]
    return cos/sum(i**2 for i in vec1)**0.5/sum(i**2 for i in vec2)**0.5
