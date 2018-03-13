# -*- coding: utf-8 -*-
import urllib2
import re


def crawl_main_pic(good_id):
    '''
    爬取主图链接
    :param good_id:
    :return:
    '''

    url_base = 'https://item.taobao.com/item.htm?id='
    url = url_base + good_id
    #
    # 获取的html如下：需要的是里面的auctionImage行
    # disableAddToCart  : !true,
    #
    # auctionImages    : ["//gd1.alicdn.com/imgextra/i2/20868741/TB2GvfHiDnI8KJjSszbXXb4KFXa_!!20868741.jpg","//gd4.alicdn.com/imgextra/i4/20868741/TB1BMjke22H8KJjy1zkXXXr7pXa_!!0-item_pic.jpg","//gd4.alicdn.com/imgextra/i4/20868741/TB2rULbe4rI8KJjy0FpXXb5hVXa_!!20868741.jpg","//gd3.alicdn.com/imgextra/i3/20868741/TB2jVmSe9YH8KJjSspdXXcRgVXa_!!20868741.jpg","//gd1.alicdn.com/imgextra/i1/20868741/TB2oxELe3fH8KJjy1zcXXcTzpXa_!!20868741.jpg","//gd2.alicdn.com/imgextra/i2/20868741/TB17yOTe4TI8KJjSspiXXbM4FXa_!!0-item_pic.jpg"]
    #
    # mode        : 0,

    try:
        req = urllib2.Request(url)
        response = urllib2.urlopen(req)
        html = response.read()

        p = re.compile(r'^.*auctionImages.*:.*\[(.*)\].*$', flags=re.M)
        m = p.search(html)
        if m != None:
            s = m.group(
                1)  # "//gd1.alicdn.com/imgextra/i2/20868741/TB2GvfHiDnI8KJjSszbXXb4KFXa_!!20868741.jpg","//gd4.alicdn.com/imgextra/i4/20868741/TB1BMjke22H8KJjy1zkXXXr7pXa_!!0-item_pic.jpg","//gd4.alicdn.com/imgextra/i4/20868741/TB2rULbe4rI8KJjy0FpXXb5hVXa_!!20868741.jpg","//gd3.alicdn.com/imgextra/i3/20868741/TB2jVmSe9YH8KJjSspdXXcRgVXa_!!20868741.jpg","//gd1.alicdn.com/imgextra/i1/20868741/TB2oxELe3fH8KJjy1zcXXcTzpXa_!!20868741.jpg","//gd2.alicdn.com/imgextra/i2/20868741/TB17yOTe4TI8KJjSspiXXbM4FXa_!!0-item_pic.jpg"
            t = s.split(',')
            print t[0]
            t1 = re.match('"(.*)"', t[0]).group(1)  # 去掉两边双引号
            return 'http:' + t1

        else:
            return None

    except:
        raise
