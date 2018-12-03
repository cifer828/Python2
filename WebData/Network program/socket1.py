import socket
import urllib2
from raw_string_trans import *
mysock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
# print socket.gethostbyname('www.py4inf.com')
mysock.connect(('www.py4inf.com', 80))
mysock.send('GET http://www.py4inf.com/code/romeo.txt HTTP/1.0\n\n')

while True:
    data = mysock.recv(1000)
    if ( len(data) < 1 ) :
        break
    print "--------------------"
    print data

mysock.close()

myurl = urllib2.urlopen("http://www.py4inf.com/code/romeo.txt")
print '---------------------'
print myurl.info()
print myurl.read()