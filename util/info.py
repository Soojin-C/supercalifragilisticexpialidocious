from urllib import request
import json

try:
    with open('keys/keys.json', 'r') as file:
        api_dict = json.load(file)
except:
	print("keys.json not found. Please Look at README.md")
	quit()

'''
Given a search result, returns the company name if exists, otherwise returns "NONE"
'''
def getSymbol(name):
    #    try:
    print(name)
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
        if counter > 10:
            break
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
def getStocksInfo(symbol):
	name = symbol.lower()
	try:
		iexUrl = request.Request("https://api.iextrading.com/1.0/stock/" + name + "/batch?types=quote,news,chart&range=1m&last=10", headers={'User-Agent': 'Mozilla/5.0'})
	except:
		print("Problems with IEX Trading API. API may be broken")
		quit()
	data = json.loads(request.urlopen(iexUrl).read())
	return data["chart"]

'''
Given a valid IEX Trading company symbol, will return the stock information of currently.
'''
def getStocks(symbol):
	name = symbol.lower()
	try:
		iexUrl = request.Request("https://api.iextrading.com/1.0/stock/" + name + "/batch?types=quote,news,chart&range=1m&last=10", headers={'User-Agent': 'Mozilla/5.0'})
	except:
		print("Problems with IEX Trading API. API may be broken")
		quit()
	data = json.loads(request.urlopen(iexUrl).read())
	return data["quote"]

'''
Given a search query, will return a dictionary of snippets of the article and the url
'''
def getArticles(query):
	try:
		nytKey = api_dict["nyt"]
	except:
		print("MISSING NEW YORK TIMES API KEY")
		quit()
	search = query.lower()
	nytUrl = request.Request("https://api.nytimes.com/svc/search/v2/articlesearch.json?api-key=" + nytKey + "&q=" +search + "&fq=news_desk:Financial%20business", headers={'User-Agent': 'Mozilla/5.0'})
	data = json.loads(request.urlopen(nytUrl).read())
	articles = {}
	response = data["response"]["docs"]
	#return response
	for article in response:
		articles[article["headline"]["main"]] = article["web_url"]
	return articles

#print(getStocks("Apple Inc."))
print(getArticles("stock"))
