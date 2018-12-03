#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2018/9/5 14:21
# @Author  : Cifer
# @File    : huawei.py



import sys
# line = input('')
# print(line)
# for line in sys.stdin:
#     a = line.split()
#     print(int(a[0]) + int(a[1]))

import sys
#
# # a=0
# # for line in sys.stdin:
# #     a = int(line)
# a = 7
# def factors(val):
#     result = []
#     for i in range(2, val):
#         if val % i == 0:
#             result.append(i)
#             result += factors(val / i)
#             break
#     if len(result) == 0:
#         result.append(val)
#     return result
# num = 1
# val = 1
# while num < a:
#     val += 1
#     cl = factors(val)
#     for i in range(len(cl) - 1, -1, -1):
#         if cl[i] == 2 or cl[i] == 3 or cl[i] == 5:
#             cl.pop(i)
#     if len(cl) == 0:
#         num += 1
# # print(val)
#
#
# num_dict = dict(zip('abcdefghijklmnopqrstuvwxyz', range(0, 26)))
# word_dict = dict(zip(range(0, 26), 'abcdefghijklmnopqrstuvwxyz'))
#
# a, b = 'z', 'bc'
#
#
# def word2num(word):
#     val = 0
#     for i in range(len(word)):
#         val += num_dict[word[i]] * (26 ** (len(word) - i - 1))
#     return val
#
#
# def num2word(num):
#     i = 0
#     result = ''
#     while num >= 26 ** (i + 1):
#         i += 1
#     while i > 0:
#         result += word_dict[int(num / (26 ** i))]
#         num = num % (26 ** i)
#         i -= 1
#     result += word_dict[num]
#     return result

#
# a1 = word2num(a)
# b1 = word2num(b)
# print(a1, b1)
# result = num2word(a1 + b1)
# print(result)

import re
a = 'a11b2bac3bad3abcd2'
word = re.findall('[a-z]+', a)
num = [int(n) for n in re.findall('\d+', a)]

r_list = zip(word, num)
r_list.sort(key = lambda x: (x[1], len(x[0]), x[0]))
result = ''
for (word, iter) in r_list:
    for _ in range(iter):
        result += word
print(result)
