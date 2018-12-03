import requests
import time
# header = {
#     'Accept':'application/json, text/javascript, */*; q=0.01',
#     'Accept-Encoding':'gzip, deflate',
#     'Accept-Language':'zh-CN,zh;q=0.8,en;q=0.6',
#     'Connection':'keep-alive',
#     'Content-Length':'2',
#     'Content-Type':'application/json',
#     'Host':'gs.amac.org.cn',
#     'Origin':'http://gs.amac.org.cn',
#     'Referer':'http://gs.amac.org.cn/amac-infodisc/res/pof/fund/index.html',
#     'User-Agent':'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/50.0.2661.102 Safari/537.36',
#     'X-Requested-With':'XMLHttpRequest'
# }
header = {
        'User-Agent':'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/52.0.2743.82 Safari/537.36',
        'content-type': "application/json",
        'cache-control': "no-cache",
        'postman-token': "a5a8f573-f9c8-07bc-770d-b077a0b86670"
    }

url='http://gs.amac.org.cn/amac-infodisc/api/pof/fund?rand=0.5867456580697086&page=0&size=20'


# r = requests.post(url, body="{}", headers=header)
# print r.text

x = time.localtime(1395878400)
# y = time.mktime(time.strptime('2014-03-27','%Y-%m-%d'))
time.strftime('%Y-%m-%d %H:%M:%S',x)
print x