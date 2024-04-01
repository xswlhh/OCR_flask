from selenium import webdriver
# from lxml import etree
import os
import time
import requests
import re
#制定URL，获取网页数据
# import urllib.request, urllib.error, urllib.parse as parse
#
# kw = input("请输入你要搜索的岗位关键字：")
# keyword = parse.quote(parse.quote(kw))

headers = {
    "user-agent": "Mozilla/5.0 (Windows NT 6.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/55.0.2883.87 Safari/537.36",
}

# 创建文件夹
if not os.path.exists("../static/files/baidu"):
    os.makedirs("../static/files/baidu")


def get_html():
    # 控制chrome浏览器
    # option = webdriver.ChromeOptions()
    path = 'msedgedriver.exe'
    driver = webdriver.Edge(path)
    # 窗口最大化
    driver.maximize_window()
    # 输入网址
    driver.get("https://image.baidu.com/")
    # 找到文本框，输入文字
    driver.find_element('xpath', '//*[@id="kw"]').send_keys("宋体字临摹")
    # 找到按钮，单击
    driver.find_element('xpath', '//*[@class="s_newBtn"]').click()
    # 停一下，等待加载完毕
    time.sleep(2)

    # 切换窗口，因为现在打开了一个窗口，目前还是在第1个窗口中
    driver.switch_to.window(driver.current_window_handle)
    for i in range(2):
        # 执行js
        driver.execute_script("window.scrollTo(0,10000)")
        time.sleep(1)
    # 获取页面html
    html = driver.page_source
    # 关闭
    driver.quit()
    # 保存html
    with open(f"../static/files/baidu.html", "w", encoding="utf-8") as file:
        file.write(html)

    return html

def get_data():
    with open("../static/files/baidu.html", "r", encoding="utf-8") as file:
        html = file.read()

    #通过正则获取img url
    img_list1 = re.findall(r'data-objurl="(.*?)"', html)
    img_list2 = re.findall(r'data-imgurl="(.*?)"', html)
    # print(len(img_list1))
    # print(len(img_list2))

    # img_list1合并到img_list2
    img_list1.extend(img_list2)

    # 图片名称
    i = 0
    for img_url in  img_list2:
        currentUrl = img_url.replace("amp;", "")
        # print(currentUrl)
        rr = requests.get(currentUrl, headers=headers)
        rr.encoding = rr.apparent_encoding  # 修改编码

        img_name = "../static/files/baidu/" + str(i) + '.JPG'
        i += 1
        # print(img_name)
        with open(img_name, 'wb') as file:
            file.write(rr.content)

if __name__ == '__main__':
    # 获取百度图片并保存到baidu.html页面中
    # 获取baidu.html页面的网页链接，并模拟打开链接，将此图片资源保存到本地文件夹中
    if get_html():
        get_data()