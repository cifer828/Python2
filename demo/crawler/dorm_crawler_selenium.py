# -*- coding: utf-8 -*-
from selenium import webdriver
import time
import BeautifulSoup


driver=webdriver.Chrome()                #用chrome浏览器打开
driver.get("https://ids.tongji.edu.cn:8443/nidp/saml2/sso?id=66&sid=0&option=credential&sid=0")       #打开知乎我们要登录
time.sleep(2)                            #让操作稍微停一下

#找到输入账号的框，并自动输入账号 这里要替换为你的登录账号
driver.find_element_by_name('Ecom_User_ID').send_keys('1632524')
time.sleep(2)
#密码，这里要替换为你的密码
driver.find_element_by_name('Ecom_Password').send_keys('828211')
time.sleep(2)

#找到登录按钮，并点击
driver.find_element_by_name('submit').click()

cookie=driver.get_cookies()
time.sleep(3)
driver.get('http://myportal.tongji.edu.cn/xsfw/sys/ssxfapp/*default/index.do?gid_=QU1QMjAxNTA4MDgxODM1NDU0NjU=#/preview')
time.sleep(5)
