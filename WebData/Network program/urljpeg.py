import socket
import time
from raw_string_trans import *

mysock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
mysock.connect(('www.py4inf.com', 80))
mysock.send('GET http://www.py4inf.com/cover.jpg HTTP/1.0\n\n')
count = 0
picture = ""
while True:
    data = mysock.recv(5120)
    if (len(data) < 1):
        break
        # time.sleep(0.25)
    count = count + len(data)
    print len(data),count
    picture = picture + data
mysock.close()
# Look for the end of the header (2 CRLF)
pos = picture.find("\r\n\r\n")
print 'Header length',pos
print picture[:pos]

# print raw string
print '--------raw string--------------'
print raw_string(picture[:pos+5])
print '--------raw string--------------'

# Skip past the header and save the picture data
print picture[pos + 4:]
print "-----------------------------------"
print picture[:pos + 4]
picture = picture[pos + 4:]
fhand = open("stuff.jpg","wb")
fhand.write(picture)
fhand.close()