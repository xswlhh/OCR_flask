from paddleocr import PaddleOCR
# 导入os-操作文件库
import os
#进行SQLite数据库操作
import sqlite3


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



if __name__ =="__main__":
    saveImg(dbpath = "./image.db",imgpath="./static/files/baidu/签名.jpg")



