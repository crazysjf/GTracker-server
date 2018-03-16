# -*- coding: utf-8 -*-
'''
通过店侦探的API来爬取数据
'''
from crawler.db.db import DB
from datetime import datetime, date, timedelta
import urllib2
import json

API_KEY='333a23d3124a8bf2c77a0703bbc3a590'
BASE_URL  = 'https://www.dianzhentan.com/api/'
MYSHOPS_URL = BASE_URL + 'myshops/' + API_KEY + "/"


def gen_items_url(shop_id, date):
    '根据shop_id和date生成items的url'
    p =  BASE_URL + 'items/' + API_KEY + '/?shopid=%s&d=%s'
    return p % (shop_id, date)


def _update_one_shop(sid, d):
    '''
    更新某个日期指定店铺的记录数据。
    :param sid:
    :param d:
    :return:
    '''
    db = DB()
    url = gen_items_url(sid, str(d))
    # 每天仅限调用10次
    s = urllib2.urlopen(url).read()
    # s = open('shopid=33003356&d=2018-03-06.txt').read()
    # print sid
    o = json.loads(s)

    # print len(o['data'])
    def _trans(x):
        y = {}
        # {good_id:商品id, creation_time:创建时间, title:标题, sales_30:30天销量}
        y['good_id'] = x['pid']
        y['creation_time'] = x['create']
        y['title'] = x['title']
        y['sales_30'] = x['per30'] # 应该是宝贝在搜索列表里面的时候所显示的付款人数
        y['bid30']    = x['bid30'] # 应该是手机端宝贝详情页的月销量，销量统计应该以这个为准
        y['main_pic'] = x['pics'][0]
        return y

    shop_data = map(_trans, o['data'])
    db.update_goods_and_records_for_shop(sid, d, shop_data)
    db.commit()

def _update_shops_info():
    # 接口每天限制调用10次
    s = urllib2.urlopen(MYSHOPS_URL).read()
    #s = '''{"data":[{"nick":"\u25ce\u599e\u599e\u25ce","title":"\u599e\u599e\u65fa\u94fa\u5feb\u65f6\u5c1a\u6f6e\u6d41\u5973\u88c5","sid":33003356},{"nick":"\u897f\u897f\u5c0f\u53ef","title":"\u897f\u897f\u5c0f\u53ef \u6f6e\u54c1\u5973\u88c5","sid":33290163},{"nick":"aiaallai","title":"\u8ff7\u604b\u5973\u88c5","sid":33322132},{"nick":"peggy_cheung","title":"\u8783\u87f9\u5df772\u53f7\u65f6\u5c1a\u5973\u88c5","sid":33494484},{"nick":"xvsh_007","title":"\u6c90\u4e43\u8863\u5973\u88c5","sid":33495993},{"nick":"ztxtidt","title":"\u54da\u5566 \u5973\u88c5","sid":33531012},{"nick":"\u90ce\u6c88\u5251","title":"Ekool\u8863\u5e93\u5bb6","sid":33981650},{"nick":"\u5c0f\u53ef\u7231\u732a\u5356\u70df\u8bb0","title":"4\u53f7\u623f\u539f\u521b\u670d\u9970","sid":34164773},{"nick":"\u65e5\u97e9\u5973\u88c5\u4e13\u5356","title":"\u897f\u74dc\u5bb6\u5feb\u65f6\u5c1a\u6f6e\u5e97","sid":34283080},{"nick":"\u5fae\u98ce\u6e05\u629a","title":"\u8587\u8587\u7cbe\u54c1\u5973\u88c5\u5b9e\u62cd\u5e97","sid":34497484},{"nick":"wuyasd","title":"\u53ef\u4eba\u65f6\u5c1a\u670d\u9970\u4f4e\u4ef7\u4f18\u8d28","sid":34757726},{"nick":"\u4e1c\u5ddd\u5d0e\u753a","title":"\u4e1c\u5ddd\u5d0e\u753a\u6279\u53d1\u5e97","sid":35023116},{"nick":"\u8d38\u6613\u70df\u884c","title":"\u756a\u8304\u7537\u53cb\u7537\u88c5","sid":35069805},{"nick":"290476779yy","title":"6\u5ea6 6Du Shop\u5973\u88c5","sid":35204970},{"nick":"milingzhi","title":"Hello MLZ \u97e9\u56fd\u590d\u53e4\u5c0f\u6e05\u65b0\u81ea\u5236\u7f8e\u8863","sid":35271361},{"nick":"\u4e1c\u65b9\u6d41\u884c\u524d\u7ebf","title":"EGGKA","sid":35329736},{"nick":"\u778c\u7761\u4e0e\u6795\u59341018","title":"SleepyBunny\u778c\u7761\u5154","sid":35413636},{"nick":"preety\u552f","title":"\u552f\u5bb6\u5e97\u94fa \u54c1\u8d28\u54c1\u4f4d\u4f18\u96c5\u72ec\u7279\u5927\u91cf\u4e0a\u65b0\u4e2d","sid":35441199},{"nick":"weiwei_1221","title":"weiwei\u7f8e\u8863","sid":35647715},{"nick":"\u5c0f\u756a\u83040506","title":"\u5c0f\u756a\u8304 \u5b9a\u5236","sid":35724438},{"nick":"eney503","title":"\u4e54\u5b89\u5bb6","sid":35774213},{"nick":"hym134225","title":"Dreamyshow\u68a6\u68a6\u5bb6\u5973\u88c5","sid":36013903},{"nick":"zjforeverxxxx","title":"JTO\u5bb6 JTOLADY\u6f6e\u6d41\u5973\u88c5","sid":36084882},{"nick":"\u9ebb\u5c06\u62fc\u56fe","title":"ITS FOCUS\u5973\u88c5 \u4e3b\u6bdb\u9488\u7ec7\u7c7b","sid":36096598},{"nick":"lv_kiki","title":"\u5c0fKK\u7f8e\u8863xiaokk","sid":36252086},{"nick":"jun03","title":"\u5c0f\u54f2 \u65f6\u5c1a\u642d\u914d\u5973\u88c5","sid":36342141},{"nick":"luotian2010","title":"\u4e3d\u59ff\u5973\u88c5LIZZYSHOP","sid":36598711},{"nick":"173\u5f53\u94fa","title":"173\u5f53\u94fa \u91d1\u51a0","sid":36604307},{"nick":"\u5c0f\u5b9c2009","title":"YESWOMEN \u5c0f\u5b9c\u5b9a\u5236","sid":36948107},{"nick":"ly86734072","title":"PURISM\u5973\u88c5","sid":37095997},{"nick":"yingxilin0405","title":"SASA\u5c0f\u59d0\u81ea\u5236","sid":57122507},{"nick":"wangbin895","title":"MOMO \u83ab\u9ed8\u7f8e\u8863","sid":57698939},{"nick":"chengzw2008","title":"Mixmind\u5973\u88c5","sid":57742470},{"nick":"\u521d\u89c1_daisy","title":"first sight studio \u521d\u89c1\u5bb6","sid":58195669},{"nick":"\u559c\u78a72009","title":"\u559c\u78a72009","sid":58340795},{"nick":"\u9047\u89c1_\u6696","title":"\u6c5f\u6696JN warmo","sid":58633820},{"nick":"\u62d4\u841d\u535c\u7684\u5c0f\u8001\u9f20","title":"\u62d4\u841d\u535c\u7684\u5c0f\u8001\u9f20\u5973\u88c5","sid":58772023},{"nick":"fashionxiaoyin","title":"STYLEYINZ\u5c0f\u94f6\u5b50\u6b27\u7f8e\u8303\u5b9a\u5236\u5973\u88c5","sid":58796011},{"nick":"gaigaizi_59","title":"Gaigaizi\u76d6\u76d6\u5b50","sid":58940708},{"nick":"\u541b\u541b\u5c4b2009","title":"\u541b\u541b\u5c4b2009","sid":58947565},{"nick":"\u745e\u4e3d\u7cbe\u54c1\u4f53\u9a8c\u5e97","title":"RPIN\u745e\u54c1\u97e9\u7248\u65e5\u7cfb\u5973\u88c5","sid":58954390},{"nick":"kunyli","title":"\u78a7\u51e1\u5bb6\u5973\u88c5","sid":59259315},{"nick":"\u80e1\u65b9\u82f1","title":"\u8513\u5ef6\u65f6\u5c1a\u6f6e\u6d41\u5973\u88c5","sid":59382693},{"nick":"\u90d1\u660e\u5fe02008","title":"\u9ed1\u725b\u5976\u5c11\u5973 Miss Zhang","sid":59605831},{"nick":"\u5c0f\u51b0649999","title":"FAIRYPAN \u5c0f\u51b0\u5b9a\u5236\u5973\u88c5","sid":59640715},{"nick":"\u5c0f\u5c0f\u6dd80704","title":"K2KCollections","sid":59683356},{"nick":"\u8ff7\u604boo\u515c\u515coo","title":"\u62ff\u5c0f\u9a6c","sid":60334039},{"nick":"\u8863\u5f69\u7f24\u7eb7shop","title":"\u5c0fC\u5bb6\u97e9\u7248\u7f8e\u8863\u5b9e\u62cd\u5e97","sid":60441651},{"nick":"madoujia","title":"\u4e8eMOMO\u6f6e\u6d41\u5973\u88c5","sid":60552065},{"nick":"\u6ee8\u5d0e\u6b6577","title":"\u9ca4\u9c7c\u5c0f\u59d0","sid":60739775},{"nick":"\u81ea\u5df1\u548c\u81ea\u5df1\u73a9zl","title":"\u7f8a\u57ce\u6545\u4e8b\u5bb6cantonstory","sid":60785920},{"nick":"\u6c99\u6f0f\u7684\u821e\u8e4855208","title":"GAGAI\u6781\u7b80\u5b9a\u5236","sid":61107280},{"nick":"\u9b54\u8863\u76d2\u5b50","title":"\u9b54\u8863\u5b9d\u8d1dMOYIBABY\u5973\u88c5","sid":61275216},{"nick":"xiaona620","title":"\u5a1c\u6837\u5e74\u534e\u97e9\u56fd\u54c1\u8d28","sid":61714176},{"nick":"ygywxt","title":"MISS LUCY\u9732\u897f\u5bb6\u5973\u88c5 \u6bcf\u65e5\u4e0a\u65b0","sid":62028840},{"nick":"\u8096\u73b211","title":"\u6728\u68c9\u82b1\u53c8\u5f00\u4e86","sid":63292300},{"nick":"\u679c\u679c\u4e00\u5973\u4eba","title":"\u679c\u679c\u5bb6  GG WOMEN\u5973\u88c5\u6f6e\u5e97\u5468\u4e00\u4e0a\u65b0","sid":63351762},{"nick":"mingming7178","title":"MingMing\u660e\u660e\u9b54\u8c46","sid":63359486},{"nick":"fjw5528","title":"\u5927\u96ef\u5bb6 DAWEN\u5973\u88c5","sid":63538640},{"nick":"\u9c9c\u6ef4\u9017\u9017","title":"\u4e86\u4e0d\u8d77\u7684\u5973\u5b69","sid":64960781},{"nick":"\u53f6\u67ab\u7fce\u65d7\u8230\u5e97","title":"\u53f6\u67ab\u7fce\u65d7\u8230\u5e97","sid":65141335},{"nick":"\u4f9d\u827e\u7eaf","title":"\u5c0f\u57ce\u6545\u4e8b\u5bb6\u5973\u88c5\u6279\u53d1\u5e97","sid":65278127},{"nick":"lxq19841003","title":"\u4e94\u4ea9\u5c0f\u6751\u5feb\u65f6\u5c1a\u5973\u88c5","sid":65537265},{"nick":"wxpcute","title":"\u4e4c77 wu77style","sid":65547799},{"nick":"\u633d\u4e91\u5986","title":"\u5c0f\u8c37\u7c92\u5973\u88c5 YESIAMXIAOG","sid":65626181},{"nick":"\u7ea2\u989c\u77e5\u5df1everyone","title":"\u897f\u74dc\u5bb6\u6a59\u5b50 \u72ec\u5bb6\u5b9a\u5236 \u6f6e \u97e9\u7248 \u767e\u5206\u767e\u5b9e\u62cd cheny","sid":65660508},{"nick":"\u67e0\u6aac\u8349\u8336\u8bed","title":"\u67e0\u6aac\u8349\u5bb6\u5973\u88c5","sid":66241212},{"nick":"\u725b\u4ed4ks","title":"Honey House\u5b9e\u62cd\u5973\u88c5","sid":66250832},{"nick":"1992_shanainainai","title":"ibabyQ\u97e9\u7aef\u5236\u8863","sid":66602966},{"nick":"\u871c\u7cd6\u96e8\u7684\u8001\u677f","title":"\u871c\u7cd6\u96e8HoneyRain \u97e9\u56fd\u5408\u4f5c\u5e97 \u6bcf\u65e5\u4e0a\u65b0","sid":67146869},{"nick":"\u5c0f\u4e0d\u70b98798","title":"MG\u679c\u679c\u5b9a\u5236STUDIO","sid":68097667},{"nick":"mliam","title":"\u516b\u722a\u5a18\u5a18\u97e9\u7248\u65e5\u7cfb\u5973\u88c5","sid":68413008},{"nick":"\u73ca\u73ca\u5b9d\u8d1d0332008","title":"\u6797\u73ca\u73ca Sunny33\u5c0f\u8d85\u4eba","sid":68440633},{"nick":"\u8ff7\u604b\u4e0a\u516c\u4e3b","title":"\u8ff7\u604b\u4e0a\u516c\u4e3b\u5b9a\u5236\u5973\u88c5","sid":68673074},{"nick":"\u62b1\u5154\u5b50\u8ffd\u5927\u5954","title":"\u62b1\u5154\u5b50\u8ffd\u5927\u5954","sid":69019980},{"nick":"vivide\u5e97","title":"\u5c0f\u9896\u5bb6\u6bcf\u5468\u4e00\u5b9a\u671f\u4e0a\u65b0","sid":69345571},{"nick":"\u516c\u4e3b\u6615\u8587","title":"\u516c\u4e3b\u6615\u8587","sid":69436183},{"nick":"\u6b63\u70b9\u65f6\u5c1a\u5b85\u88c5","title":"\u767e\u5206\u7740\u8863","sid":69667879},{"nick":"\u94b1\u592b\u4eba209","title":"\u94b1\u592b\u4eba\u5bb6 \u96ea\u68a8\u5b9a\u5236","sid":69714396},{"nick":"\u767e\u601d\u57ce","title":"basein \u500d\u5fc3","sid":70432334},{"nick":"\u5c0f\u82f1chi","title":"\u6708\u7259\u57ce","sid":70523617},{"nick":"\u5c0f\u5b85\u5973\u5927\u8d2d\u7269","title":"\u5c0f\u5b85\u5973\u5927\u8d2d\u7269 xiaozhainv \u5c0f\u5b85\u5973\u5bb6 xiao zhai nv","sid":71007028},{"nick":"\u9b45\u4e3d\u4e1d888","title":"\u4e95\u8587\u5bb6 \u6f6e\u6d41\u5973\u88c5","sid":71089909},{"nick":"\u821e\u7b75\u67f3\u556c","title":"\u963f\u5357\u5bb6 ANJ Clothing\u5973\u88c5","sid":71123195},{"nick":"yezimo01","title":"ZIMO\u5bb6 \u5b9e\u62cd\u5973\u88c5","sid":71187136},{"nick":"\u7c73\u4e36mu","title":"\u5c0fV\u5bb6\u5973\u88c5 THATXIAOV","sid":71747560},{"nick":"\u6325\u970d\u7684\u6c14\u5019","title":"D JING \u5927\u9759\u5bb6 fashion\u5973\u88c5","sid":71852592},{"nick":"kenken1116","title":"BiBiQueen\u72ec\u5bb6\u5b9a\u5236","sid":71917038},{"nick":"\u6311\u5254\u7684\u5973\u90ce","title":"Picky Girl  \u97e9\u56fdulzzang\u5973\u88c5 \u6bcf\u65e5\u4e0a\u65b0","sid":72037804},{"nick":"long2942334","title":"\u97e9\u56fdBaby\u4e1c\u5927\u95e8\u5973\u88c5","sid":72849624},{"nick":"\u97e9\u8863\u4f1a","title":"\u97e9\u60d1\u5973\u88c5","sid":73025397},{"nick":"brisa520","title":"\u8611\u83c7\u5934\u9488\u7ec7","sid":73133083},{"nick":"\u9b45\u4f9d\u4e4b\u90fd","title":"KOKO HOUSE","sid":73163911},{"nick":"aim\u79c0","title":"Aim\u79c0 \u5b9a\u5236\u5973\u88c5","sid":73403857},{"nick":"teem111","title":"\u5341\u516d\u5df7\u5973\u88c5","sid":73414042},{"nick":"tb588405_2012","title":"AMJ\u7231\u529b\u9b54\u6212","sid":100168729},{"nick":"\u7a81\u7136\u597d\u60f3\u4f60_1234","title":"\u5b50\u58a8\u7cbe\u54c1\u574a","sid":100371107},{"nick":"chenfangxi1992","title":"\u8303\u897f\u897f \u5973\u88c5","sid":101179482},{"nick":"\u9495\u4eba\u4e00\u751f","title":"WF\u5b9a\u5236\u5de5\u5382","sid":101460112},{"nick":"hmin1122","title":"\u90fd\u5e02\u5973\u5b69 \u9ad8\u7aef\u670d\u9970","sid":101477518},{"nick":"\u5de6\u624b\u65c1\u8fb9\u4f60\u7684\u53f3\u624b","title":"\u90a3\u4e9b\u4e8b\u8863\u6a71","sid":101785619},{"nick":"\u6211\u662f\u7b28\u86cb333","title":"ZZhen \u73cd\u73cd\u5bb6","sid":101939615},{"nick":"\u54c6\u5566a\u68a6\u4e28","title":"DOR Collections","sid":102024431},{"nick":"\u6c5d\u4eba\u4e4b\u5bb6888","title":"\u5c0f\u5357\u5bb6 \u8f7b\u719f\u7cfb\u81ea\u5236","sid":102132035},{"nick":"77\u7740\u8863","title":"\u975e\u753a\u5feb\u65f6\u5c1a\u5973\u88c5","sid":102478935},{"nick":"\u6c49\u57ce\u5bb6","title":"A11 ELEVEN \u5b9a\u5236\u5973\u88c5","sid":102560443},{"nick":"\u68a6\u9732\u65e5\u8bb0","title":"\u68a6\u9732\u65e5\u8bb0\u65f6\u5c1a\u5973\u88c5","sid":102856969},{"nick":"\u8482\u62c9\u683c\u6155\u65d7\u8230\u5e97","title":"\u8482\u62c9\u683c\u6155\u65d7\u8230\u5e97","sid":103227817},{"nick":"qi900629","title":"\u5c0f\u4e03\u97e9\u88c5","sid":103460086},{"nick":"e\u83f2_\u83f2e","title":"\u5c0f\u83f2\u5bb6\u65b0\u6b3e\u6bcf\u65e5\u66f4\u65b0","sid":103684818},{"nick":"hanmeiren_mm","title":"\u827e\u683c\u8d1d\u5b9a\u5236","sid":105439071},{"nick":"\u6155\u83b2\u5a1c\u65d7\u8230\u5e97","title":"\u6155\u83b2\u5a1c\u65d7\u8230\u5e97","sid":105666009},{"nick":"\u621a\u7c73\u65d7\u8230\u5e97","title":"\u621a\u7c73\u65d7\u8230\u5e97","sid":105779984},{"nick":"\u7fbd\u7f8a\u65d7\u8230\u5e97","title":"\u7fbd\u7f8a\u65d7\u8230\u5e97","sid":106089095},{"nick":"\u683c\u8c03\u8863\u6a71\u65d7\u8230\u5e97","title":"\u683c\u8c03\u8863\u6a71\u65d7\u8230\u5e97","sid":106241183},{"nick":"ruonan1224","title":"Rena \u5c0f\u94fa","sid":106592362},{"nick":"\u597d\u5b69\u5b50v","title":"\u53ef\u53ef\u91cc\u5c0f\u59d0","sid":108075468},{"nick":"\u6881\u77f3\u576418","title":"\u5927\u773c\u775b\u8863\u6a71","sid":108802178},{"nick":"jc_market","title":"MOKI\u5bb6\u5973\u88c5\u5b9e\u62cd\u5e97","sid":108911660},{"nick":"\u8863\u604b\u661f\u8fb0","title":"\u58a8\u67d3\u7c73\u5170","sid":109179864},{"nick":"\u97e9\u90fd\u8863\u820d97","title":"\u97e9\u8863\u9488\u7ec7 \u4e13\u6ce8\u9488\u7ec7\u6bdb\u8863","sid":109225750},{"nick":"\u50bb\u591a\u591a\u7684\u5e97","title":"SANSAN\u5bb6\u6f6e\u6d41\u5973\u88c5\u5e97","sid":109741595},{"nick":"\u6e2f\u5473\u6f6e\u4eba\u9986","title":"\u6e2f\u5473\u6f6e\u4eba\u9986","sid":109847364},{"nick":"\u516c\u4e3b\u9b54\u8863\u574a","title":"\u516c\u4e3b\u9b54\u8863\u574a\u539f\u521b\u5973\u88c5","sid":110340325},{"nick":"\u4e03\u6708\u7cbe\u7075\u5bb6","title":"\u4e03\u6708\u7cbe\u7075\u5bb6","sid":110471204},{"nick":"\u52a8\u611f\u5c11\u5973\u65d7\u8230\u5e97","title":"\u52a8\u611f\u5c11\u5973\u65d7\u8230\u5e97","sid":110542553},{"nick":"tb68332428","title":"\u5ab1\u5ab1\u5bb6\u5b9e\u62cd\u5973\u88c5","sid":110695318},{"nick":"crazydandan66","title":"\u84dd\u5c4b\u4e00\u8857","sid":110880913},{"nick":"\u6b27\u97e9\u95fa\u871c\u5973\u88c5","title":"\u6b27\u97e9\u95fa\u871c\u5973\u88c5","sid":111251736},{"nick":"\u7f8a\u5c0f\u59d0\u5973\u88c5","title":"\u7f8a\u5c0f\u59d0\u5973\u88c5","sid":112128674},{"nick":"\u9047\u89c1\u9a74\u5148\u751f","title":"\u9047\u89c1\u9a74\u5148\u751f","sid":112297494},{"nick":"\u81fb\u65af\u60e0\u65d7\u8230\u5e97","title":"\u81fb\u65af\u60e0\u65d7\u8230\u5e97","sid":112523383},{"nick":"\u97e9\u4f18\u5c1a\u65d7\u8230\u5e97","title":"\u97e9\u4f18\u5c1a\u65d7\u8230\u5e97","sid":112586529},{"nick":"\u82b1\u59ff\u5170\u65d7\u8230\u5e97","title":"\u82b1\u59ff\u5170\u65d7\u8230\u5e97","sid":112655648},{"nick":"\u4eae\u9edb\u65d7\u8230\u5e97","title":"\u4eae\u9edb\u65d7\u8230\u5e97","sid":112744850},{"nick":"\u7cef\u7c73\u5bb618","title":"\u5c0f\u7cef\u7c73\u65f6\u5c1a\u5c4b","sid":112956262},{"nick":"\u5927sim","title":"\u5927Sim\u5c0fSim\u5c0f\u6e05\u65b0","sid":112985436},{"nick":"missshi11","title":"\u4e5d\u5982\u5df7 \u5b9e\u62cd\u5973\u88c5","sid":113295367},{"nick":"\u7545\u5f69\u65d7\u8230\u5e97","title":"\u7545\u5f69\u65d7\u8230\u5e97","sid":113444016},{"nick":"anting\u59d0","title":"\u5c0f\u5ce5\u5ce5\u65f6\u5c1a\u5973\u88c5","sid":113883564},{"nick":"goddess\u5c0f\u66e6","title":"\u97e9\u4f9d\u6d41","sid":114136770},{"nick":"\u82b1\u76f8\u5b9c\u65d7\u8230\u5e97","title":"\u82b1\u76f8\u5b9c\u65d7\u8230\u5e97","sid":114725125},{"nick":"\u62fe\u886b\u5996","title":"\u5c0f\u5996\u5bb6\u65f6\u5c1a\u5973\u88c5","sid":116985202},{"nick":"\u5b5f\u5c0f\u6728\u6728\u6728","title":"\u897f\u67e0 \u8212\u9002\u7b80\u7ea6\u5973\u88c5","sid":117386212},{"nick":"\u5929\u4f7f\u51e4\u51f0\u8857","title":"\u62c9\u7740\u73cd\u8ffd\u5927\u5954","sid":119620607},{"nick":"hello\u5973\u795e\u8303","title":"\u5de6\u5c0f\u59d0\u6765\u4e86","sid":122685716},{"nick":"\u5343\u4e1d\u4e07\u7f15yy","title":"\u5343\u4e1d\u4e07\u7f15yy","sid":124191660},{"nick":"\u540d\u838e\u96c6\u56e2","title":"\u540d\u838e\u96c6\u56e2\u5b98\u65b9\u5e97","sid":124573447},{"nick":"momo\u9ad8\u7aef\u5e97","title":"\u6768\u6cab\u6cabstudio","sid":125684263},{"nick":"\u8d85\u7ea7\u5e05\u7684\u638c\u67dc","title":"JHJ\u97e9\u56fd\u9986","sid":128836737},{"nick":"\u5de6\u90bb\u53f3\u820d5588","title":"\u5927\u8212\u5973\u88c5","sid":130060970},{"nick":"uvtt\u670d\u9970\u65d7\u8230\u5e97","title":"uvtt\u670d\u9970\u65d7\u8230\u5e97","sid":150088144},{"nick":"missve1","title":"MISS VE \u97e9\u56fd\u5973\u88c5\u5408\u4f5c\u5e97\u6bcf\u65e5\u4e0a\u65b0","sid":151746147},{"nick":"\u6d0b\u91522014","title":"\u7b80\u5c0f\u59d0\u5973\u88c5\u94fa","sid":152773861},{"nick":"insunday\u539f\u521b\u5973\u88c5","title":"InSunday\u539f\u521b\u5973\u88c5","sid":154871496},{"nick":"\u4e00\u751f\u5b88\u5019418","title":"\u8389\u8389\u5c0f\u516c\u4e3e","sid":162545180},{"nick":"\u7f8e\u5c1a\u534e\u7ee3\u670d\u9970\u65d7\u8230\u5e97","title":"\u7f8e\u5c1a\u534e\u7ee3\u670d\u9970\u65d7\u8230\u5e97","sid":181068872}],"ret":true}'''
    o = json.loads(s)
    if o['ret'] == True:
        # 更新店铺信息
        shop_data =  o['data']
        shops=[(d['sid'], d['title']) for d in shop_data]
        db = DB()
        db.update_shops(shops)
        db.commit()
    else:
        print '更新店铺数据失败'
        print s


def _crawl_one_day(d=None):
    '''
    爬取一天的数据。
    先获取所有店铺信息，再把所有店铺中的宝贝信息爬取出来
    d: date对象。指定日期。如果不指定的话爬取昨天数据
    :return:
    '''

    if d == None:
        d = date.today() - timedelta(1) #昨天日期

    db = DB()
    shops = db.get_all_shops()

    for s in shops:
        _update_one_shop(s[1], d)
        print 'updated shop: %s, for date: %s' % (s[1], d)




def _crawl_last_week():
    db = DB()
    shops = db.get_all_shops()

    for i in range(7, 0, -1):
        d = date.today() - timedelta(i) #昨天日期
        _crawl_one_day(d)

def update_and_crawl_one_day(d=None):
    _update_shops_info()
    _crawl_one_day()
    DB().update_params_for_goods()

def update_and_crawl_last_week():
    _update_shops_info()
    _crawl_last_week()
    DB().update_params_for_goods()

def update_all_need_to():
    '''
    更新所有需要更新且能更新的店铺数据
    :return:
    '''
    db = DB()
    shops = db.shops_needed_to_crawl()
    print shops
    for k in shops.keys():
        dates = shops[k]
        for d in dates:
            _update_one_shop(k, d)
            print 'updated: %s, %s'%(k, d)
    DB().update_params_for_goods()


if __name__ == "__main__":
    # _update_one_shop('110880913', date.today()-timedelta(1))
    # DB().update_indexes_for_goods(shop_id='110880913')

    update_and_crawl_one_day()
    #update_and_crawl_last_week()
    # update_all_need_to()
    #DB().update_params_for_goods()
    #print gen_items_url('110880913', '2018-03-11')