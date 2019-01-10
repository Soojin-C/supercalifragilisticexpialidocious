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

#print(getCompany("Nymox Pharmaceutical Corporation"))
