# Note - this code must run in Python 2.x and you must download
# http://www.pythonlearn.com/code/BeautifulSoup.py
# Into the same folder as this program

import urllib
from WebData.Examples.BeautifulSoup import *

url = raw_input('Enter - ')
html = urllib.urlopen(url).read()
soup = BeautifulSoup(html)
num_list = []
# Retrieve all of the anchor tags
tags = soup('span')
for tag in tags:
    # Look at the parts of a tag
    print tag.contents[0]
    num_list.append(int(tag.contents[0]))

count = len(num_list)
sum = sum(num_list)
print "Count ", count
print "Sum ", sum