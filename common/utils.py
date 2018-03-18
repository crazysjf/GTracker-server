# -*- coding: utf-8 -*-


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


def gen_diff2(a):
    '''
    版本2
    计算数组a的差分并返回。
    a中允许有None存在。如果a[i] == None, 则a[i] = a[i+1]
    如果全部为None，则全部作为0.
    返回数组的长度比a的长度小1。
    假设返回值为r:

    [1, 2, 3]    => [1, 1]
    [1, None, 3] => [2, 0]
    [None, 2, 3] => [0, 1]
    [None, None, 3] => [0, 3]
    [None, None, None] => [0, 0, 0]

    '''
    r = [None] * (len(a) - 1)

    for i in range(len(a) - 1, -1, -1):
        if a[i] != None:
            # 把后部为None的填充为最近的非None值
            for j in range(i + 1, len(a)):
                a[j] = a[i]
            break

        if i == 0 and a[i] == None:
            # 整个数组全部为None
            for j in range(0, len(a)):
                a[j] = 0

    for i in range(len(a) - 1, -1, -1):
        if i != len(a) - 1 and a[i] == None:
            a[i] = a[i + 1]

    for i in range(1, len(a)):
        # if a[i] == None and a[i-1] == None:
        #     print r
        r[i - 1] = a[i] - a[i - 1]
    return r

from datetime import datetime
def str_2_date(s):
    '''
    把形如'2018-03-12'的字符串转成date对象
    :param s:
    :return:
    '''
    _s = s.split()[0] # 处理"2018-03-21 18:23:33"之类的带时间的参数
    return datetime.strptime(_s, '%Y-%m-%d').date()