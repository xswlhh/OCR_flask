基于falsk框架 + paddleocr的简单OCR文字识别web系统

一、	基础环境
Python 3.8
Flask 3.0+
Jinja2 3.1+
Paddleocr 2.7
Paddlepaddle 2.6
Selenium 无版本要求，最新即可

二、	使用说明
1.	先运行spider文件下的image.py 获得一些样例图片
如果有关于浏览器驱动的报错，说明浏览器驱动(edge)与电脑上的浏览器不兼容，可自行下载兼容版本到spider文件夹下
2.	再运行getImageTxt.py ,此操作是读取已下载好图片内的文字
3.	直接运行app.py 启动项目即可



