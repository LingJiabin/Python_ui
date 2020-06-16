# _*_ coding:utf-8 _*_
# 开发人员: LingJiabin
# 开发工具: PyCharm
# 开发日期: 2020/4/30 下午 3:50
# 文件名  : demo_3.py

import cv2
import os
import jieba.analyse


s_files = os.listdir('src')  # 返回指定文件夹的列表名
s_files.sort(key=lambda x: int(x))


for i in s_files:
    Vpath = 'src\\' + i + r'\News.mp4'
    Jpath = 'src\\' + i + r'\Cover.jpg'
    vidcap = cv2.VideoCapture(Vpath)
    vidcap.set(cv2.CAP_PROP_POS_FRAMES, 100)
    success, image = vidcap.read()
    imag = cv2.imwrite(Jpath, image)

print("ok")

'''

Text_path = 'src\\141' + r'\\News.txt'

with open(Text_path, 'r', encoding='utf-8') as f:
    file_text = f.read()

key_word = jieba.analyse.extract_tags(file_text.replace("\t", "").replace("\n", ""), topK=20, withWeight=False,
                                      allowPOS=('n', 'nr', 'ns', 'nt', 'nz', 'q', 'tg'))

S_word = jieba.analyse.extract_tags(file_text.replace("\t", "").replace("\n", ""), topK=20, withWeight=False,
                                    allowPOS=('n', 'nz', 'a', 'an', 'e', 'i', 'v', 'vi'))

outline = ' '.join(key_word)  # 提取新闻文本关键词
S_line = ' '.join(S_word)

print(outline)
'''