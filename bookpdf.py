# -*- coding: utf-8 -*-
"""
Spyder Editor

This is a temporary script file.
"""

###  先安装google浏览器驱动chromedriver
###  安装方法： https://www.jianshu.com/p/dc0336a0bf50


from lxml import etree
import time
import re
import random
from selenium import webdriver
import os
import requests

def read_book(web_url,unif_time):
    #web_url="https://max.book118.com/index.php?g=Home&m=NewView&a=index&aid=5042234004001343&v=20190917"
    browser = webdriver.Chrome()
    browser.get(web_url)

    page_text = "PREVIEW_PAGE = { actual: parseInt\(\'(\d*?)\'\), preview: parseInt\(\'(\d*?)\'\)}"
    parseInt = re.search(page_text,browser.page_source)
    dd = int(parseInt.group(1))

    # 先翻页
    nextpage = browser.find_element_by_class_name('page-next')
    for i in range(0, dd):
        nextpage.click()
        time.sleep(random.uniform(unif_time,unif_time+2))  # 等待图片加载
    # 再解析
    # 解析页面数据（获取页面中的图片链接）
    # 创建etree对象
    tree = etree.HTML(browser.page_source)
    div_list = tree.xpath("//div[@class='webpreview-item']")
    urls = []
    # 解析获取图片地址和图片的名称
    for div in div_list:
        urls.append(div.xpath('.//img/@src'))
    
    i = 0
    for item in urls:
        i = i+1
        if len(item) > 0:
            if "http:" in item[0]:
                url = item[0]
            else:
                url = "http:"+item[0]
            response = requests.get(url)
            with open('D:/zgs/pdf/'+str(i)+'.png', 'wb') as f:
                f.write(response.content)
        else:
            print(item)  # 打印未加载出来的页面
    f.close()
    return dd
    
    
    
    




# 读取图片列表
picPath = "D:/zgs/pdf/"

web_url = "https://max.book118.com/index.php?g=Home&m=NewView&a=index&aid=7140053164001150&v=20190917"
i = 1
unif_time = 6

while i<=3:
    dd = read_book(web_url,unif_time)
    i = i+1
    unif_time = unif_time-2
    if len(os.listdir(picPath)) == dd:
        break
    

from PIL import Image
file_list = os.listdir(picPath)
file_list.sort(key= lambda x:int(x[:-4]))
pic_name = []
for x in file_list:
    pic_name.append(picPath+x)

# 合并为pdf
im1 = Image.open(pic_name[0])
pic_name.pop(0)
im_list = []
for pic in pic_name:
    img = Image.open(pic)
    if img.mode == "RGBA":
        img = img.convert('RGB')
        im_list.append(img)
    else:
        im_list.append(img)
im1.save(picPath + "生物信息学分析实践.pdf", "PDF", save_all=True, append_images=im_list)
im1.close()


