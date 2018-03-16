# -*- coding: utf-8 -*-
import sqlite3 as lite
from datetime import date, timedelta
from crawler.misc import constants
import os
from common.utils import gen_diff2, str_2_date
from enum import Enum

dir = os.path.dirname(os.path.abspath(__file__))

# 默认日期范围
START_DATE = date.today() - timedelta(constants.DATE_RANGE)
END_DATE   = date.today() - timedelta(1)

class Singleton(object):
    _instance = None
    def __new__(cls, *args, **kw):
        if not cls._instance:
            cls._instance = super(Singleton, cls).__new__(cls, *args, **kw)
        return cls._instance

# 排序方法
class SortMethod:
    BY_SUM_SALES_3  = 1
    BY_SUM_SALES_7  = 2
    BY_SNR          = 3
    BY_CREATE       = 4

    param_str_dict = {
        BY_SUM_SALES_3: ["SumSales3",   '最近3天销量'],
        BY_SUM_SALES_7: ["SumSales7",   '最近7天销量'],
        BY_SNR:         ["snr",         '销新比'],
        BY_CREATE:      ["create",      '创建时间']
    }


    @staticmethod
    def desc(p):
        '''中文描述'''
        return SortMethod.param_str_dict[p][1]


    @staticmethod
    def param_str(s):
        '''转为http请求用的参数字符串'''
        return SortMethod.param_str_dict[s][0]


    @staticmethod
    def param_str_2_sort_method(s):
        '''参数字符串转SortMethod'''
        for k in SortMethod.param_str_dict.keys():
            if SortMethod.param_str_dict[k][0] == s:
                return k
        return None


    @staticmethod
    def all():
        return SortMethod.param_str_dict.keys()


class DB(Singleton):
    '''
    用法：
    db=DB() # 获取单例
    用db操作
    db.commit() # 需要提交时调用
    db.finish() # 需要显式关闭数据库时使用
    '''
    db_name = os.path.join(dir, "data.db")


    def __init__(self, db = None):
        '''初始化
        db_file:db文件，如果不指定则为当前目录下的data.db
        '''
        if db != None:
            self.db_name = db
        self.con = lite.connect(self.db_name)
        self.cur = self.con.cursor()

    def __del__(self):
        self.finish()

    def commit(self):
        self.con.commit()

    def finish(self):
        self.con.commit()
        self.con.close()


    def update_shops(self, shops):
        '''
        更新店铺信息，对于已存在的店铺不进行处理
        shops格式:((店铺id，名称))
        所有在shops里面存在的店铺即为当前被监控的店铺
        '''
        self.cur.execute("update Shops set active=0") # 所有店铺active清空
        for shop in shops:
            #print shop[2]
            self.cur.execute("SELECT COUNT(*) FROM Shops WHERE ShopId=?", (shop[0],))
            # 如果记录不存在就插入
            if self.cur.fetchone()[0] == 0:
                self.cur.execute("INSERT INTO Shops(ShopId, Name, active) VALUES(?,?,?)", (shop[0], shop[1], True))
            else:
                self.cur.execute("update Shops set Name=?, active=? where ShopId=?", (shop[1], True, shop[0]))



    def get_all_shops(self):
        self.cur.execute("SELECT name, shopid FROM Shops where active=1")
        rows = self.cur.fetchall()

        return rows

    def get_shop_name(self, sid):
        self.cur.execute("SELECT name FROM Shops where shopid=?", (sid,))
        rows = self.cur.fetchall()
        return rows[0][0]


    def good_exists(self, good_id):
        self.cur.execute('select * from goods where GoodId = ?', (good_id,))
        if self.cur.fetchone() == None:
            return False
        else:
            return True

    def get_good_info(self, good_id):
        self.cur.execute('select Name, id, CreationDate, mainPic, shopid from goods where GoodId = ?', (good_id,))
        r = self.cur.fetchone()
        return r

    def get_goods_nr(self, shop_id = None):
        sql = 'select count(*) from goods where active=1'
        if shop_id != None:
            sql = sql + " and ShopId=%s" % shop_id
        self.cur.execute(sql)
        r = self.cur.fetchall()
        return r[0][0]


    def get_goods(self, shop_id = None, sort=SortMethod.BY_SNR, offset=0, limit=None):
        sql = 'select goodid, Name, MainPic, CreationDate from goods where active=1'
        if shop_id != None:
            sql = sql + " and ShopId=%s" % shop_id

        order_by_dict = {
            SortMethod.BY_SUM_SALES_3:'SumSales3',
            SortMethod.BY_SUM_SALES_7:'SumSales7',
            SortMethod.BY_SNR: "SNR",
            SortMethod.BY_CREATE:"CreationDate"
        }
        order_by = order_by_dict[sort]

        sql = sql + " order by " + order_by + " DESC"
        if limit != None:
            sql = sql + " limit " + limit + ' offset ' + offset

        self.cur.execute(sql)
        r = self.cur.fetchall()
        return r


    def get_all_goods_with_empty_main_pic(self):
        self.cur.execute('select goodid from goods where mainpic isNull')
        r = self.cur.fetchall()
        return r


    def good_update_main_pic(self, good_id, main_pic):
        self.cur.execute('update goods set mainPic=? where goodId=?', (main_pic, good_id))



    def insert_good(self, good):
        '''
        插入商品
        :param good: 格式：(GoodId, ShopId, Name, CreationDate，MainPic)
        :return: 
        '''
        self.cur.execute("INSERT INTO Goods(GoodId, ShopId, Name, CreationDate, MainPic, active) VALUES(?,?,?,?,?,?)",
                         good + (1,))

    def record_exists(self, good_id, date):
        '''判断某店铺某天的数据是否存在'''
        self.cur.execute("select * from records where GoodId=? and date=?", (good_id, date))
        if self.cur.fetchone() == None:
            return False
        else:
            return True

    def insert_record(self, r):
        self.cur.execute("INSERT INTO Records(date, GoodId, sales_30, bid30, fav_cnt, view_cnt, review_cnt) VALUES(?,?,?,?,?,?,?)", r)


    def get_records(self, date, good_id = None):
        param = [date]
        sql = 'select * from records where date=?'
        if good_id != None:
            sql += ' and GoodId=?'
            param.append(good_id)
        self.cur.execute(sql, param)
        r = self.cur.fetchall()
        return r

    def get_records2(self, date, shop_id):
        sql = '''select r.*, s.Name from Records r, Goods g, Shops s where
                    r.GoodId = g.GoodId and
                    g.ShopId = s.ShopId and
                    r.date = ? and
                    s.ShopId = ?'''
        self.cur.execute(sql, (date, shop_id))
        r = self.cur.fetchall()
        return r


    def get_records_with_good_id_in_date_range(self, gid, start_date, end_date):
        sql = '''select r.date, r.bid30 from Records r where
                    r.GoodId = ? and
                    r.date >= ? and
                    r.date <= ?'''
        self.cur.execute(sql, (gid, start_date, end_date))
        r = self.cur.fetchall()
        return r


    def get_records_with_shop_id_in_date_range(self, shop_id, start_date=None, end_date=None):
        '''
        
        :param shop_id: 
        :param start_date: 开始日期，不指定则为30天前
        :param end_date: 结束日期，不指定则为当天
        :return: [good_id, r.date, r.bid30
        '''
        if start_date == None:
            start_date = START_DATE

        if end_date == None:
            end_date = END_DATE

        sql = '''select r.GoodId, r.date, r.bid30, g.name from Records r, Goods g, Shops s where
                    r.GoodId = g.GoodId and
                    g.ShopId = s.ShopId and
                    s.ShopId = ? and
                    r.date >= ? and
                    r.date <= ? and
                    g.active = 1'''
        self.cur.execute(sql, (shop_id, start_date, end_date))
        r = self.cur.fetchall()
        return r

    def all_shops(self):
        sql = '''select ShopId, Name, Link from Shops'''
        self.cur.execute(sql)
        r = self.cur.fetchall()
        return r


    def shops_needed_to_crawl(self, date_range = 7):
        '''判断哪些店铺的哪些日期需要爬取。如果某个店铺在某天一条记录也没有就被判定为需要爬取
        返回格式：{ shop_id1: [date1, date2,...], 
                    shop_id2: [date3, date4,...],...}

        date_range: 从昨天开始往前追溯多少天。通过API抓取只能抓最近7天的
        该函数执行需要约2分钟
         '''
        _all_shops = self.all_shops()
        result = {}
        for (shop_id, _, _) in _all_shops:
            for d in range(0, date_range):
                date = END_DATE - timedelta(d)
                sql = '''select count(*) from Records r, Goods g, Shops s where
                            r.GoodId = g.GoodId and
                            g.ShopId = s.ShopId and
                            g.ShopId = ? and
                            r.date = ?'''
                self.cur.execute(sql, (shop_id, date))
                r = self.cur.fetchall()[0]
                if r[0] == 0:
                    #print shop_id, date
                    if result.has_key(shop_id):
                        result[shop_id].append(date)
                    else:
                        result[shop_id] = [date]
        return result

    def update_goods_and_records_for_shop(self, shop_id, date, shop_data):
        '''
        :param : shop_data: 至少包含以下键：[{good_id:商品id, creation_time:创建时间, title:标题, main_pic:主图sales_30:30天付款人数，bid30: 30天销量（关键数据）}, ...]
                date: 数据的日期，datetime.date对象
        :return:
        '''

        self.cur.execute("update goods set active=0 where shopid=?", (shop_id,)) # 店铺所有商品active清空

        for d in shop_data:
            try:
                # if not db.record_exists(good_id, date):
                r = (date, d['good_id'],
                     d['sales_30'] if d['sales_30'] else 0,
                     d['bid30'] if d['bid30'] else 0,
                     0, 0, 0)
                #用于更新bid30，仅临时使用
                #self.cur.execute("update records set bid30=? where goodid=? and date=?", (d['bid30'], d['good_id'], date))
                self.insert_record(r)
            except lite.IntegrityError as e:
                pass

            # 重复数据不用每次判断，直接插入，可以大幅提高性能
            # 如果重复会抛出IntegrityError异常，直接忽略即可。
            try:
                #r = self.calc_indexes_for_good(d['good_id'])
                g = (d['good_id'], shop_id, d['title'], d['creation_time'],d['main_pic'])

                self.cur.execute("update goods set name=?, creationDate=?, mainPic=?, active=1 where goodid=?",
                                 g[2:]+ (g[0],)) # 如果商品存在则更新active，不存在无效果
                #(GoodId, ShopId, Name, CreationDate，MainPic)
                self.insert_good(g) # 如果商品存在进入抛出异常，不存在进行插入
            except lite.IntegrityError as e:
                pass

    def update_params_for_goods(self, shop_id = None):
        '''
        更新所有商品的各个指标。
        如果指定了shop_id，则仅更新指定shop的商品
        返回：{sum_sales_7: 7天销量和， sum_sales_3: 3天销量和， snr: 销新比'}
        '''
        gids = self.get_goods(shop_id)
        total = len(gids)
        cnt = 0
        print "begin to update indexes for %d goods..." % total
        for _gid in gids:
            gid = _gid[0] #_gid是一个tuple

            date_range = 8  # 取出近8天数据
            start_date = date.today() - timedelta(date_range)
            end_date = date.today() - timedelta(1)
            rs = self.get_records_with_good_id_in_date_range(gid, start_date, end_date)

            a = [None] * date_range
            for r in rs:
                idx = (str_2_date(r[0]) - start_date).days
                a[idx] = r[1]
            diff = gen_diff2(a)
            sum_sales_7 = diff[0] + diff[1] + diff[2] + diff[3] + diff[4] + diff[5] + diff[6]
            sum_sales_3 = diff[4] + diff[5] + diff[6]

            # 从返回的结果中找出最后一天的30天销量
            latest_bid_30 = 0
            t = filter(lambda x: str_2_date(x[0]) == end_date, rs)
            if len(t) != 0:
                latest_bid30 = t[0][1]
            # 商品的创建时间
            create = self.get_good_info(gid)[2]
            days =  (end_date - str_2_date(create.split()[0])).days
            if days <= 0:
                days = 1 # +1避免出现除0错误，有时候days算出来为负数，原因不明

            snr = float(latest_bid30) / days

            self.cur.execute("update Goods set SumSales7=?, SumSales3=?, snr=? where GoodId=?",
                             (sum_sales_7, sum_sales_3, snr, gid))
            cnt = cnt + 1
            print "updated %s, %d, %d\%%" % (gid, cnt, float(cnt*100)/total)

        self.commit()
        print "finished updating indexes ..."


if __name__ == '__main__':
    # db = DB()
    # gids = db.get_all_active_goods()
    # print gids
    print DB().get_goods_nr('33495993')