import urllib
import tw_url
import json

TWITTER_URL = 'https://api.twitter.com/1.1/statuses/user_timeline.json'

while True:
    print ''
    acct = raw_input('Enter Twitter Account:')
    if ( len(acct) < 1 ) : break
    url = tw_url.augment(TWITTER_URL,
                         {'screen_name': acct, 'count': '2'})
    print 'Retrieving', url
    connection = urllib.urlopen(url)
    data = connection.read()
    jsondata = json.loads(data)
    try:
        print 'Latest Tweet: \n', json.dumps(jsondata[0]['text'], indent=4, ensure_ascii=False)
    except:
        print 'Wrong Account.'
    headers = connection.info().dict
    # print headers
    print 'Limit-Remaining: ', headers['x-rate-limit-remaining']
