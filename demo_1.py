# _*_ coding:utf-8 _*_
# 开发人员: LingJiabin
# 开发工具: PyCharm
# 开发日期: 2020/4/3 下午 7:28
# 文件名  : demo_1.py

import requests
import re
import jieba.analyse
from sklearn.externals import joblib
import time
import collections

label_map = ['财经', '彩票', '房产', '股票', '家居',
                     '教育', '科技', '社会', '时尚', '时政',
                     '体育', '星座', '游戏', '娱乐']

channel_way = ['新闻', '经济', '体育', '科教']
sort_way = {'热点':'relevance', '实时':'date'}
page = '1'

url = u"https://search.cctv.com/search.php?qtext=疫情&page=1&type=web&sort="+ sort_way['实时'] +"&datepid=1&channel="+channel_way[0]+"&vtime=-1&page="+page
head = {'User-Agent' : 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/80.0.3987.149 Safari/537.36'}
i = 0

url1 = r'https://v.cctv.com/index.shtml'

while i < 3:
    try:
        time.sleep(1.2)
        html = requests.post(url, verify=False, headers=head)
        html1 = requests.post(url1, verify=False, headers=head)
        html.raise_for_status()
        html1.raise_for_status()
        html.close()
        html1.close()
        break
    except Exception as e:
        # logger.error(e)
        print(e)
        i += 1
    else:
        # print(html.text)
        print("html_ok")

html.encoding = html.apparent_encoding
html1.encoding = html1.apparent_encoding

t_word = re.findall('target="_blank">(.*)?</a>', html.text)
t_word = {}.fromkeys(t_word).keys()
t_word = list(t_word)
#print(html.text)
print(html1.text)
con_word = re.findall('(.*)?		                        						</p>', html.text)
News_time = re.findall('tim">(.*)?</span>', html.text)
imgs_url = re.findall(';" src="(.*)?" onload', html.text)

img_url = re.findall('src="(.*)?" data-src', html1.text)
title_s = re.findall('text"><p>(.*)?</p></div>', html1.text)
show_url = re.findall('<a href="(.*)?" target="_blank">', html1.text)

print('time')
print(News_time)
print('imgs')
print(imgs_url)
print('img')
print(title_s)
print(show_url[25:31])
print(img_url[0:6])

title = []
content = []

if page=='1':
    flag = 2
else:
    flag = 0

#print(con)

for i in range(10):
    temp = t_word[i+1+flag].replace('<font color="red">', '')
    #print(temp.replace('</font>', ''))
    title.append(temp.replace('</font>', '').replace('&ldquo;', '"').replace('&rdquo;', '"'))
    temp1 = con_word[i].replace('<font color="red">', '').replace("\t", '').strip()
    content.append(temp1.replace('</font>', '').replace('\u3000', '').replace('&ldquo;', '"').replace('&rdquo;', '"'))

print(title)
print(content)

S_classifier = joblib.load("S_clf_model.m")
S_tf = joblib.load('S_tf_model.m')
S_tests = []
tests = []
for x in content:
    #print(x)
    S_word = jieba.analyse.extract_tags(x, topK=20, withWeight=False, allowPOS=( 'n', 'a', 'an', 'e', 'i', 'v', 'vi'))
    key_word = jieba.analyse.extract_tags(x, topK=10, withWeight=False, allowPOS=('n', 'nr', 'ns',  'nz', 'an', 'q', 'tg'))
    #allowPOS=('n','nr','ns', 'nt', 'nz', 'q', 'tg')( 'n', 'nz', 'a', 'an', 'e', 'i', 'v', 'vi')
    S_line = ' '.join(S_word)
    line = ' '.join(key_word)
    S_tests.append(S_line)
    tests.append(line)
    #输出关键词
    print(S_line)

#print(S_tests)
print(tests)

S_proba = S_classifier.predict_proba(S_tf.transform(S_tests))

s0_list = []
s1_list = []

for x in range(10):
    s0 = float(S_proba[x][0])
    s1 = float(S_proba[x][1])

    s0_list.append(round(s0, 4))
    s1_list.append(round(s1, 4))

print(s0_list)
print(s1_list)

Inf = 0
for i in range(10):
    #print(s0_list.index(max(s0_list)))
    s0_list[s0_list.index(max(s0_list))] = Inf


classifier = joblib.load("clf_model.m")  # 加载训练模型
tf = joblib.load('tf_model.m')

res_predict = classifier.predict(tf.transform(tests))
res_predict = list(res_predict)
print(res_predict)

sub = [0 for i in range(14)]
print(sub)

for i in range(len(res_predict)):
    sub[res_predict[i]-1] += 1
print(sub)

All = []
for i in range(len(tests)):
    All += tests[i].split()
print(All)

All_res = collections.Counter(All)
print(All_res.most_common(5))

word = '全国'
print(len(word))



