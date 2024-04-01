# 导入easyocr-识别图片文字库
import easyocr
from paddleocr import PaddleOCR
# 导入os-操作文件库
import os
#进行SQLite数据库操作
import sqlite3

dbpath = "../image.db"

def saveData(dbpath):
    init_db(dbpath)
    # print("数据库初始化成功！")
    conn = sqlite3.connect(dbpath)
    cur = conn.cursor()

    # 获取爬取到的所有文件名称，以及当前路径
    file_dir = '../static/files/baidu'  # 你的文件路径

    def getFlist(path):
        for files in os.walk(path):
            print('files:', files)  # 得到一个元组：1、当前路径 2、子文件夹 3、文件名称，返回list类型
        return files

    file_name = getFlist(file_dir)
    # 创建reader对象
    reader = easyocr.Reader(['ch_sim', 'en'], gpu=False)
    ocr = PaddleOCR(use_gpu=False, lang='ch')
    for item in file_name[2]:
        data = []
        # 读取完整路径下的图像
        full_path = file_name[0] + '/' + item
        data.append('"' + full_path + '"')
        # 防止无效图片路径
        if str(type(full_path)) != "<class 'NoneType'>":
            try:
                # easyocr
                # result = reader.readtext(full_path, detail=0, paragraph=True)
                # # 将列表转为字符串
                # result = ''.join(result)
                # # 去除字符串中的空格
                # result = result.replace(" ", "")

                # paddleocr
                result = ocr.ocr(full_path)
                str1 = ''
                for res in result[0]:
                    # print(res[-1])
                    str1 = str1 + res[-1][0]
                # print(str1)
                data.append('"' + str1 + '"')



                sql = '''
                            insert into imageTab(
                                image_url, image_txt
                            )values(%s)''' % ",".join(data)
                cur.execute(sql)
                conn.commit()

                # 结果
                print('正在识别' + item + '图片' + ',并导入其文字至数据库：' + result)
            except:
                print(full_path)

    cur.close()
    conn.close()


# 初始化数据库数据
def init_db(dbpath):
    # 创建图片表
    sql1 = '''
        create table if not exists imageTab (
            id integer primary key autoincrement,
            image_url varchar,
            image_txt text
        )
    '''

    # 创建用户表
    sql2 = '''
        create table if not exists userInfo (
            id integer primary key autoincrement,
            username varchar,
            mm varchar
        )
        '''
    sql3 = '''delete from imageTab; 
          
           '''
    sql4 = '''
            update sqlite_sequence set seq=0 where name = 'imageTab';
            '''
    #创建数据表
    conn = sqlite3.connect(dbpath)
    cursor = conn.cursor()
    cursor.execute(sql1)
    cursor.execute(sql2)
    # 清空图片表
    cursor.execute(sql3)
    cursor.execute(sql4)
    conn.commit()
    cursor.close()
    conn.close()

if __name__ == '__main__':
    saveData(dbpath)
    # init_db(dbpath)