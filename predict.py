def predict(docs,terms,vector):
    buy_score = 0
    sell_score = 0
    for doc in docs:
        strategy = doc["predicted_stock"]
        weight = likelyhood(doc["content"],terms,vector)
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
    return cos/sum(i**2 for i in vec1)**0.5/sum(i**2 for i in vec2)**0.5
