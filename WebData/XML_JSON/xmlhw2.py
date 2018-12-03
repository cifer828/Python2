import urllib
import xml.etree.ElementTree as ET

# serviceurl = 'http://python-data.dr-chuck.net/comments_42.xml'

while True:
    url = raw_input('Enter url: ')
    if len(url) < 1:
        break
    print 'Retrieving', url
    data = urllib.urlopen(url).read()
    print 'Retrieved',len(data),'characters'
    tree = ET.fromstring(data)
    counts = tree.findall('.//count')
    sum = 0
    for count in counts:
        sum += int(count.text)
    print "Count: ", len(counts)
    print "Sum: ", sum

