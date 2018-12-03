import random
def merge(line):
    new_line = ([0] * len(line))
    non_zero_entry = 0
    for i in range(0, len(line)):
        if (line[i] != 0):
            new_line[non_zero_entry] = line[i]
            non_zero_entry += 1
    new_merge_line = ([0] * len(line))
    new_merge_entry = 0
    i = 0
    while (i < (non_zero_entry - 1)):
        if (new_line[i] == new_line[(i + 1)]):
            new_merge_line[new_merge_entry] = (new_line[i] * 2)
            i += 2
        else:
            new_merge_line[new_merge_entry] = new_line[i]
            i += 1
        new_merge_entry += 1
    new_merge_line[new_merge_entry] = new_line[i]
    return new_merge_line

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

def my_merge(line):
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

def gen_all_sequences(outcomes, length):
    """
    Iterative function that enumerates the set of all sequences of
    outcomes of given length
    """
    ans = set([()])
    for dummy_idx in range(length):
        temp = set()
        for seq in ans:
            for item in outcomes:
                new_seq = list(seq)
                new_seq.append(item)
                temp.add(tuple(new_seq))
        ans = temp
    return ans

TEST_CASES = [[8, 4, 8, 8, 2, 2, 4, 8]]
def test():
    for i in range(10,1,-1):
        test_lists=list(gen_all_sequences([0,2,4,8],i))
        print i
        for Test_list in test_lists:
            print list(Test_list)
            if merge(list(Test_list))!=my_merge(list(Test_list)):
                print "Test_list",list(Test_list)
                print "my",my_merge(list(Test_list))
                print "wrong",merge(list(Test_list))

print merge([8, 8, 4, 8, 2, 8, 2, 2, 8, 8])
test()