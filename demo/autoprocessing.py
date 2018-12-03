import os

import sys
print 'Count:', len(sys.argv)
print 'Type:', type(sys.argv)
for arg in sys.argv:
    print 'Argument:', arg

count = 0
for (dirname, dirs, files) in os.walk('.'):
    print '-------------------'
    print dirname
    print dirs
    print files
    for filename in files:
        if filename.endswith('py') :
            thefile = os.path.join(dirname,filename)
            print os.path.getsize(thefile),os.path.abspath(thefile)

print 111