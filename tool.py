#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import math
from collections import Counter

def analyse(values):
    total_digg = 0
    total_forward = 0
    digg_list = list()
    forward_list = list()
    lines = list(values)
    count = len(lines)
    for line in lines:
        tmp = line.split("$$", maxsplit=2)
        digg_count = int(float(tmp[0]))
        forward_count = int(float(tmp[1]))
        digg_list.append(digg_count)
        forward_list.append(forward_count)
    total_digg = sum(digg_list)
    total_forward = sum(forward_list)
    digg_avg = total_digg/float(count*1.0)
    forward_avg = total_forward/float(count*1.0)
    digg_avg = round(digg_avg,2)
    forward_avg = round(forward_avg,2)
    digg_variance = var(digg_list,digg_avg)
    forward_variance = var(forward_list,forward_avg)
    digg_exp = exp(digg_list)
    forward_exp = exp(forward_list)
    return total_digg,total_forward,digg_variance,forward_variance,digg_exp,forward_exp

# 求方差的函数
def var(lst,avg):
    var1 = 0
    for i in lst:
        var1 += float((i-avg)**2*1.0)
    # 样本个数为1时，方差为0
    if len(lst) ==1:
        var2 = 0
    else:
        var2 = (math.sqrt(var1/(len(lst)-1)*1.0))
    var2 = round(var2,2)
    return var2

# 求期望的函数
def exp(lst):
    ex = 0
    count = len(lst)
    values_counts = Counter(lst)
    se = set(lst)
    for i in se:
        # print(i,values_counts[i])
        ex += i*(float(values_counts[i]/count))
    ex = round(ex,2)
    return ex

if __name__ == '__main__':
    li = [5,5,5,5,4,1,2,3]
    avg = sum(li)/len(li)
    print(avg)
    va = var(li,avg)
    print(va)
    ex = exp(li)
    print(ex)