"""
Student code for Word Wrangler game
http://www.codeskulptor.org/#user41_lhpy3nKqiL_5.py
"""

import urllib2
# import poc_wrangler_provided as provided
import time

WORDURL = "http://codeskulptor-assets.commondatastorage.googleapis.com/assets_scrabble_words3.txt"


# Functions to manipulate ordered word lists

def remove_duplicates(list1):
    """
    Eliminate duplicates in a sorted list.

    Returns a new sorted list with the same elements in list1, but
    with no duplicates.

    This function can be iterative.
    """
    results = []
    for ele in list1:
         if ele not in results:
                results.append(ele)
    return results

#print remove_duplicates([1, 3, 4, 6, 7, 1, 4])

def intersect(list1, list2):
    """
    Compute the intersection of two sorted lists.

    Returns a new sorted list containing only elements that are in
    both list1 and list2.

    This function can be iterative.
    """
    results = []
    len1 = len(list1)
    len2 = len(list2)
    idx1 = 0
    idx2 = 0
    while idx1 < len1 and idx2 < len2:
        if list1[idx1] < list2[idx2]:
            idx1 += 1
        elif list1[idx1] > list2[idx2]:
            idx2 += 1
        else:
            results.append(list1[idx1])
            idx1 += 1
            idx2 += 1
    return results
#print intersect([1, 2, 2, 4, 5, 6], [2, 3, 4, 5])

# Functions to perform merge sort

def merge(list1, list2):
    """
    Merge two sorted lists.

    Returns a new sorted list containing those elements that are in
    either list1 or list2.

    This function can be iterative.
    """
    results= []
    i = 0
    j = 0
    while i < len(list1) and j < len(list2):
        if list1[i] < list2[j]:
            results.append(list1[i])
            i += 1
        else:
            results.append(list2[j])
            j += 1
    if i == len(list1):
        results += list2[j: ]
    if j == len(list2):
        results += list1[i: ]
    return results

def merge_sort(list1):
    """
    Sort the elements of list1.

    Return a new sorted list with the same elements as list1.

    This function should be recursive.
    """
    if len(list1) <= 1:
        return list1
    mid = len(list1) / 2
    first_half = merge_sort(list1[: mid])
    second_half = merge_sort(list1[mid: ])
    return merge(first_half, second_half)

# Test for merge_sort()
#import random
#def test_for_merge_sort(test_num, test_len):
#    for _ in range(test_num):
#        random_list = [random.randrange(1, 20) for _ in range(test_len)]
#        build_in_sort = sorted(random_list)
#        my_merge_sort = merge_sort(random_list)
#        for idx in range(test_len):
#            if build_in_sort[idx] != my_merge_sort[idx]:
#                print "################################################"
#                print "Random list: ", random_list
#                print "Expected sorted list: ", build_in_sort
#                print "My sorted list: ", my_merge_sort
#                print
#test_for_merge_sort(10, 10)

# Function to generate all strings for the word wrangler game

def gen_all_strings(word):
    """
    Generate all strings that can be composed from the letters in word
    in any order.

    Returns a list of all strings that can be formed from the letters
    in word.

    This function should be recursive.
    """
    if not word:
        return [""]
    first = word[0]
    rest_strings = gen_all_strings(word[1: ])
    new_strings = []
    for string in rest_strings:
        for idx in range(len(string) + 1):
            new_strings.append(string[: idx] + first + string[idx: ])
    return rest_strings + new_strings

# print gen_all_strings("aab")

# Function to load words from a file

def load_words(url):
    """
    Load word list from the file named filename.

    Returns a list of strings.
    """
    netfile = urllib2.urlopen(url)
    strings_list = []
    time.clock()
    for line in netfile.readlines():
        strings_list.append(line[: -1])
    print time.clock()
    return strings_list

print len(load_words(WORDURL))

def run():
    """
    Run game.
    """
    words = load_words(WORDURL)
    wrangler = provided.WordWrangler(words, remove_duplicates,
                                     intersect, merge_sort,
                                     gen_all_strings)
    provided.run_game(wrangler)

# Uncomment when you are ready to try the game
# run()


