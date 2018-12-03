import os

# get current work directory
print os.getcwd()

# Note: double '\'
os.chdir('C:\\Users\\lenovo\\Documents')

print os.getcwd()

file = open('test2.txt')
print file.read()