import json
import urllib

import tw_url

TWITTER_URL = 'https://api.twitter.com/1.1/friends/list.json'

while True:
    print ''
    acct = raw_input('Enter Twitter Account:')
    if ( len(acct) < 1 ) : break
    url = tw_url.augment(TWITTER_URL,
                         {'screen_name': acct, 'count': '5'})
    print 'Retrieving', url
    connection = urllib.urlopen(url)
    data = connection.read()
    headers = connection.info().dict
    print 'Remaining', headers['x-rate-limit-remaining']
    js = json.loads(data)
    print json.dumps(js, indent=4)

    for u in js['users'] :
        print u['name']+':'
        try:
            s = u['status']['text']
            print 'Latest Tweet: ',s[:50]
        except:
            print 'Latest Tweet: '