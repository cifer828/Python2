import sqlite3

conn = sqlite3.connect('friends.sqlite')
cur = conn.cursor()

cur.execute('SELECT * FROM People')
count = 0
print 'People:'
for row in cur :
    if count < 5: print row
    count = count + 1
print count, 'rows.'

cur.execute('SELECT * FROM Follows')
count = 0
print 'Follows:'
for row in cur :
    if count < 5: print row
    count = count + 1
print count, 'rows.'

cur.execute('''SELECT p1.name as follower, p2.name as followee FROM People as p1 JOIN Follows JOIN People as p2
ON Follows.from_id = p1.id  and Follows.to_id = p2.id WHERE Follows.from_id = 2''')
count = 0
print 'Connections for id = 2:'
for row in cur :
    if count < 5: print row
    count = count + 1
print count, 'rows.'

cur.close()
