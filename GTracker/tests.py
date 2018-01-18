# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.test import TestCase

# Create your tests here.

a = [1,None,3]


def gen_diff(a):
    '''
    计算数组a的差分并返回。
    a中允许有None存在。
    返回数组的长度比a的长度小1。
    '''
    def remove_none(a):
        '''去掉数组a里面的None：如果第一个值为None，则替换为0，如果不是第一个值为None，则替换为结果数组里面的前一个值'''
        r = [0] * len(a)
        for i in range(0, len(a)):
            if a[i] == None:
                 r[i] = 0 if i == 0 else r[i-1]
            else:
                r[i] = a[i]
        return r
    b = remove_none(a)
    c = [b[i] - b[i-1] for i,x in enumerate(b) if i > 0]
    return c


print gen_diff(a)