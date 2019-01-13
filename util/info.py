from urllib import request
import json

#try:
#    with open('api.json', 'r') as file:
#        api_dict = json.load(file)
#except:
#    print("Missing api.json")
'''
Given a search result, returns the company name if exists, otherwise returns "NONE"
'''
def getSymbol(name):
    #    try:
    iexUrl = request.Request("https://api.iextrading.com/1.0/ref-data/symbols", headers={'User-Agent': 'Mozilla/5.0'})
    data = json.loads(request.urlopen(iexUrl).read())
    symbols = {}
    for comp in data:
        companyName = comp["name"].lower()
        companyName = companyName.replace(".", " ")
        companyName = companyName.replace("&", "and")
        companyName = " " + companyName
        #print (companyName)
        symbols[companyName] = [comp["symbol"], comp["name"]]

    retval = {}
    counter = 0
    for each in symbols:
        if (each.find(name) != -1):
            # retval{symbol: name}
            retval[symbols[each][0]] = symbols[each][1]
            counter = counter + 1
    if (counter > 0):
        #print (retval)
        return retval
    else:
        return "NONE"

def quickGetSymbol(name):
    #    try:
    iexUrl = request.Request("https://api.iextrading.com/1.0/ref-data/symbols", headers={'User-Agent': 'Mozilla/5.0'})
    data = json.loads(request.urlopen(iexUrl).read())
    symbols = {}
    for comp in data:
        #print (companyName)
        symbols[comp["name"]] = comp["symbol"]

    if name in symbols:
        return symbols[name]
    else:
        return "NONE"

'''
Given a valid IEX Trading company symbol, will return the stock information of the past 30 days.
'''
def getStocks(symbol):
    name = symbol.lower()
    iexUrl = request.Request("https://api.iextrading.com/1.0/stock/" + name + "/batch?types=quote,news,chart&range=1m&last=10", headers={'User-Agent': 'Mozilla/5.0'})
    data = json.loads(request.urlopen(iexUrl).read())
    return data["chart"]




#print(getStocks("Apple Inc."))
