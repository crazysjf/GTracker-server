# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.test import TestCase

# Create your tests here.

a = [None, None, None]


def gen_diff(a):
    '''
    计算数组a的差分并返回。
    a中允许有None存在.
    返回数组的长度比a的长度小1。
    假设返回值为r:
    如果a[i] == None, 则r[i] = None；
    如果a[i] != None，则r[i] = a[i]和最近一个非空值的差。
    如果a[0] == None则当0处理

    [1, 2, 3]    => [1, 1]
    [1, None, 3] => [None, 2]
    [None, 2, 3] => [2, 1]
    [None, None, 3] => [None, 3]
    '''
    r = [None] * (len(a) - 1)
    last_unnone = 0 if a[0] == None else a[0]  # 最近一个非None值
    for i in range(1, len(a)):
        if a[i] == None:
            r[i - 1] = None
        else:
            if a[i - 1] == None:
                r[i - 1] = a[i] - last_unnone
            else:
                r[i - 1] = a[i] - a[i - 1]
            last_unnone = a[i]
    return r


print gen_diff(a)