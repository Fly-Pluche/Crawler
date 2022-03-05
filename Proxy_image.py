import time

from lxml import etree
import os
import datetime
import requests
from urllib import request


# 下载图片（获取某一页图片链接并下载）
def downloadImage(url, pathway):
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/98.0.4758.80 Safari/537.36 Edg/98.0.1108.43'
    }
    res = requests.get(url='https://' + url, headers=headers)  # 加个头，伪装一下
    res.encoding = res.apparent_encoding  # 设置编码格式，防止乱码，好像这个网站，不设置也可以

    dom = etree.HTML(res.text)  # etree.html 生成一个xpath对象，参数必须是string类型

    src = dom.xpath('//div[@id="piclist"]/ul/li/img/@src')  # 获取一个图集内图片的链接

    title = dom.xpath('//div[@class="container"]/div/div/div/div/div/h1/text()')  # 获取标题
    firstsrc = src[0]
    filetype = firstsrc[-4:]  # 获取图片类型，个人觉得不获取也可以

    path = pathway + "/性感美女/" + title[0] + "/"
    if not os.path.exists(path):
        os.makedirs(path)
    i = 1  # 给一组图片记个数
    for img in src:
        imgUrl = "https:" + img
        temp = requests.get(imgUrl, headers=headers)
        with open(path + '/' + str(i) + str(filetype), 'wb') as f:
            f.write(temp.content)
        print("图片下载成功：" + imgUrl)
        i += 1


if __name__ == '__main__':
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/98.0.4758.80 Safari/537.36 Edg/98.0.1108.43'
    }
    pathway = 'E:/wallhaven/anime'  # 存储路径
    urlList = 'https://wallhaven.cc/search'
    url = 'https://wallhaven.cc/w/'
    handler = request.ProxyHandler({'http': 'https://127.0.0.1:4780'})
    opener = request.build_opener(handler)

    yaml_path = './log/1.yaml'
    log = open(yaml_path, 'r')
    print("   == 即将开始精彩资源的下载 == ")
    startNum = int(log.read())
    index = int((startNum - 1) * 24)
    print(startNum, index)
    log.close()
    endNum = int(130)  # 终止页，左闭右开

    startTime = datetime.datetime.now()
    for n in range(startNum, endNum):
        print(f'第{n}页')
        log = open(yaml_path, 'w')
        log.write(f'{n}\n')
        log.close()
        req = request.Request(
            url=f'https://wallhaven.cc/search?categories=010&purity=110&topRange=1M&sorting=toplist&order=desc&page={n}',
            headers=headers)
        try:
            response = opener.open(req).read()
        except:
            print('can\'t get',f'https://wallhaven.cc/search?categories=010&purity=110&topRange=1M&sorting=toplist&order=desc&page={n}',)
            time.sleep(10)
        # content = response.content
        dom = etree.HTML(response)  # 生成一个xpath对象
        src = dom.xpath(f'//*[@id="thumbs"]/section[1]/ul/li/figure/@data-wallpaper-id')  # 获取每一组图片的链接
        starttime = datetime.datetime.now()

        for img in src:
            img = str(img)
            url_img = url + img
            req = request.Request(url=url_img, headers=headers)
            response = opener.open(req).read()
            dom = etree.HTML(response)
            img_src = dom.xpath('//*[@id="wallpaper"]/@src')[0]
            filetype = img_src[-4:]

            req = request.Request(url=img_src, headers=headers)
            response = opener.open(req).read()
            print('index', index)

            with open(pathway + '/' + str(index) + str(filetype), 'wb') as f:
                f.write(response)
            print("图片下载成功：" + url_img)
            time.sleep(3)

            index += 1
        endtime = datetime.datetime.now()

        print("  下载成功，耗时：" + str(endtime - starttime))
        time.sleep(10)
        print("===========================> 第" + str(n) + "页图片列表下载完成 <===========================")

    endTime = datetime.datetime.now()

    print("下载成功，耗时：：" + str(endTime - startTime))
