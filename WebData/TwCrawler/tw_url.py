#!/usr/bin/python
# -*- coding: utf-8 -*-
"""
Return a url for certain Twitter API
"""
import urllib
import tw_hidden_info
import oauth
import json
import chardet
import re

# import sys
#
# reload(sys)
# print sys.getdefaultencoding()
# sys.setdefaultencoding('utf8')


def augment(url, parameters) :
    secrets = tw_hidden_info.oauth()
    consumer = oauth.OAuthConsumer(secrets['consumer_key'], secrets['consumer_secret'])
    token = oauth.OAuthToken(secrets['token_key'], secrets['token_secret'])

    oauth_request =oauth.OAuthRequest.from_consumer_and_token(consumer,token=token, http_method='GET', http_url=url, parameters=parameters)
    oauth_request.sign_request(oauth.OAuthSignatureMethod_HMAC_SHA1(), consumer, token)
    return oauth_request.to_url()


def test_me() :
    print '* Calling Twitter...'
    url = augment('https://api.twitter.com/1.1/statuses/user_timeline.json',
        {'screen_name': 'zhqchen', 'count': '2'} )
    print url
    connection = urllib.urlopen(url)
    data = connection.read()
    # print data
    jsondata = json.loads(data)
    print 'My latest Tweet: \n', json.dumps(jsondata[0]['text'], indent=4, ensure_ascii=False)
    headers = connection.info().dict
    print 'x-rate-limit-remaining: ', headers['x-rate-limit-remaining']



# test_me()
