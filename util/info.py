import urllib
import json

#try:
#    with open('api.json', 'r') as file:
#        api_dict = json.load(file)
#except:
#    print("Missing api.json")

def getCompany(name):
#    try:
    iexUrl =  urllib.request.Request("https://api.iextrading.com/1.0/ref-data/symbols", headers={'User-Agent': 'Mozilla/5.0'})
    data = json.loads(request.urlopen(f2fUrl).read())
    print(data)
    return data

print(getCompany("yes"))
