"""
Merge function for 2048 game.
"""
def nonempty(line):
    """
    Function that slid over all of the non-zero tiles 
    to the beginning
    """
    templist = []    
    for index in range(len(line)):
            templist.append(0)
    temp = 0
    for index in range(len(line)):   
        if line[index] != 0:
            templist[temp] = line[index]
            temp = temp + 1
        else:
            continue
    return templist

def merge(line):
    """
    Function that merges a single row or column in POC_2048.
    """
    templist = nonempty(line)
    index = 0;
    while (index < len(templist)-1):
        if templist[index] == templist[index+1]:
            templist[index] = templist[index] * 2
            templist[index+1] = 0
            index = index + 1
        index = index +1
    return nonempty(templist)

print merge([2,4,0,2])
