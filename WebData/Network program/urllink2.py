# Note - this code must run in Python 2.x and you must download
# http://www.pythonlearn.com/code/BeautifulSoup.py
# test url: http://www.dr-chuck.com/page1.htm
# Into the same folder as this program

import urllib

from WebData.Examples.BeautifulSoup import *

url = raw_input('Enter - ')
html = urllib.urlopen(url).read()
print type(urllib.urlopen(url).info())
soup = BeautifulSoup(html)

# Retrieve all of the anchor tags
tags = soup('a')
for tag in tags:
    # Look at the parts of a tag
    print 'TAG:',tag
    print 'URL:',tag.get('href', None)
    print 'Contents:',tag.contents[0]
    print 'Attrs:',tag.attrs
