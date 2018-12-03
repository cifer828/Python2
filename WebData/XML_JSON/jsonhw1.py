import json
import urllib2

# url1 = "http://python-data.dr-chuck.net/comments_42.json"
url2 =  "http://python-data.dr-chuck.net/comments_254441.json"
netjson = urllib2.urlopen(url2).read()
info = json.loads(netjson)['comments']
print json.dumps(info, indent=4)
sum = 0
for item in info:
    sum += int(item['count'])
print 'Count:', len(info)
print 'Sum:', sum
