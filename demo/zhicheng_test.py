# -*- coding:utf-8 -*-

import requests
import datetime

cookie_dict={
    'gr_user_id':'47e8bbb3-fe4a-4669-b082-c7193768a879',
    'TYCID':'b91c42621f26430d870f554644146686',
    'aliyungf_tc':'AQAAABZU1kmrPAUAjRGtPYkEgBUPFhdy',
    'tnet':'61.173.17.141',
    '_pk_ref.1.e431':'%5B%22%22%2C%22%22%2C1495071576%2C%22https%3A%2F%2Fwww.baidu.com%2Flink%3Furl%3DA6tSb6OSvYwtuzjh00z9CraDLvGvdSCzgGKF6ib4S9oReX5e5utSMFahsa7qkg7t%26wd%3D%26eqid%3Da3f7976e000647d600000004591cfbb6%22%5D',
    'RTYCID':'41d0804bfd7544f598134b4d488e553c',
    'Hm_lvt_e92c8d65d92d534b0fc290df538b4758':'1494669139,1494979234,1495071576,1495071959',
    'Hm_lpvt_e92c8d65d92d534b0fc290df538b4758':'1495072092',
    '_pk_id.1.e431':'47fa17c5b130a5ea.1491792848.14.1495072093.1495071576.',
    'token':'b7662472ed8b461282cc6d5f8e4f6488',
    '_utm':'5152ea49d6eb4bd3a86fbdaad182b0c6',
    'paaptp':'1af3ef309730d44ef6697a1548a32eaf46c52fc11e03db56f515c193db370',
    '_pk_ses.1.e431':'*'
}

url = 'http://www.tianyancha.com/v2/company/9519792.json'
r = requests.get(url, cookies = cookie_dict)
print r.content
# print datetime.datetime.now()