from paddleocr import PaddleOCR, draw_ocr

import numpy as np

# Paddleocr目前支持中英文、英文、法语、德语、韩语、日语，可以通过修改lang参数进行切换
# 参数依次为`ch`, `en`, `french`, `german`, `korean`, `japan`。
ocr = PaddleOCR(use_gpu=False,lang='ch') # need to run only once to download and load model into memory
img_path = './static/files/baidu/9.JPG'
result = ocr.ocr(img_path)

print(len(result))
print(len(result[0]))
str1 = ''
for res in result[0]:
    print(res[-1])
    str1 = str1 + res[-1][0]
print(str1)
