

import sys
import io
import importlib
import time
import requests  # 导入requests
from bs4 import BeautifulSoup  # 导入bs4中的BeautifulSoup
import os

# 将系统输出编码设为默认utf8格式，不然会出现UnicodeEncodeError
importlib.reload(sys)
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf8')

# 获取工作区的路径
wdir = os.getcwd()

headers = {'User-Agent':"Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.1 (KHTML, like Gecko) Chrome/22.0.1207.1 Safari/537.1"}##浏览器请求头（大部分网站没有这个请求头会报错、请务必加上哦）   
all_url = 'https://e-hentai.org/lofi/s/6f9855d14c/1012445-1'  ##开始的URL地址   
start_html = requests.get(all_url,  headers=headers)  ##使用requests中的get方法来获取all_url(就是：http://www.mzitu.com/all这个地址)的内容 headers为上面设置的请求头、请务必参考requests官方文档解释   
soup=BeautifulSoup(start_html.text,'lxml')
li_list=soup.find_all('a')
print('find over')
for li in li_list:##读取下一页
    href=li['href']
    print(href)
    break
print('spider over')