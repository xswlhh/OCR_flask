from flask import Flask, render_template, request, jsonify, session, redirect
import math
import sqlite3
from paddleocr import PaddleOCR
import os


app = Flask(__name__)
app.config["SECRET_KEY"] = 'TP52fjHWRbyVq8zu9v82dWYW1'

#每次路由之前
@app.before_request
def before_request():
    if (request.path == "/login" or request.path == "/login_action" or request.path == "/registered" or request.path == "/registered_action" or request.path == "/logout"):
        return None
    if not session.get("username") and request.endpoint not in ('login', 'static'):
        return redirect("/login")

# 1、首页
@app.route('/')
def hello_world():
    pageObj = getPageList(1)
    username = session.get("username")
    return render_template("index.html", result='', page=1, pagelists=pageObj, username=username)


# 2、注册模块
@app.route('/registered')
def registered():
    return render_template("registered.html", result='')


@app.route('/registered_action', methods=['POST'])
def registered_action():
    ###POST提交方式
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')
        result = addUser(username, password)

        return jsonify(result)


# 3、登录模块
@app.route('/login')
def login():
    # print("231231")
    return render_template("login.html")


@app.route('/login_action', methods=['POST'])
def login_action():
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')
        result = getUserInfo(username, password)

        if(result['code'] == 200):
            session["username"] = username

        return jsonify(result)

@app.route('/logout', methods=['GET'])
def logout():
    del session["username"]
    return redirect('/login')


#  三、翻页模块
@app.route('/page', methods=['POST', 'GET'])
def page():
    if request.method == 'POST':
        username = session.get("username")

        result = request.form
        data = []
        where = ''

        for key, value in result.items():
            if key == 'page':
                page = int(value)
                data.append(int(value))
            elif key == 'page_image_txt':
                where = " where image_txt LIKE '%" + value + "%'"
                data.append(value)

        pageObj = getPageList(page, where)

        # print(pagelists)
        return render_template("index.html", result=data[1], page=page, pagelists=pageObj, username=username)


# 四、搜索模块
@app.route('/result', methods=['POST', 'GET'])
def result():

    if request.method == 'POST':
        username = session.get("username")
        result = request.form
        for key, value in result.items():
            where = " where image_txt LIKE '%" + value + "%'"
            # print(where)
            pageObj = getPageList(1, where)

            return render_template("index.html", result=value, page=1, pagelists=pageObj, username=username)

@app.route('/add', methods=['POST', 'GET'])
def add():
    if request.method == 'POST':

        fileStorage = request.files.get('file')
        if fileStorage != '':
            print(fileStorage.filename)
            if fileStorage.filename.split('.')[-1] == 'jpg' or fileStorage.filename.split('.')[-1] == 'png':
                save_folder = 'C:/Users/27230/Desktop/毕业设计/python-图片识别文字项目/project/static/files/baidu/'
                # fileStorage.save() 文件位置必须是绝对路径
                fileStorage.save(save_folder + fileStorage.filename)
                print('保存成功',fileStorage.filename)

                saveImg("./image.db","./static/files/baidu/"+fileStorage.filename)

        pageObj = getPageList(1)
        username = session.get("username")
        return render_template("index.html", result='', page=1, pagelists=pageObj, username=username)

# 获取imageTab表数据方法
def getPageList(page,where=''):
    pageObj = {
        "list": [], "total": 1, "pageSize": 16
    }

    offset = (page - 1) * pageObj["pageSize"]
    conn = sqlite3.connect("image.db")
    cur = conn.cursor()
    sql1 = "select count(*) from imageTab " + where
    # print(sql1)
    totalData = cur.execute(sql1)
    for item1 in totalData:
        # item1是元组
        pageObj["total"] = math.ceil(int(item1[0]) / pageObj["pageSize"])

    sql = "select * from imageTab " + where + " order by image_url asc limit " + str(offset) + ',' + str(pageObj["pageSize"])
    data = cur.execute(sql)
    for item in data:
        pageObj["list"].append(item)
    cur.close()
    conn.close()
    return pageObj


# 添加userInfo表数据方法
def addUser(username, password):
    result = {'code': '', 'data': ''}

    conn = sqlite3.connect("image.db")
    cur = conn.cursor()
    # print(username, password)
    sql1 = "select * from userInfo where username = '"+username+"' "
    cur.execute(sql1)
    userData = cur.fetchall()
    # print(userData)

    if len(list(userData)) == 0:
        sql2 = "Insert into userInfo (username, mm) values ('" + username + "','" + password + "') "
        cur.execute(sql2)
        conn.commit()  # 执行sql语句
        result['code'] = 200
        result['data'] = '用户未存在，注册成功'
    else:
        result['code'] = 400
        result['data'] = '用户已存在'

    cur.close()
    conn.close()

    return result


# 查询userInfo表数据方法
def getUserInfo(username, password):
    result = {'code': '', 'data': ''}

    conn = sqlite3.connect("image.db")
    cur = conn.cursor()
    # print(username, password)
    sql1 = "select * from userInfo where username = '" + username + "' and mm = '" + password + "'"
    # print(sql1)
    cur.execute(sql1)
    userData = cur.fetchall()
    if len(list(userData)) == 0:
        result['code'] = 400
        result['data'] = '账号密码错误，登录失败'
    else:
        result['code'] = 200
        result['data'] = '登录成功'
    # print(userData)

    cur.close()
    conn.close()

    return result
# 添加图片
def saveImg(dbpath,imgpath):

    ocr = PaddleOCR(use_gpu=False, lang='ch')
    conn = sqlite3.connect(dbpath)
    cur = conn.cursor()
    data = []
    # img_url
    data.append('"' + imgpath + '"')

    result = ocr.ocr(imgpath)
    str1 = ''
    for res in result[0]:
        # print(res[-1])
        str1 = str1 + res[-1][0]
    # image_txt
    data.append('"' + str1 + '"')

    print(data)
    sql = '''
                                insert into imageTab(
                                    image_url, image_txt
                                )values(%s)''' % ",".join(data)
    cur.execute(sql)
    conn.commit()

    cur.close()
    conn.close()

if __name__ == '__main__':
    app.run()
