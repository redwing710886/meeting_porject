
# coding: utf-8

# In[ ]:

import codecs

with codecs.open("C:\\Users\\user\\Desktop\\name_list.txt",'rb','utf8') as f:
    content = f.readlines()
    
    with codecs.open("C:\\Users\\user\\Desktop\\name_list.csv",'wb','utf8') as g:
        
        g.write('名字,學號,信箱\r\n')
    
        for line in content:
            line = line.split()
            
            g.write(line[0]+line[1]+','+str(line[2].split('@')[0])+','+line[2]+'\r\n')
            
print ('END')


# In[ ]:

import pymysql

connection = pymysql.connect(host="127.0.0.1", user="redwing", passwd="", db="word",charset='utf8')

try:
    with connection.cursor() as cursor:
        sql = "SELECT * FROM `word` WHERE `class`='認知-猜測 epistemic-conjecture'" #基本sql指令
        cursor.execute(sql)
        
        #提取出的資料必須以遞迴形式拿出
        for i in cursor:
            print (i)    
finally:
    connection.close()


# In[ ]:

#取出SCS各文本
import xml.etree.ElementTree as ET
import os
import time
import codecs

path = "C:\\Users\\user\\Desktop\\課業相關\\碩士班\\SNA\\meeting\\source\\SCS_4.0\\CKIP\\"
out_path = 'C:\\Users\\user\\Desktop\\article\\'

file_list = []
count = 1

for file in os.listdir(path):
    file_list.append(file)

for file in file_list:
    
    tree = ET.parse(path+file)
    root = tree.getroot()
    
    for article in root.iter('article'):
        with codecs.open(out_path+str(count).zfill(5)+'.txt','wb','utf8') as g:
            if article.find('title').text != None:
                g.write('#'+article.find('title').text+'\r\n')
            #print (article.find('title').text)
            for i in article.find('text').findall('sentence'):
                #print (i.text)
                if i.text != None:
                    g.write(i.text+'\r\n')
            #time.sleep(1)
        count += 1
print ('END')


# In[3]:

import matplotlib
import matplotlib.pyplot as plt 
myfont = matplotlib.font_manager.FontProperties(fname='c:\\windows\\fonts\\msyh.ttc', size=14)

#调节图形大小，宽，高
plt.figure(figsize=(6,9))
#定义饼状图的标签，标签是列表
labels = ['第一部分','第二部分','第三部分']
#每个标签占多大，会自动去算百分比
sizes = [20.5,40.5,38.9]
colors = ['red','yellowgreen','lightskyblue']
#将某部分爆炸出来， 使用括号，将第一块分割出来，数值的大小是分割出来的与其他两块的间隙
explode = (0,0.05,0)

patches,l_text,p_text = plt.pie(sizes,explode=explode,labels=labels,colors=colors,
                                labeldistance = 1.1,autopct = '%3.1f%%',shadow = False,
                                startangle = 90,pctdistance = 0.6)

#labeldistance，文本的位置离远点有多远，1.1指1.1倍半径的位置
#autopct，圆里面的文本格式，%3.1f%%表示小数有三位，整数有一位的浮点数
#shadow，饼是否有阴影
#startangle，起始角度，0，表示从0开始逆时针转，为第一块。一般选择从90度开始比较好看
#pctdistance，百分比的text离圆心的距离
#patches, l_texts, p_texts，为了得到饼图的返回值，p_texts饼图内部文本的，l_texts饼图外label的文本

#改变文本的大小
#方法是把每一个text遍历。调用set_size方法设置它的属性
for t in l_text:
    t.set_size=(30)
    t.set_fontproperties(myfont)
for t in p_text:
    t.set_size=(20)
    #t.set_fontproperties(myfont)
# 设置x，y轴刻度一致，这样饼图才能是圆的
plt.axis('equal')
plt.legend(prop=myfont)
plt.show()

