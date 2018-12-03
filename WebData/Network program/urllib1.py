import urllib2

# Course example
fhand = urllib2.urlopen('http://www.py4inf.com/code/romeo.txt')
print fhand
for line in fhand.readlines():
    print line.strip()

# # my method
# mhand = urllib2.urlopen('http://www.ciferzh.byethost12.com/css/py.txt')
# for line in mhand.readlines():
#     print line.strip()