# Note - this code must run in Python 2.x and you must download
# http://www.pythonlearn.com/code/BeautifulSoup.py
# Into the same folder as this program

import re
import urllib

from WebData.Examples.BeautifulSoup import *

url = raw_input('Enter URL: ')
count = raw_input('Enter count: ')
pos = raw_input('Enter position: ')
print "Retrieving: ", url

for _ in range(int(count)):
    html = urllib.urlopen(url).read()
    soup = BeautifulSoup(html)
    tags = soup('a')
    # print tags
    pos_idx = 1
    for tag in tags:
        if pos_idx < int(pos):
            pos_idx += 1
            continue
        url = tag.get('href', None)
        print "Retrieving: ", url
        break

print re.findall('_by_(.*)\.', url)[0]

