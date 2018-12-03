# coding=utf-8
def test1():
    n = int(raw_input())
    sign = 1
    sum = 0
    for i in range(1, n + 1):
        sum += i * sign
        sign *= -1
    print sum

def test2():
    input = raw_input()
    num_list = [int(i) for i in input.split()]
    idx = 0
    while(idx < len(num_list) - 1):
        idx += num_list[idx]
    if idx > len(num_list) - 1:
        print idx
        print False
    elif idx == len(num_list) - 1:
        print True

def test3():
    target = int(raw_input())
    num_list= [4,5,6,5,6,7,8,9,10,9]
    current_idx = 0
    while(num_list[current_idx] != target):
        current_idx += abs(target - num_list[current_idx])
    print current_idx

def test4():
    print test4_op('abc')[:-1]

def test4_op(s):
    if len(s) == 0:
        return ['']
    else:
        sub = test4_op(s[1:])
        return [s[0] + comb for comb in sub] + sub

# -*- coding:utf-8 -*-
def kp(arr,i,j):#快排总函数
                #制定从哪开始快排
    if i<j:
        base=kpgc(arr,i,j)
        kp(arr,i,base)
        kp(arr,base+1,j)
def kpgc(arr,i,j):#快排排序过程
    base=arr[i]
    while i<j:
        while i<j and arr[j]>=base:
            j-=1
        while i<j and arr[j]<base:
            arr[i]=arr[j]
            i+=1
            arr[j]=arr[i]
        arr[i]=base
    return i
ww=[3,2,4,1,59,23,13,1,3]
print ww
# kp(ww,0,len(ww)-1)
# print ww

def test5(arr):
    arr[0], arr[1] = arr[1], arr[0]

test5(ww)
print(ww)
# test4()
