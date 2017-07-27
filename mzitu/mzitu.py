

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


class mzitu:

    def all_url(self, url):
        html = self.request(url)  # 调用request函数把套图地址传进去会返回给我们一个response

        # 利用BeautifulSoup分析页面源码 获得分标题列表
        all_a = BeautifulSoup(html.text, 'lxml').find(
            'div', class_='main').find_all('a')

        img_title_num = 1
        img_page_num = 1

        # 遍历所有分页面
        for a in all_a:
            title = a.get_text()
            if title == '':
                pass
            else:
                print(
                    '-----------------------------------')
                print(u'开始保存------->第', img_title_num,
                      '组：', title)  # 加点提示不然太枯燥了
                path = str(img_title_num) + '--' + str(title).strip()

                # 调用mkdir函数创建文件夹！这儿path代表的是标题title哦！！！！！不要糊涂了哦！
                self.mkdir(path)
                os.chdir(wdir + '/' + path)  # 切换到目录
                href = a['href']

                # 调用html函数把href参数传递过去！href是啥还记的吧？ 就是套图的地址哦！！不要迷糊了哦！
                self.html(href, img_title_num, img_page_num, title)
                img_title_num += 1
                sys.stdout.write('一组保存完毕')
                sys.stdout.writelines('，组名是' + title)
                print(
                    '\n----------------------------------')
        print('爬虫完毕')

    def html(self, href, img_title_num, img_page_num, title):  # 这个函数是处理套图地址获得图片的页面地址
        html = self.request(href)

        # 利用BeautifulSoup分析相应页面，并获得分页面的页码数
        max_span = BeautifulSoup(html.text, 'lxml').find_all('span')[
            10].get_text()

        # 捕获标签信息类型异常
        try:
            max_page = int(max_span) + 1
        except ValueError:
            print("ERROR******页面页码获取异常（数值类型异常），跳过该页面******")
            errf = open('errlog.txt', 'w')
            errf.write('ERROR******页面页码获取异常（数值类型异常），跳过该页面******' + 'ValueError:' +
                       str(img_title_num) + "--title---name is:" + title)
            errf.close()
            return

        # 遍历分页面所有页码
        for page in range(1, max_page):
            page_url = href + '/' + str(page)
            self.img(page_url, img_title_num,
                     img_page_num, max_page)  # 调用img函数
            img_page_num += 1

    def img(self, page_url, img_title_num, img_page_num, max_page):  # 这个函数处理图片页面地址获得图片的实际地址
        img_html = self.request(page_url)
        img_url = BeautifulSoup(img_html.text, 'lxml').find(
            'div', class_='main-image').find('img')['src']
        self.save(img_url, img_title_num, img_page_num, max_page)

    def save(self, img_url, img_title_num, img_page_num, max_page):  # 这个函数保存图片
        ##name = img_url[-9:-4]
        name = '第' + str(img_title_num) + '组' + '第' + str(img_page_num) + '张'
        img = self.request(img_url)

        # 捕获文件名异常
        try:
            f = open(name + '.jpg', 'wb')
            f.write(img.content)
            f.close()
            sys.stdout.write('图片保存成功，名字为:' + name + '----' +
                             str(img_page_num) + ' \ ' + str(max_page-1) + '\r')
            sys.stdout.flush()
            time.sleep(0.1)
        except PermissionError:
            print('ERROR******图片保存异常，跳过该张图片******')
            errf = open('errlog.txt', 'w')
            errf.write('ERROR******图片保存异常，跳过该张图片******\n' + "PermissionError:" +
                       str(img_page_num) + "--page---is:" + name)
            errf.close()
            return

    def mkdir(self, path):  # 这个函数创建文件夹
        isExists = os.path.exists(os.path.join(wdir, path))
        if not isExists:
            print(u'建了一个名字叫做', path, u'的文件夹！')
            os.makedirs(os.path.join(wdir, path))
            return True
        else:
            print(u'名字叫做', path, u'的文件夹已经存在了！')
            return False

    def request(self, url):  # 这个函数获取网页的response 然后返回
        headers = {
            'User-Agent': "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.1 (KHTML, like Gecko) Chrome/22.0.1207.1 Safari/537.1"}
        content = requests.get(url, headers=headers)
        return content


MeiZiTu = mzitu()
MeiZiTu.all_url('http://www.mzitu.com/all')  # 给函数all_url传入参数  你可以当作启动爬虫（就是入口）
