import sys
from time import sleep

output = sys.stdout
for count in range(0,100):
    second = 1

    sleep(second)
    output.write('\r%d\r'%count)
    output.flush()