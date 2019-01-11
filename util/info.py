from urllib import request
import json

#try:
#    with open('api.json', 'r') as file:
#        api_dict = json.load(file)
#except:
#    print("Missing api.json")
'''
Given a company name, returns the company symbols if exists, otherwise returns "NONE"
'''
def getCompany(name):
#    try:
    iexUrl = request.Request("https://api.iextrading.com/1.0/ref-data/symbols", headers={'User-Agent': 'Mozilla/5.0'})
    data = json.loads(request.urlopen(iexUrl).read())
    symbols = {}
    for comp in data:
        symbols[comp["name"]] = comp["symbol"]
    if name in symbols:
        return symbols[name]
    else:
        return "NONE"
'''
Given a valid IEX Trading symbol, will return the stock information of the past 30 days.
'''
def getStocks(symbol):
	comp = getCompany(symbol)
	iexUrl = request.Request("https://api.iextrading.com/1.0/stock/" +comp + "/batch?types=quote,news,chart&range=1m&last=10", headers={'User-Agent': 'Mozilla/5.0'})
	data = json.loads(request.urlopen(iexUrl).read())
	return data["chart"]
	
		
		
		
#print(getStocks("Apple Inc."))