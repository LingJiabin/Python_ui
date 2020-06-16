# _*_ coding:utf-8 _*_
# 开发人员: LingJiabin
# 开发工具: PyCharm
# 开发日期: 2020/4/3 下午 6:31
# 文件名  : demo_0.py

from PySide2.QtWidgets import QApplication, QMainWindow, QPushButton, QPlainTextEdit, QMessageBox, QFileDialog
from PySide2.QtCore import *
from PySide2.QtUiTools import QUiLoader
from PySide2.QtCharts import *
from PySide2.QtGui import *
from PySide2.QtMultimedia import *
from PySide2.QtMultimediaWidgets import QVideoWidget

import re
import os
import sys
import cv2
import test2 as t2
import time
from threading import  Thread, Lock
import jieba
import you_get
import moviepy.editor as me
import requests
import linecache
import webbrowser
import collections
import jieba.analyse
import jieba.posseg
from datetime import datetime, timedelta
from sklearn.externals import joblib

#登陆界面
class Login():

    def __init__(self):
        self.log = QUiLoader().load('Login1.ui')
        self.log.pushButton.clicked.connect(self.open_Main)
        self.log.pushButton_2.clicked.connect(self.closeW)

    def open_Main(self):
        user = self.log.lineEdit.text()
        passw = self.log.lineEdit_2.text()
        if user == 'user' and passw == '123':
            self.mw = News_Analysis()
            #self.mw.ui.setWindowOpacity(0.9)
            self.mw.ui.resize(1500, 900)
            self.mw.ui.setStyleSheet("#Form{border-image:url(2.png)}")
            self.mw.ui.show()
            self.closeW()
        else:
            Box = QMessageBox()
            Box.setWindowTitle('提示')
            Box.setText('请输入正确账号密码')
            Box.exec_()

    def closeW(self):
        self.log.close()

#功能界面
class News_Analysis():

    def __init__(self):
        self.ui = QUiLoader().load('Main1.ui')

        self.label_map = ['财经', '彩票', '房产', '股票', '家居',
                     '教育', '科技', '社会', '时尚', '时政',
                     '体育', '星座', '游戏', '娱乐']
        self.channel_way = {'1':'新闻', '2':'经济', '3':'体育', '4':'科教'}
        self.sort_way = {'热点': 'relevance', '实时': 'date'}
        self.head = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/80.0.3987.149 Safari/537.36'}

        #self.Classed = 0

        self.V_page = 0
        self.News_page = 0   #实时新闻页
        self.Search_page = 1 #检索页
        self.flag = 0   #实时新闻是否以及执行
        self.flag1 = 0  #检索是否执行

        self.Vsort = 0

        self.V_title, self.V_show, self.V_imgs  = self.Get_V()
        #print(self.V_title)
        #print(self.V_show)


        self.A_Pid = QtCharts.QPieSeries()
        self.A_Pid1 = QtCharts.QPieSeries()
        self.Chart_P = QtCharts.QChart()


        self.ui.pushButton.clicked.connect(self.Get_channel)
        self.ui.pushButton.clicked.connect(self.Hot_News)
        self.ui.pushButton.clicked.connect(self.Date_News)

        self.ui.pushButton_2.clicked.connect(self.Get_channel)
        self.ui.pushButton_2.clicked.connect(self.S_News)
        self.ui.pushButton_2.clicked.connect(self.Show_pid)

        self.ui.pushButton_3.clicked.connect(self.V_Previous)
        self.ui.pushButton_4.clicked.connect(self.Web_V)
        self.ui.pushButton_5.clicked.connect(self.V_Next)
        self.ui.pushButton_6.clicked.connect(self.N_Previous)
        self.ui.pushButton_7.clicked.connect(self.N_Next)
        self.ui.pushButton_8.clicked.connect(self.Search_V)
        self.ui.pushButton_9.clicked.connect(self.Web_sea)
        self.ui.pushButton_17.clicked.connect(self.Sea_Previous)
        self.ui.pushButton_18.clicked.connect(self.Sea_Next)
        self.ui.pushButton_10.clicked.connect(self.Open_DownV)

        '''
        if self.Classed == 0:
            self.ui.pushButton.clicked.connect(self.Class_News)
        '''

    def V_Previous(self):

        if self.V_page > 0:
            self.V_page -= 1
        else:
            self.V_page = 0

        name = r'V.jpg'
        html = requests.get(url='https:' + self.V_imgs[self.V_page], headers=self.head)
        with open(name, 'wb') as f:
            f.write(html.content)

        pix = QPixmap(name)
        self.ui.label_6.setPixmap(pix)
        self.ui.lineEdit.clear()
        self.ui.lineEdit.setText(self.V_title[self.V_page])

    def V_Next(self):

        if self.V_page < 5:
            self.V_page += 1
        else:
            self.V_page = 5

        name = r'V.jpg'
        html = requests.get(url='https:' + self.V_imgs[self.V_page], headers=self.head)
        with open(name, 'wb') as f:
            f.write(html.content)

        pix = QPixmap(name)
        self.ui.label_6.setPixmap(pix)
        self.ui.lineEdit.clear()
        self.ui.lineEdit.setText(self.V_title[self.V_page])

    def Web_V(self):
        webbrowser.open(url=self.V_show[self.V_page], new=1, autoraise=True)

    def N_Previous(self):
        if self.flag == 1:
            if self.News_page > 0:
                self.News_page -= 1
            else:
                self.News_page = 0

            html = requests.get(url=self.N_img[self.News_page], headers=self.head)
            with open('News.jpg', 'wb') as f:
                f.write(html.content)
            pix = QPixmap(r'News.jpg')
            pix = pix.scaled(self.ui.label_7.size(), Qt.KeepAspectRatio)
            self.ui.label_7.setScaledContents(True)
            self.ui.label_7.setPixmap(pix)
            self.ui.lineEdit_2.clear()
            self.ui.lineEdit_2.setText(self.N_title[self.News_page])
            self.ui.textEdit_5.clear()
            self.ui.textEdit_5.append(self.N_content[self.News_page] + '\n')
            self.ui.textEdit_5.append( '类别: ' + self.label_map[self.N_resp[self.News_page] - 1] + '  情感倾向: ' + self.S_list[self.News_page])
            self.ui.textEdit_5.append(self.N_time[self.News_page])
            self.ui.label_8.setText(str(self.News_page + 1) + '/10')

    def N_Next(self):
        if self.flag == 1:
            if self.News_page < 9:
                self.News_page += 1
            else:
                self.News_page = 9

            html = requests.get(url=self.N_img[self.News_page], headers=self.head)
            with open('News.jpg', 'wb') as f:
                f.write(html.content)
            pix = QPixmap(r'News.jpg')
            pix = pix.scaled(self.ui.label_7.size(), Qt.KeepAspectRatio)
            self.ui.label_7.setScaledContents(True)
            self.ui.label_7.setPixmap(pix)
            self.ui.lineEdit_2.clear()
            self.ui.lineEdit_2.setText(self.N_title[self.News_page])
            self.ui.textEdit_5.clear()
            self.ui.textEdit_5.append(self.N_content[self.News_page] + '\n')
            self.ui.textEdit_5.append( '类别: ' + self.label_map[self.N_resp[self.News_page] - 1] + '  情感倾向: ' + self.S_list[self.News_page])
            self.ui.textEdit_5.append(self.N_time[self.News_page])

            self.ui.label_8.setText(str(self.News_page+1)+'/10')

    def Sea_Previous(self):
        if self.flag1 == 1:
            if self.Vsort == 1:
                if self.Search_page > 1:
                    self.Search_page -= 1
                else:
                    self.Search_page = 1

                res = self.Vres[self.Search_page-1]

                path1 = 'src\\' + res[1] + r'\url.txt'
                path2 = 'src\\' + res[1] + r'\News.txt'
                path3 = 'data\\' + res[1] + r'\Detail.txt'
                path4 = 'src\\' + res[1] + r'\Cover.jpg'


            elif self.Vsort == 2:

                if self.Search_page > 0:
                    self.Search_page -= 1
                else:
                    self.Search_page = 1

                res = self.Vres[self.Search_page - 1]

                path1 = 'src\\' + res[0] + r'\url.txt'
                path2 = 'src\\' + res[0] + r'\News.txt'
                path3 = 'data\\' + res[0] + r'\Detail.txt'
                path4 = 'src\\' + res[0] + r'\Cover.jpg'


            vurl = linecache.getline(path1, 1).strip()
            self.Vurl = vurl
            vtitle = linecache.getline(path1, 2).strip()
            vtime = linecache.getline(path1, 3).strip()
            vtype = linecache.getline(path3, 15).strip()
            vemotion = linecache.getline(path3, 18).strip()
            vkw = linecache.getline(path3, 19).strip()
            with open(path2, 'r', encoding='utf-8') as fr:
                vcontent = fr.read().replace("\t", "").replace("\n", "").strip()

            #self.ui.textEdit_6.setOpenLinks(False)
            print(path4)
            pix = QPixmap(path4)
            pix = pix.scaled(self.ui.label_16.size(), Qt.KeepAspectRatio)
            self.ui.label_16.setScaledContents(True)
            self.ui.label_16.setPixmap(pix)

            self.ui.textEdit_6.clear()
            self.ui.textEdit_6.append("<h2>" + vtitle + "</h2>")
            self.ui.textEdit_6.append("\n<h3>内容: </h3>" + vcontent)
            self.ui.textEdit_6.append('\n时间: ' + vtime)
            self.ui.textEdit_6.append('\nurl: ' + "<a href='" + vurl + "'>" + vurl + "</a>")
            self.ui.textEdit_6.append('\n类别: ' + vtype + '\t情感极性: ' + vemotion)
            self.ui.textEdit_6.setTextColor(QColor(255, 187, 153))
            self.ui.textEdit_6.append('\n关键词: ' + vkw)
            self.ui.textEdit_6.setTextColor(QColor(255, 255, 255))
            self.ui.label_31.setText(str(self.Search_page) + '/' + str(len(self.Vres)))

    def Sea_Next(self):
        if self.flag1 == 1:
            res_len = len(self.Vres)

            if self.Vsort == 1:
                if self.Search_page < res_len:
                    self.Search_page += 1
                else:
                    self.Search_page = res_len

                res = self.Vres[self.Search_page - 1]

                path1 = 'src\\' + res[1] + r'\url.txt'
                path2 = 'src\\' + res[1] + r'\News.txt'
                path3 = 'data\\' + res[1] + r'\Detail.txt'
                path4 = 'src\\' + res[1] + r'\Cover.jpg'

            elif self.Vsort == 2:

                if self.Vsort == 1:
                    if self.Search_page < res_len:
                        self.Search_page += 1
                    else:
                        self.Search_page = res_len

                res = self.Vres[self.Search_page - 1]

                path1 = 'src\\' + res[0] + r'\url.txt'
                path2 = 'src\\' + res[0] + r'\News.txt'
                path3 = 'data\\' + res[0] + r'\Detail.txt'
                path4 = 'src\\' + res[0] + r'\Cover.jpg'


            vurl = linecache.getline(path1, 1).strip()
            self.Vurl = vurl
            vtitle = linecache.getline(path1, 2).strip()
            vtime = linecache.getline(path1, 3).strip()
            vtype = linecache.getline(path3, 15).strip()
            vemotion = linecache.getline(path3, 18).strip()
            vkw = linecache.getline(path3, 19).strip()
            with open(path2, 'r', encoding='utf-8') as fr:
                vcontent = fr.read().replace("\t", "").replace("\n", "").strip()

            #self.ui.textEdit_6.setOpenLinks(False)
            print(path4)
            pix = QPixmap(path4)
            pix = pix.scaled(self.ui.label_16.size(), Qt.KeepAspectRatio)
            self.ui.label_16.setScaledContents(True)
            self.ui.label_16.setPixmap(pix)

            self.ui.textEdit_6.clear()
            self.ui.textEdit_6.append("<h2>" + vtitle + "</h2>")
            self.ui.textEdit_6.append("\n<h3>内容: </h3>" + vcontent)
            self.ui.textEdit_6.append('\n时间: ' + vtime)
            self.ui.textEdit_6.append('\nurl: ' + "<a href='" + vurl + "'>" + vurl + "</a>")
            self.ui.textEdit_6.append('\n类别: ' + vtype + '\t情感极性: ' + vemotion)
            self.ui.textEdit_6.setTextColor(QColor(255, 187, 153))
            self.ui.textEdit_6.append('\n关键词: ' + vkw)
            self.ui.textEdit_6.setTextColor(QColor(255, 255, 255))
            self.ui.label_31.setText(str(self.Search_page) + '/' + str(len(self.Vres)))

    def Web_sea(self):
        webbrowser.open(url=self.Vurl, new=1, autoraise=True)

    def Get_V(self):

        url1 = r'https://v.cctv.com/index.shtml'

        i = 0
        while i < 3:
            try:
                time.sleep(0.5)
                html1 = requests.post(url1, verify=False, headers=self.head)
                html1.raise_for_status()
                html1.close()
                break
            except Exception as e:
                # logger.error(e)
                print(e)
                i += 1

        html1.encoding = html1.apparent_encoding
        V_img = re.findall('src="(.*)?" data-src', html1.text)
        V_title = re.findall('text"><p>(.*)?</p></div>', html1.text)
        V_show = re.findall('<a href="(.*)?" target="_blank">', html1.text)

        name = r'V.jpg'
        html = requests.get(url='https:'+ V_img[0], headers = self.head )
        with open(name, 'wb') as f:
            f.write(html.content)

        pix = QPixmap(r'V.jpg')
        self.ui.label_6.setScaledContents(True)
        self.ui.label_6.setPixmap(pix)
        self.ui.lineEdit.setText(V_title[self.V_page])


        return V_title, V_show[25:31], V_img[0:6]

    #分析要获取的来源
    def Get_channel(self):
        self.channel = self.ui.comboBox.currentText()
        print(self.channel)

    #获取新闻爬虫
    def Get_News(self, sort, page, channel=''):

        if channel == '':
            url = u"https://search.cctv.com/search.php?qtext=疫情&page=1&type=web&sort=" + self.sort_way[
                sort] + "&datepid=1&channel=" + self.channel + "&vtime=-1&page=" + page
        else:
            url = u"https://search.cctv.com/search.php?qtext=疫情&page=1&type=web&sort=" + self.sort_way[
                sort] + "&datepid=1&channel=" + channel + "&vtime=-1&page=" + page

        head = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/80.0.3987.149 Safari/537.36'}

        i = 0
        while i < 3:
            try:
                time.sleep(0.5)
                html = requests.post(url, verify=False, headers=head)
                html.raise_for_status()
                html.close()
                break
            except Exception as e:
                # logger.error(e)
                print(e)
                i += 1
            else:
                # print(html.text)
                print("html_ok")

        html.encoding = html.apparent_encoding

        t_word = re.findall('="_blank">(.*)?</a>', html.text)
        t_word = {}.fromkeys(t_word).keys()
        t_word = list(t_word)
        # print(html.text)
        con_word = re.findall('(.*)?		                        						</p>', html.text)
        News_time = re.findall('tim">(.*)?</span>', html.text)
        imgs_url = re.findall(';" src="(.*)?" onload', html.text) #图片获取

        title = []
        content = []

        if page == '1':
            flag = 2
        else:
            flag = 0

        #print(len(t_word))
        #print(t_word)

        for i in range(len(t_word)-3):
            temp = t_word[i + 1 + flag].replace('<font color="red">', '')
            # print(temp.replace('</font>', ''))
            title.append(temp.replace('</font>', '').replace('&ldquo;', '"').replace('&rdquo;', '"'))
            temp1 = con_word[i].replace('<font color="red">', '').replace("\t", '').replace('&mdash;','-').replace('&hellip;','...').strip()
            content.append(temp1.replace('</font>', '').replace('\u3000', '').replace('&ldquo;', '"').replace('&rdquo;', '"'))
        return title, content, News_time, imgs_url

    #情感分析
    def S_analysis(self, content):

        S_classifier = joblib.load("S_clf_model.m")
        S_tf = joblib.load('S_tf_model.m')
        S_tests = []


        for x in content:
            # print(x)
            S_word = jieba.analyse.extract_tags(x, topK=20, withWeight=False,
                                                allowPOS=('nz','a', 'an', 'ad', 'e', 'i', 'v', 'vi', 'y', 'z'))
            # allowPOS=('n','nr','ns', 'nt', 'nz', 'q', 'tg')( 'n', 'nz', 'a', 'an', 'e', 'i', 'v', 'vi')
            S_line = ' '.join(S_word)
            S_tests.append(S_line)

        print(S_tests)

        S_proba = S_classifier.predict_proba(S_tf.transform(S_tests))

        s0_list = []
        s1_list = []

        for x in range(len(S_proba)):
            s0 = float(S_proba[x][0])
            s1 = float(S_proba[x][1])

            s0_list.append(round(s0, 5))
            s1_list.append(round(s1, 5))

        return s0_list, s1_list

    #类别分析
    def Class_analysis(self, content, title):
        # 分类
        classifier = joblib.load("clf_model.m")  # 加载训练模型
        tf = joblib.load('tf_model.m')

        tests = []
        l_tests = []

        for x in content:

            key_word = jieba.analyse.extract_tags(x, topK=15, withWeight=False,
                                                  allowPOS=('n', 'nr', 'nz', 'an', 'q','i', 'z'))
            line = ' '.join(key_word)
            tests.append(line)

            '''
            line_t = ' '.join(local_word)
            l_tests.append(line_t)
            
        print(l_tests)'''
        #print("------------")
        #print(tests)

        res_predict = classifier.predict(tf.transform(tests))
        res_predict = list(res_predict)
        #print(res_predict)

        return tests, res_predict

    #地区分析
    def Local_analysis(self, content, title):
        local_w = ['全国/全球' for i in range(len(content))]
        #print(local_w)
        #print('$$$$$$$$$$$$')
        flag = 0
        for y in content:
            local_word = jieba.posseg.cut(y, HMM=False)
            for x in local_word:
                if x.flag == 'ns' and len(x.word) >= 2:
                    local_w[flag] = x.word
                    #print(x.word)
                    break
            flag += 1
            #print('////////')
        print(local_w)
        return local_w

    #热点新闻
    def Hot_News(self):
        page = '1'
        title, content, News_time, imgs_url = self.Get_News(sort='热点', page=page)
        local_w = self.Local_analysis(content=content, title=title)
        tests, res_predict = self.Class_analysis(content=content, title=title)

        #热度计算
        hot_res = collections.Counter(res_predict) #得到字典
        #print('Hot_new')
        #print(res_predict)

        self.ui.textEdit.clear()
        for x in range(len(content)):
            i = (hot_res[res_predict[x]]*6)/(x+1)
            self.ui.textEdit.append("<h3>"+ str(x+1) + '.\t' + title[x] + "</h3>")
            self.ui.textEdit.append('\t' + '类别: '+ self.label_map[res_predict[x]-1] +',  地区: ' + local_w[x] )
            self.ui.textEdit.setTextColor(QColor(255, 190-int(i*2), 83))
            self.ui.textEdit.append('\t' + '热度: ' + str(round(i, 3)) + '\n')
            self.ui.textEdit.setTextColor(QColor(255, 255, 255))

    #实时新闻
    def Date_News(self):
        page = '1'
        title, content, News_time, imgs_url = self.Get_News(sort='实时', page=page)

        local_w = self.Local_analysis(content=content, title=title)
        tests, res_predict = self.Class_analysis(content=content, title=title)
        s0_list, s1_list = self.S_analysis(content=content)

        self.ui.textEdit_2.clear()
        for x in range(len(content)):
            self.ui.textEdit_2.append("<h3>"+ str(x+1) + '.\t' + title[x] + "</h3>")
            self.ui.textEdit_2.append('\t' + '类别: '+ self.label_map[res_predict[x]-1] +',  地区: ' + local_w[x])
            self.ui.textEdit_2.append('\t' + News_time[x] + '\n')

        s_list = []

        for i in range(len(s0_list)):
            temp = abs(s0_list[i]-s1_list[i])
            if round(temp, 2) >= 0.30:
                if s0_list[i] > s1_list[i]:
                    s_list.append('偏消极')
                else:
                    s_list.append('偏积极')
            else:
                s_list.append('中立')

        #放入全局
        self.N_title = title
        self.N_content = content
        self.N_time = News_time
        self.N_img = imgs_url
        self.S_list = s_list
        self.N_resp = res_predict


        html = requests.get(url=self.N_img[0], headers=self.head)
        with open('News.jpg', 'wb') as f:
            f.write(html.content)

        pix = QPixmap(r'News.jpg')
        pix = pix.scaled(self.ui.label_7.size(), Qt.KeepAspectRatio)
        self.ui.label_7.setScaledContents(True)
        self.ui.label_7.setPixmap(pix)
        self.ui.lineEdit_2.setText(self.N_title[0])
        self.ui.textEdit_5.clear()
        self.ui.textEdit_5.append(content[0] + '\n')
        self.ui.textEdit_5.append('类别: '+ self.label_map[res_predict[0]-1] + '  情感倾向: ' + s_list[0])
        self.ui.textEdit_5.append(News_time[0])

        self.ui.label_8.setText('1/10')
        self.Classed = 0

        self.flag = 1

    #Top10分析
    def S_News(self):
        page = '1'
        title1, content1, News_time1, imgs_url1 = self.Get_News(sort='实时', page=page, channel='')
        page = '2'
        title2, content2, News_time2, imgs_url2 = self.Get_News(sort='实时', page=page, channel='')
        page = '3'
        title3, content3, News_time3, imgs_url3 = self.Get_News(sort='实时', page=page, channel='')
        page = '4'
        title4, content4, News_time4, imgs_url4 = self.Get_News(sort='实时', page=page, channel='')

        title = title1 + title2 + title3 + title4
        content = content1 + content2 + content3 + content4
        imgs_url =  imgs_url1 + imgs_url2 + imgs_url3 + imgs_url4

        s0_list, s1_list = self.S_analysis(content=content)
        local_w = self.Local_analysis(content=content, title=title)
        tests, res_predict  = self.Class_analysis(content=content, title=title)

        #print(s0_list)
        #print(s1_list)
        s0_map = []
        s1_map = []
        Inf = 0

        for i in range(10):
            s1_map.append(s1_list.index(max(s1_list)))
            s1_list[s1_list.index(max(s1_list))] = Inf
            s0_list[s1_list.index(max(s1_list))] = Inf


        for i in range(10):
            #print(s0_list.index(max(s0_list)))
            s0_map.append(s0_list.index(max(s0_list)))
            s1_list[s0_list.index(max(s0_list))] = Inf
            s0_list[s0_list.index(max(s0_list))] = Inf

        self.ui.textEdit_3.clear()
        self.ui.textEdit_4.clear()

        for i in range(10):
            word1 = tests[s1_map[i]].split()
            word0 = tests[s0_map[i]].split()
            self.ui.textEdit_3.append("<h3>" + str(i + 1) + '.\t' + title[s1_map[i]] + "</h3>")
            self.ui.textEdit_3.append('\t' + '类别: ' + self.label_map[res_predict[s1_map[i]]-1] + ',  地区: ' +  local_w[s1_map[i]])
            self.ui.textEdit_3.setTextColor(QColor(255, 187, 153))
            self.ui.textEdit_3.append('\t' + '敏感词: ' + word1[0] + '、' + word1[1]  +'\n')
            self.ui.textEdit_3.setTextColor(QColor(255, 255, 255))


            self.ui.textEdit_4.append("<h3>" + str(i + 1) + '.\t' + title[s0_map[i]] + "</h3>")
            self.ui.textEdit_4.append('\t' + '类别: ' + self.label_map[res_predict[s1_map[i]]-1] + ',  地区: ' +  local_w[s0_map[i]])
            self.ui.textEdit_4.setTextColor(QColor(255, 187, 153))
            self.ui.textEdit_4.append('\t' + '敏感词: ' + word0[0] + '、' + word0[1]  +'\n')
            self.ui.textEdit_4.setTextColor(QColor(255, 255, 255))


        #百分比图绘制
        sub = [0 for i in range(14)]
        # print(sub)

        for i in range(len(res_predict)):
            sub[res_predict[i] - 1] += 1

        self.A_Pid.clear()
        for i in range(14):
            if sub[i] > 1:
                self.A_Pid.append(self.label_map[i], sub[i])

        # 敏感信息监测
        self.Sensitive_News(key_word=tests)

    #总体敏感词汇
    def Sensitive_News(self, key_word):
        All = []
        for i in range(len(key_word)):
            All += key_word[i].split()
        #print(All)
        All_res = collections.Counter(All)
        print(All_res.most_common(5))
        self.A_Pid1.clear()
        for y in All_res.most_common(5):
            temp = y[0] +':'+ str(round(y[1]/40, 2))
            self.A_Pid1.append( temp, y[1])

    #新闻检索模块(已经停下)
    def Search_News(self):

        datepid_map = {'不限': 1, '一天内': 2, '一周内': 3, '一月内': 4,'一年内': 5}
        sort_map = {'相关度': 'relevance', '时间': 'date'}
        channel_check = self.ui.buttonGroup.checkedButton()
        datepid_check = self.ui.buttonGroup_2.checkedButton()
        sort_check = self.ui.buttonGroup_3.checkedButton()

        print(sort_check)

        channel = ''

        text = self.ui.lineEdit_3.text()
        if text == '':
            text = '全球'

        if sort_check == None:
            sort = 'date'
        else:
            sort = sort_map[sort_check.text()]

        if datepid_check == None:
            datepid = '1'
        else:
            datepid = str(datepid_map[datepid_check.text()])

        if channel == '不限' or channel_check == None:
            channel = ''
        else:
            channel = channel_check.text()

        page = str(self.Search_page)

        url = r'https://search.cctv.com/search.php?qtext=' + text + '&page=' + page + '&type=web&sort='+ sort +'&datepid=' + datepid + '&channel=' + channel + '&vtime=-1'

        print(url)
        print(page)
        i = 0
        while i < 3:
            try:
                time.sleep(0.5)
                html = requests.post(url, verify=False, headers=self.head)
                html.raise_for_status()
                html.close()
                break
            except Exception as e:
                # logger.error(e)
                print(e)
                i += 1
            else:
                # print(html.text)
                print("html_ok")

        html.encoding = html.apparent_encoding
        # print(html.text)
        t_word = re.findall('="_blank">(.*)?</a>', html.text)
        t_word = {}.fromkeys(t_word).keys()
        t_word = list(t_word)

        con_word = re.findall('(.*)?		                        						</p>', html.text)
        News_time = re.findall('tim">(.*)?</span>', html.text)

        title = []
        content = []

        if page == '1':
            flag = 2
        else:
            flag = 0

        print(len(t_word))
        print(len(con_word))
        print(t_word)
        print(con_word)
        self.ui.textEdit_6.clear()
        if len(con_word) == (len(t_word)-flag-1):
            for i in range(len(t_word)-1-flag):
                temp = t_word[i + 1 + flag].replace('<font color="red">', '')
                # print(temp.replace('</font>', ''))
                title.append(temp.replace('</font>', '').replace('&ldquo;', '"').replace('&rdquo;', '"'))
                temp1 = con_word[i].replace('<font color="red">', '').replace("\t", '').replace('&mdash;', '-').replace('&hellip;','...').strip()
                content.append(temp1.replace('</font>', '').replace('\u3000', '').replace('&ldquo;', '"').replace('&rdquo;', '"'))

            for i in range(len(content)):
                self.ui.textEdit_6.append(str(i + 1) + '.  ' + title[i])
                self.ui.textEdit_6.append('简介:  ' + content[i])
                self.ui.textEdit_6.append(News_time[i] + '\n')



        else:
            self.ui.textEdit_6.append('查找不到/获取失败，请尝试别的条件')
            print('查找不到')
        self.ui.label_31.setText(str(page) + '/5')
        self.flag1 = 1
        print(len(title))
        print(len(content))
        print(title)
        print(content)

    #视频新闻检索模块
    def Search_V(self):

        datepid_map = {'不限': 1, '一天内': 2, '一周内': 3, '一月内': 4}
        sort_map = {'相关度': 'relevance', '时间': 'date'}
        channel_check = self.ui.buttonGroup.checkedButton() #类型
        datepid_check = self.ui.buttonGroup_2.checkedButton() #时间范围
        sort_check = self.ui.buttonGroup_3.checkedButton()  #排序方式

        text = self.ui.lineEdit_3.text()  #查找的关键字

        if text == '':
            Box = QMessageBox()
            Box.setWindowTitle('提示')
            Box.setText('请输入关键词')
            Box.exec_()
            return 0

        if  channel_check == None:
            channel = ''
        elif channel_check.text() == '不限':
            channel = ''
        else:
            channel = channel_check.text()

        if datepid_check == None:
            datepid = 1
        else:
            datepid = datepid_map[datepid_check.text()]


        if sort_check == None:
            sort = 'date'
        else:
            sort = sort_map[sort_check.text()]

        s_files = os.listdir('src')  # 返回指定文件夹的列表名
        s_files.sort(key=lambda x: int(x))
        src_path = 'src\\'
        data_path = 'data\\'

        now = datetime.now()
        if datepid == 1:
            delta = timedelta(days=365)
        elif datepid == 2:
            delta = timedelta(days=1)
        elif datepid == 3:
            delta = timedelta(days=7)
        elif datepid == 4:
            delta = timedelta(days=30)

        #统计整体时间
        all_dir = {}

        for i in range(len(s_files)):
            path = src_path + s_files[i] + '\\url.txt'
            V_time = linecache.getline(path, 3)
            all_dir[V_time] = s_files[i]
        #print(all_dir)



        key_words = text.split()  # 转化为list
        key_num = len(key_words)

        #统计关键词 相关度
        sub_num = {i: 0 for i in s_files}
        #类型筛选器
        sub_type = {}
        #选出来的时间
        Tsort_V = {}
        #选出来的相关度
        sort_V = {}

        if channel!='': #channel 有选择
            for x in key_words:
                for y in s_files:
                    file_path = data_path + y + r'\Detail.txt'
                    V_keys = linecache.getline(file_path, 19).split()
                    V_type = linecache.getline(file_path, 15).strip()
                    if channel == V_type:
                        sub_type[y] = 1
                    for z in V_keys:
                        if z == x:
                            sub_num[y] += 1
                            break;

            for k in list(sub_num.keys()):
                if sub_num[k] == 0:
                    sub_num.pop(k)

            for k in sub_type:#以频道选出统计词
                if sub_num.get(k):
                    path = src_path + k + '\\url.txt'
                    V_time = linecache.getline(path, 3).strip()
                    n_data = now - delta
                    n_data = n_data.strftime('%Y-%m-%d')
                    if str(n_data) < V_time:#如果在时间范围内
                        Tsort_V[V_time] = k
                        sort_V[k] = sub_num[k]


            print(Tsort_V)
            print(sort_V)

        else: #任意的channal
            for x in key_words:
                for y in s_files:
                    file_path = data_path + y + r'\Detail.txt'
                    V_keys = linecache.getline(file_path, 19).split()
                    for z in V_keys:
                        if z == x:
                            sub_num[y] += 1
                            break;

            for k in list(sub_num.keys()):
                if sub_num[k] == 0:
                    sub_num.pop(k)

            for k in sub_num:
                if sub_num[k] > 0:
                    path = src_path + k + '\\url.txt'
                    V_time = linecache.getline(path, 3).strip()
                    n_data = now - delta
                    n_data = n_data.strftime('%Y-%m-%d')
                    if str(n_data) < V_time: #如果在时间范围内
                        Tsort_V[V_time] = k
                        sort_V[k] = sub_num[k]

            print(Tsort_V)
            print(sort_V)


        self.ui.textEdit_6.clear()

        if sort == 'date':
            if not Tsort_V:
                self.ui.textEdit_6.append('搜索结果为空')
                return 0
            self.Vsort = 1
            self.Vres = sorted(Tsort_V.items(), reverse=True)
            res = self.Vres[0]
            path1 = src_path + res[1] + r'\url.txt'
            path2 = src_path + res[1] + r'\News.txt'
            path3 = data_path + res[1] + r'\Detail.txt'
            path4 = src_path + res[1] + r'\Cover.jpg'


        else:
            self.Vsort = 2
            if not sort_V:
                self.ui.textEdit_6.append('搜索结果为空')
                return 0
            self.Vres = sorted(sort_V.items(), key=lambda x: x[1], reverse=True)
            res = self.Vres[0]
            path1 = src_path + res[0] + r'\url.txt'
            path2 = src_path + res[0] + r'\News.txt'
            path3 = data_path + res[0] + r'\Detail.txt'
            path4 = src_path + res[0] + r'\Cover.jpg'

        vurl = linecache.getline(path1, 1).strip()
        self.Vurl = vurl
        vtitle = linecache.getline(path1, 2).strip()
        vtime = linecache.getline(path1, 3).strip()
        vtype = linecache.getline(path3, 15).strip()
        vemotion = linecache.getline(path3, 18).strip()
        vkw = linecache.getline(path3, 19).strip()

        with open(path2, 'r', encoding='utf-8') as fr:
            vcontent = fr.read().replace("\t", "").replace("\n", "").strip()

        #self.ui.textEdit_6.setOpenLinks(False)
        pix = QPixmap(path4)
        pix = pix.scaled(self.ui.label_16.size(), Qt.KeepAspectRatio)
        self.ui.label_16.setScaledContents(True)
        self.ui.label_16.setPixmap(pix)

        self.ui.textEdit_6.append("<h2>" + vtitle + "</h2>")
        self.ui.textEdit_6.append("\n<h3>内容: </h3>" + vcontent)
        self.ui.textEdit_6.append('\n时间: ' + vtime)
        self.ui.textEdit_6.append('\nurl: ' + "<a href='" + vurl + "'>" + vurl + "</a>")
        self.ui.textEdit_6.append('\n类别: ' + vtype + '\t情感极性: ' + vemotion)
        self.ui.textEdit_6.setTextColor(QColor(255, 187, 153))
        self.ui.textEdit_6.append('\n关键词: ' + vkw)
        self.ui.textEdit_6.setTextColor(QColor(255, 255, 255))
        self.flag1 = 1
        self.Search_page = 1

        self.ui.label_31.setText(str(self.Search_page) + '/' + str(len(self.Vres)))
        #print(vtitle)
        #print(vcontent)
        #print(vtime)

    def Open_DownV(self):
        self.Down = Down_V()
        self.Down.win.show()




    '''
    #类别百分比分析
    def Class_News(self):
        page = '1'
        title1, content1, News_time1 = self.Get_News(sort='实时', page=page, channel='新闻')
        page = '2'
        title2, content2, News_time2 = self.Get_News(sort='实时', page=page, channel='新闻')
        page = '3'
        title3, content3, News_time3 = self.Get_News(sort='实时', page=page, channel='新闻')
        page = '4'
        title4, content4, News_time4 = self.Get_News(sort='实时', page=page, channel='新闻')

        title = title1 + title2 + title3 + title4
        content = content1 + content2 + content3 + content4

        #类别分析
        tests, res_predict = self.Class_analysis(content=content,title=title)
        sub = [0 for i in range(14)]
        # print(sub)

        for i in range(len(res_predict)):
            sub[res_predict[i] - 1] += 1

        self.A_Pid.clear()
        for i in range(14):
            if sub[i] > 1:
                self.A_Pid.append(self.label_map[i], sub[i])

        #敏感信息监测
        self.Sensitive_News(key_word=tests)
        self.Classed = 1

    '''
    def Show_pid(self):
        '''
        if self.Classed == 0:
            self.Class_News()
        '''
        self.A_Pid.setPieSize(0.8)
        self.A_Pid.setHoleSize(0.7)
        self.A_Pid1.setPieSize(0.3)
        self.A_Pid.setLabelsVisible()
        self.A_Pid1.setLabelsVisible()

        '''
        self.slices.setPen(QPen(Qt.yellow, 1))  # 设置画笔类型
        self.slices.setBrush(Qt.yellow)  # 设置笔刷
        '''
        self.Chart_P.addSeries(self.A_Pid)
        self.Chart_P.addSeries(self.A_Pid1)
        self.Chart_P.setTitle('类别统计及敏感信息')

        self.ChartView_P = QtCharts.QChartView(self.Chart_P)
        self.ChartView_P.setRenderHint(QPainter.Antialiasing)
        self.ChartView_P.setWindowTitle('A_News_Pid')
        self.ChartView_P.resize(800, 800)
        self.ChartView_P.show()


class Down_V():

    def __init__(self):
        self.win = QUiLoader().load('Down_V.ui')
        self.win.pushButton.clicked.connect(self.Web_Get)
        self.src_dir_num = len(os.listdir('src'))

    def Analysis_txt(self, file_path):

        label_map = {'__label__财经': 1, '__label__彩票': 2, '__label__房产': 3, '__label__股票': 4, '__label__家居': 5,
                     '__label__教育': 6, '__label__科技': 7, '__label__社会': 8, '__label__时尚': 9, '__label__时政': 10,
                     '__label__体育': 11, '__label__星座': 12, '__label__游戏': 13, '__label__娱乐': 14}

        # 输出测试数据
        t_name = []
        t_num = []

        # 构建tag_name
        for i in label_map.keys():
            t_name.append(i.strip('__label__'))
            t_num.append(int(label_map[i]))

        Num_map = dict(zip(t_num, t_name))


        self.win.textEdit.append('分析中...')

        classifier = joblib.load("clf_model.m")  # 加载训练模型
        tf = joblib.load('tf_model.m')

        S_classifier = joblib.load("S_clf_model.m")
        S_tf = joblib.load('S_tf_model.m')

        Text_path = file_path + r'\News.txt'

        with open(Text_path,'r', encoding='utf-8') as f:
            file_text  = f.read()

        key_word = jieba.analyse.extract_tags(file_text.replace("\t", "").replace("\n", ""), topK=20, withWeight=False,
                                              allowPOS=('n', 'nr', 'ns', 'nt', 'nz', 'q', 'tg'))

        S_word = jieba.analyse.extract_tags(file_text.replace("\t", "").replace("\n", ""), topK=20, withWeight=False,
                                            allowPOS=('n', 'nz', 'a', 'an', 'e', 'i', 'v', 'vi'))

        outline = ' '.join(key_word)  # 提取新闻文本关键词
        S_line = ' '.join(S_word)

        tests = []
        tests.append(outline)

        S_tests = []
        S_tests.append(S_line)

        S_proba = S_classifier.predict_proba(S_tf.transform(S_tests))

        print(S_proba)
        print(S_classifier.predict(S_tf.transform(S_tests)))

        s0 = float(S_proba[0][0])
        s1 = float(S_proba[0][1])

        s0 = round(s0 + 0.005, 2)
        s1 = round(s1 + 0.005, 2)

        S_res = round(abs(s0 - s1), 2)
        S_lable = ''
        if S_res >= 0.37:
            if s0 < s1:
                S_lable = "积极的"
                print("正")
            else:
                S_lable = "消极的"
                print("负")
        else:
            S_lable = "中立的"
            print("中")

        S_list = []
        S_list.append('消极 ' + str(s0))
        S_list.append('积极 ' + str(s1))

        sum = 0.0
        proba = classifier.predict_proba(tf.transform(tests))
        pre_num = int(classifier.predict(tf.transform(tests)))

        t_Name = Num_map.get(pre_num)
        texts = tests[0]

        print(texts)

        for x in range(14):
            num = str(proba[0][x])
            sum += float(num)

        A_list = []
        for i in range(14):
            num = str(proba[0][i])
            name = str(Num_map.get(i + 1))
            # print(type(num))
            persent = int((float(num) / sum) * 100 + 0.5)
            A_list.append(name + ' ' + str(persent) + '%')

        print(proba)
        pre_num = int(classifier.predict(tf.transform(tests)))
        print('预测结果为: %s' % Num_map.get(pre_num))

        path = 'data\\' + str(self.src_dir_num)

        if not os.path.exists(path):
            os.mkdir(path)
        detail_txt = path + '\Detail.txt'

        with open(detail_txt, 'w', encoding='utf-8') as f:
            for x in A_list:
                f.write(x + '\n')

            f.write(t_Name + '\n')
            f.write(S_list[0] + '\n')
            f.write(S_list[1] + '\n')
            f.write(S_lable + '\n')
            f.write(str(texts))

        self.win.textEdit.append('分析完成')
        return texts

    def Web_Get(self):

        head = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/80.0.3987.149 Safari/537.36'}

        self.win.textEdit.clear()
        self.win.textEdit.append('下载中......')

        def Download(url, file_path):
            sys.argv = ['you-get', '-o', file_path, '-O', 'News', url]
            you_get.main()

        def Translate_V(file_path):
            if os.path.exists(file_path):
                file_path_V = file_path + r'\News.mp4'
                file_path_A = file_path + r'\News.wav'

                # print(file_path_V)
                # print(file_path_A)

                video = me.VideoFileClip(file_path_V)
                audio = video.audio
                audio.write_audiofile(file_path_A)

            else:
                print('文件不存在')

        url = self.win.lineEdit.text().strip()

        print(url)

        Apid = '5ee46124'
        Sk = 'f6203dabecc334cf07d5872418bf5c12'


        if url == '':
            Box = QMessageBox()
            Box.windowTitle('提示')
            Box.setText('请输入url')
            Box.exec_()
            return 0

        self.src_dir_num += 1  # 文件个数

        file_path = 'src\\' + str(self.src_dir_num)  # 重要

        if not os.path.exists(file_path):
            os.mkdir(file_path)
        else:
            os.system('cd ' + file_path + r' && del /q *')
            print("文件存在")

        Download(url, file_path)
        Translate_V(file_path)

        self.win.textEdit.clear()
        self.win.textEdit.append('下载完成')

        now = datetime.now()

        Vpath = file_path + r'\News.mp4'
        Jpath = file_path + r'\Cover.jpg'

        vidcap = cv2.VideoCapture(Vpath)
        vidcap.set(cv2.CAP_PROP_POS_FRAMES, 100)
        success, image = vidcap.read()
        imag = cv2.imwrite(Jpath, image)

        url_txt = file_path + r'\url.txt'
        

        html = requests.get(url, verify=False)
        html.raise_for_status()
        html.close()
        html.encoding = html.apparent_encoding
        V_title = re.findall('<title>(.*)?</title>', html.text)
        print(V_title)
        with open(url_txt, 'w', encoding='utf-8') as f:
            f.write(url + '\n')
            f.write(V_title[0] + '\n')
            f.write(now.strftime('%Y-%m-%d'))

        '''
        V_title = re.findall('<title>(.*)?</title>', html.text)
        
        url_txt = file_path + r'\\url.txt'

        with open(url_txt, 'w', encoding='utf-8') as f:
            f.write(url)
            f.write(V_title[0])
            f.write(now.strftime('%Y-%m-%d'))
        '''
        try:
            t2.Translate_A(apid=Apid, sk=Sk, pre_fp=file_path)
        except:
            print('xinfei')

        self.Analysis_txt(file_path=file_path)






#app = QApplication(sys.argv)
app = QApplication([])
A = Login()
A.log.setWindowFlag(Qt.FramelessWindowHint)
#A.log.setWindowOpacity(0.9) # 设置窗口透明度
A.log.setAttribute(Qt.WA_TranslucentBackground) #设置窗口背景透明
A.log.show()

'''
vw = QVideoWidget()  # 定义视频显示的widget
vw.show()
player = QMediaPlayer()
player.setVideoOutput(vw)
player.setMedia(QMediaContent(QFileDialog.getOpenFileUrl()[0]))
player.play()
'''
#sys.exit(app.exec_())
app.exec_()