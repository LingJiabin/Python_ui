# _*_ coding:utf-8 _*_
# 开发人员: LingJiabin
# 开发工具: PyCharm
# 开发日期: 2020/4/25 下午 7:17
# 文件名  : demo_2.py


import requests
import linecache
from  datetime import datetime,timedelta
import random
import re
import os

'''
url = 'https://v.cctv.com/2020/04/25/VIDEDBmswH0ZKXs6NRTaXTD6200425.shtml?spm=C90324.PE6LRxWJhH5P.S23920.5'

head = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/80.0.3987.149 Safari/537.36'}

html = requests.post(url, verify=False, headers=head)
html.raise_for_status()
html.close()

html.encoding = html.apparent_encoding

V_title = re.findall('<title>(.*)?</title>', html.text)

d_files = os.listdir('src')  #返回指定文件夹的列表名
d_files.sort(key=lambda x:int(x))


src_path = 'src\\'
data_path = 'data\\'


for i in range(len(d_files)):
    path = src_path + d_files[i] + '\\url.txt'

    with open(path, 'r', encoding='UTF-8') as f:
        url = f.readline()

    for x in range(3):
        try:
            html = requests.post(url, verify=False, headers=head)
            html.raise_for_status()
            html.close()
            html.encoding = html.apparent_encoding
            V_title = re.findall('<title>(.*)?</title>', html.text)

            with open(path, 'w', encoding='utf-8') as f:
                f.write(url)
                f.write(V_title[0])
            break
        except:
            print('???')
'''
flag = 0

src_path = 'src\\'
data_path = 'data\\'

d_files = os.listdir('src')  #返回指定文件夹的列表名
d_files.sort(key=lambda x:int(x))
x = random.randint(0,46)
delta = timedelta(days=x)
now = datetime.now()


n_data = now - delta

print(n_data.strftime('%Y-%m-%d'))
'''
for i in range(len(d_files)):
    path = src_path + d_files[i] + '\\url.txt'
    x = random.randint(20, 46)
    delta = timedelta(days=x)
    n_data = now - delta
    if linecache.getline(path, 3) == None:
        with open(path, 'a', encoding='utf-8') as f:
            f.write('\\n'+ str(n_data.strftime('%Y-%m-%d')))
            print(str(n_data.strftime('%Y-%m-%d')))
    else:
        continue
'''

all_dir={}

for i in range(len(d_files)):
    path = src_path + d_files[i] + '\\url.txt'
    V_time = linecache.getline(path, 3).strip()
    if V_time == None:
        print(path)
    all_dir[V_time] = d_files[i]


list1 = sorted(all_dir.items())
print(sorted(all_dir.items()))
print(list1[0][0])
#print(V_title)