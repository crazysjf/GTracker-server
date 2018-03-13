# -*- coding: utf-8 -*-
# 店侦探爬虫
# 按店铺分类的宝贝销量列表：左侧面板宝贝分析 => 宝贝列表
# 导出按钮的链接例子：https://www.dianzhentan.com/member/items/all/73414042/?t=all&act=out&d=2018-01-01
# 格式应该为：https://www.dianzhentan.com/member/items/all/<店铺ID>?/t=all&act=out&d=<日期>

import base64
import os
import random
import signal
import sys
import time
#import winsound
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
from urlparse import urlparse

from crawler.db import db, csv_processor
from crawler.misc.constants import *
import pickle
import urllib2

dir = os.path.dirname(os.path.abspath(__file__))
COOKIE_FILE                 = os.path.join(dir, "cookies.pkl")
NEED_LOG_IN_FLAG_FILE       = os.path.join(dir, ".need_log_in")
CSV_DIR                     = os.path.join(dir, 'csv/')

class DztCrawler:
    '''
    爬虫实例。
    用法：
    c = DztCrawler()
    if c.need_log_in()
        # 获取验证码
        c.log_in()
    c.crawl_shops()
    
    '''
    @staticmethod
    def set_need_log_in_flag(f):
        if f:
            open(NEED_LOG_IN_FLAG_FILE, 'w').close()
        else:
            try:
                os.remove(NEED_LOG_IN_FLAG_FILE)
            except:
                pass


    @staticmethod
    def need_log_in_flag():
        return os.path.exists(NEED_LOG_IN_FLAG_FILE)


    def __init__(self):
        #driver = webdriver.PhantomJS()
        self.driver = webdriver.Chrome()
        # 设置cookie。设置之前先必须get一个dummy page
        self.driver.get(ERROR_404_URL)
        self.load_cookies()

    def __del__(self):
        self.finish()


    def need_log_in(self):
        self.driver.get(SHOP_LIST_URL)
        if u"用户登陆" in self.driver.title:
            self.set_need_log_in_flag(True)
            return True
        else:
            self.set_need_log_in_flag(False)
            return False


    def log_in(self, captcha=""):
        '''
        登录。成功返回True，失败返回False
        :param captcha: 
        :return: 
        '''
        driver = self.driver

        if not DztCrawler._is_same_path(driver.current_url, LOG_IN_URL):
            driver.get(LOG_IN_URL)

        ele = driver.find_elements_by_css_selector('input#username')[0]
        ele.clear()
        ele.send_keys(USER_NAME)

        ele = driver.find_elements_by_css_selector('input#password')[0]
        ele.clear()
        ele.send_keys(PASSWORD)

        ele = driver.find_elements_by_css_selector('input#validatecode')[0]
        ele.clear()
        ele.send_keys(captcha)

        ele.send_keys(Keys.RETURN)

        cnt = 0
        while cnt < 20:
            cnt += 1
            if u"用户登陆" in self.driver.title:
                time.sleep(1)
            else:
                self.dump_cookies()
                return True
        return False

    def get_captcha(self):
        '''获取验证码，成功返回验证码jpeg句柄，如下保存：
                    with open(r"captcha.jpg", 'wb') as f:
                        f.write(base64.b64decode(img_captcha_base64))
            失败返回None.'''
        driver = self.driver
        if not DztCrawler._is_same_path(driver.current_url, LOG_IN_URL):
            driver.get(LOG_IN_URL)

        if u"用户登陆" in driver.title:
            # find the captcha element
            ele_captcha = driver.find_elements_by_css_selector("div#form_group_validatecode div.input-group div.input-group-addon img")[0]
            img_captcha_base64 = driver.execute_async_script("""
                var ele = arguments[0], callback = arguments[1];
                ele.addEventListener('load', function fn(){
                  ele.removeEventListener('load', fn, false);
                  var cnv = document.createElement('canvas');
                  cnv.width = this.width; cnv.height = this.height;
                  cnv.getContext('2d').drawImage(this, 0, 0);
                  callback(cnv.toDataURL('image/jpeg').substring(22));
                }, false);
                ele.dispatchEvent(new Event('load'));
                """, ele_captcha)
            return img_captcha_base64
        else:
            return None

    def finish(self):
        self.dump_cookies()
        self.driver.quit()

    def crawl_shops(self, shops):
        driver = self.driver
        eList = driver.find_elements_by_css_selector("table#shop-list-table tbody tr")

        shops = []
        for e in eList:
            shop_id = e.get_attribute('data-shopid')
            a = e.find_element_by_css_selector('td.shop-name span a')
            link =  a.get_attribute('href')
            name =  a.text
            shops.append((name, link, shop_id))

        db.update_shops(shops)


    @staticmethod
    def _is_same_path(p1, p2):
        '''
        判断两个url是不是同一个地址。
        有时候在login页面的时候，url为如下形式：
        https://www.dianzhentan.com/base/?next=https%3A%2F%2Fwww.dianzhentan.com%2Fmember%2F
        需要判断上面的url和下面的url是不是同一个页面：
        https://www.dianzhentan.com/base/
        '''
        ps1 = urlparse(p1)
        ps2 = urlparse(p2)
        if ps1.netloc == ps2.netloc and  ps1.path == ps2.path:
            return True
        else:
            return False


    CSV_DIR = 'csv/'
    file_url_pattern = DZT_BASE_URL + 'member/items/all/%s/?t=all&act=out&d=%s'
    def download_a_csv(self, shop_id, date_str):
        '''下载单个文件。调用的时候必须保证登录成功。
        成功返回文件的绝对路径。
        失败返回None。
        data_str: 日期，形式：yyyy-mm-dd，必须要用字符串表示，否则无法通过rpc传输'''
        driver = self.driver
        cookies = [item["name"] + "=" + item["value"] for item in driver.get_cookies()]
        cookiestr = ';'.join(item for item in cookies)

        file_url = self.file_url_pattern % (shop_id, date_str)
        headers = {'cookie':cookiestr}
        req = urllib2.Request(file_url, headers = headers)
        try:
            response = urllib2.urlopen(req)
            text = response.read()

            file_name = CSV_DIR + shop_id + '-' + date_str + '.csv'
            fd = open(file_name, 'w')
            fd.write(text)
            fd.close()
            print '###get %s success!!' % file_name
            return os.path.join(dir, file_name)
        except:
            print("Unexpected error:", sys.exc_info()[0])
            raise

    def load_cookies(self):
        if os.path.exists(COOKIE_FILE):
            cookies = pickle.load(open(COOKIE_FILE, "rb"))
            for cookie in cookies:
                self.driver.add_cookie(cookie)

    # 保存cookie
    def dump_cookies(self):
        c = self.driver.get_cookies()
        pickle.dump(c, open(COOKIE_FILE, "wb"))

    def _print_cookies(self):
        cookie = "; ".join([item["name"] + "=" + item["value"] + "\n" for item in self.driver.get_cookies()])
        print cookie

    def console(self):
        while True:
            s = raw_input("Enter your input: ")
            l = s.split()
            c = l[0]    # 命令
            p1 = None
            if len(l) > 1:
                p1 = l[1]   # 参数1

            if c == "p":
                from urlparse import urlparse
                print urlparse(self.driver.current_url)
                #print_cookies(driver)
            if c == 'd':
                print self.download_a_csv('63359486', '2017-12-23')
            if c == 'l':
                csv_processor.download_files(driver)
            if c == 'i':
                print self.log_in(p1)
            if c == "q":
                break

if __name__ == "__main__":
    c = DztCrawler()
    if c.need_log_in():
        b64 = c.get_captcha()
        with open(r"captcha.jpg", 'wb') as f:
            f.write(base64.b64decode(b64))
    c.console()
