
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

connection = pymysql.connect(host="140.119.80.113", user="user06", passwd="yueboss", db="dbo.CD2010",charset='utf8')

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


# In[1]:

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


# In[ ]:

import pymysql as db
import operator
import time

PORT = 3306
HOST = '140.119.164.170'
USER = 'wcchen'
PASSWORD ='62295'
DB = input('DB = ')
CHARSET = 'UTF8'
USEUNICODE = True


def m():
    table = input('table = ')
    data = database(table)
    print(data)

def database(table):#存取database
    connection = db.Connection(host = HOST, port = PORT, user = USER, passwd = PASSWORD, db = DB, charset = CHARSET, use_unicode = USEUNICODE)
    o = connection.cursor()
    o.execute('SELECT * FROM `%s` WHERE 1' % table)
    raw = o.fetchall()
    return raw

m()


# In[ ]:

import codecs

path = "C:\\Users\\user\\Desktop\\"

count = 1
error = []
file = []
with codecs.open(path+'文藝.csv','rb') as f:
    head = f.readline()
    content = f.readlines()
    
    for i in content:
        try:
            print (count,i.decode('big5').strip())
            file.append(i.decode('big5').strip())
        except:
            print (count)
            error.append(count)
            file.append('')
        count += 1

with codecs.open(path+'temp.txt','wb','utf8') as g:
    for i in file:
        g.write(i+'\r\n')

print (error)        
print ('END')


# In[ ]:

import codecs
import os 

path = "C:\\Users\\user\\Desktop\\"

book = []

file_list = []

for file in os.listdir(path+'雷震處理資料\\source\\雷震日記母體\\'):
    file_list.append(file)
    
with codecs.open(path+'文藝.txt','rb','utf8') as f:
    content = f.readlines()
    
    for line in content:
        line = line.strip()
        
        book.append(line)

size = len(book)

out = []
check = False
        
count = 0
for file in file_list:
    with codecs.open(path+'雷震處理資料\\source\\雷震日記母體\\'+file,'rb','utf8') as f:
        head = f.readline()
        for i in book:
            if i.split(',')[0] in head and i.split(',')[1] in head:
                if i in out:
                    check = True
                else:
                    out.append(i)
                print (i)
                count += 1
                break

for i in book:
    if i not in out:
        print ('error',i)
print (check,count,len(out))


# In[ ]:

#http://www.jerrynest.com/python-get-ubike-opendata/
#http://learn4rookie.blogspot.tw/2016/03/python-youbike.html
import urllib.request
import gzip
import json
#from pprint import pprint
url = "http://data.taipei/youbike"
urllib.request.urlretrieve(url, "data.gz")
f = gzip.open('data.gz', 'r')
jdata = f.read()
f.close()
data = json.loads(jdata.decode('utf8'))
for key,value in data["retVal"].items():
    sno = value["sno"]
    sna = value["sna"]
    print ("NO." + sno + " " + sna)


# In[ ]:

import os
import codecs

from ipywidgets import IntProgress
from IPython.display import display


path = "C:\\Users\\user\\Desktop\\課業相關\\論文資料\\SCS\\"
out_path = "C:\\Users\\user\\Desktop\\SCS2\\"

file_list = []

for file in os.listdir(path):
    file_list.append(file)
    

p = IntProgress()
p.max = len(file_list)
p.description = 'start'
display(p)
count = 0

for file in file_list:
    with codecs.open(path+file,'rb','utf8') as f:
        title = f.readline()
        content = f.readlines()
        
        with codecs.open(out_path+file,'wb','utf8') as g:
            g.write(title.strip()+'\r\n')
            
            second_line = []
            
            for line in content:
                
                try:
                    line = line.strip()
                    words = line.split()

                    #check = False

                    temp = []

                    for word in words:
                        if len(word.split('[')) > 1 and '+' in word.split('[')[1]:
                            word = word.split('[')[0]
                            #check = True
                        if len(word.split('(')) != 2:
                            #check = True
                            continue
                        
                        temp.append(word)

                    '''if check:
                        print (line)
                        print (' '.join(temp))'''
                    
                    second_line.append(' '.join(temp))

                except:
                    print ('ERROR',line)
                    
            g.write(' '.join(second_line)+'\r\n')
                        
    count = count + 1
    p.value = count
    p.description = str(count)
        
p.description = 'end'


# In[ ]:

import codecs
import os
import time

file_path = "C:\\Users\\user\\Desktop\\raw_txt\\"
out_path = "C:\\Users\\user\\Desktop\\raw_txt2\\"

file_list = []

for file in os.listdir(file_path):
    file_list.append(file)
    
for file in file_list:
    title = ''
    con = ''
    check = False
    with codecs.open(file_path+file,'rb','utf8') as f:
        content = f.readlines()
        
        for i in content:
            i = i.strip()
            if len(i) == 0:
                continue
            elif i[0] == '<':
                if 'DATE' in i and not check and len(con) == 0:
                    title = (i.split('>')[1]).split('<')[0].strip()
                    check = True
            else:
                con = con + i + '。'
    with codecs.open(out_path+file,'wb','utf8') as g:
        g.write(title+'\r\n')
        g.write(con+'\r\n')
print ('END')


# In[ ]:

import codecs
import os
import time
from ckip import CKIPSegmenter, CKIPParser

segmenter = CKIPSegmenter('104753018', 'sayanouta')

file_path = "C:\\Users\\user\\Desktop\\raw_txt3\\"
out_path = "C:\\Users\\user\\Desktop\\raw_txt4\\"

file_list = []

for file in os.listdir(file_path):
    file_list.append(file)
    
for file in file_list:
    with codecs.open(file_path+file,'rb','utf8') as f:
        title = f.readline().strip()
        second = f.readline().strip()
        
        result = []
        error_check = False
        
        '''for i in second.split('。'):
            i = i + '。'
            if i == '。':
                continue
            check = True
            
            while(check):
                check = False
                temper = []
                try:
                    segmented_result = segmenter.process(i)

                    if segmented_result['status_code'] != '0':
                        print ('Process Failed: ' + segmented_result['status'])
                    else:
                        for sentence in segmented_result['result']:
                            for term in sentence:
                                temper.append(term['term'] + '(' + term['pos'] + ')')
                except:
                    print ('*'+i)
                    check = True
                    
                if not check:
                    result += temper
        print (file)
        print (' '.join(result))'''
        
        try:
            segmented_result = segmenter.process(second)

            if segmented_result['status_code'] != '0':
                print ('Process Failed: ' + segmented_result['status'])
            else:
                for sentence in segmented_result['result']:
                    for term in sentence:
                        result.append(term['term'] + '(' + term['pos'] + ')')
        except:
            print ('error',file)
            error_check = True
        
        if error_check:    
            with codecs.open(out_path+'error.txt','ab','utf8') as g:
                g.write(file+'\r\n')
        else:
            with codecs.open(out_path+file,'wb','utf8') as g:
                g.write(title+'\r\n')
                g.write(' '.join(result)+'\r\n')
            print (file)


# In[4]:

import tensorflow as tf
import numpy as np

# 添加层
def add_layer(inputs, in_size, out_size, activation_function=None):
    # add one more layer and return the output of this layer
    Weights = tf.Variable(tf.random_normal([in_size, out_size]))
    biases = tf.Variable(tf.zeros([1, out_size]) + 0.1)
    Wx_plus_b = tf.matmul(inputs, Weights) + biases
    if activation_function is None:
        outputs = Wx_plus_b
    else:
        outputs = activation_function(Wx_plus_b)
    return outputs

# 1.训练的数据
# Make up some real data 
x_data = np.linspace(-1,1,300)[:, np.newaxis]
noise = np.random.normal(0, 0.05, x_data.shape)
y_data = np.square(x_data) - 0.5 + noise

# 2.定义节点准备接收数据
# define placeholder for inputs to network  
xs = tf.placeholder(tf.float32, [None, 1])
ys = tf.placeholder(tf.float32, [None, 1])

# 3.定义神经层：隐藏层和预测层
# add hidden layer 输入值是 xs，在隐藏层有 10 个神经元   
l1 = add_layer(xs, 1, 10, activation_function=tf.nn.relu)
# add output layer 输入值是隐藏层 l1，在预测层输出 1 个结果
prediction = add_layer(l1, 10, 1, activation_function=None)

# 4.定义 loss 表达式
# the error between prediciton and real data    
loss = tf.reduce_mean(tf.reduce_sum(tf.square(ys - prediction),
                     reduction_indices=[1]))

# 5.选择 optimizer 使 loss 达到最小                   
# 这一行定义了用什么方式去减少 loss，学习率是 0.1       
train_step = tf.train.GradientDescentOptimizer(0.1).minimize(loss)


# important step 对所有变量进行初始化
init = tf.global_variables_initializer()
sess = tf.Session()
# 上面定义的都没有运算，直到 sess.run 才会开始运算
sess.run(init)

# 迭代 1000 次学习，sess.run optimizer
for i in range(1000):
    # training train_step 和 loss 都是由 placeholder 定义的运算，所以这里要用 feed 传入参数
    sess.run(train_step, feed_dict={xs: x_data, ys: y_data})
    if i % 50 == 0:
        # to see the step improvement
        print(sess.run(loss, feed_dict={xs: x_data, ys: y_data}))


# In[16]:

import os
import codecs
import logging
from collections import defaultdict

logging.basicConfig(format='%(asctime)s : %(levelname)s : %(message)s', level=logging.INFO)

path = "C:\\Users\\user\\Desktop\\課業相關\\碩士班\\SNA\\meeting\\source\\自由中國\\"

name = ['孟瑤', '徐訏', '朱伴耘', '殷海光', '羅鴻詔', '胡適', '蔣勻田', '陳之藩', '雷震', '龍平甫']

file_list = []

for d in os.listdir(path):
    for file in os.listdir(path+d+'\\'):
        file_list.append(d+'\\'+file)
        
frequency = defaultdict(list)

for file in file_list:
    with codecs.open(path+file,'rb','utf8') as f:
        header = (f.readline().strip()).split()
        
        if len(header) >= 6 and header[5] in name:
            frequency[header[5]].append(file)
            
for item in frequency:
    print (item,frequency[item])


# In[18]:

import codecs
import os

path = "C:\\Users\\user\\Desktop\\"

loc_index = []

with codecs.open(path+'地名2.csv','rb','utf8') as f:
    header = f.readline()
    content = f.readlines()
    
    for line in content:
        for words in (line.strip()).split(','):
            if len(words) != 0:
                for word in words.split('、'):
                    if word not in loc_index and len(word) != 0 and word != ' ':
                        loc_index.append(word)
                        
    
'''with codecs.open(path+'地名.txt','wb','utf8') as g:
    for word in loc_index:
        g.write(word+'\r\n')'''


# In[50]:

from gensim.models import word2vec
import logging

path = "C:\\Users\\user\\Desktop\\"

logging.basicConfig(format='%(asctime)s : %(levelname)s : %(message)s', level=logging.INFO)
sentences = word2vec.Text8Corpus(path+"diary.txt")  # 加载语料
#model2 = word2vec.Word2Vec.load_word2vec_format(path+"diary.model.bin", binary=True)
model = word2vec.Word2Vec(sentences, size=1000)  # 训练skip-gram模型; 默认window=5
model.save_word2vec_format(path+"diary-1000.model.bin", binary=True)


# In[51]:

find = '臺北'
t = model.most_similar(find,topn=30)
print ('和['+find+']最相關的詞有：\n')
for item in t:
    print (item[0],item[1])
t3 = model.similarity('臺北','英雄館')
print (t3)


# In[44]:

from collections import defaultdict

loc_frequency = defaultdict(int)

loc_index = []

with codecs.open(path+'地名.txt','rb','utf8') as f:
    content = f.readlines()
    
    for i in content:
        loc_index.append(i.strip())

for add in loc_index:
    try:
        t = model.most_similar(add,topn=100)
        loc_frequency[add] += 1
        for item in t:
            loc_frequency[item[0]] += 1
    except:
        loc_frequency[add] += 1

print (len(loc_frequency))

sort_words = sorted(loc_frequency.items(), key=lambda d:d[1], reverse = True)

with codecs.open(path+'地名2.txt','wb','utf8') as g:
    for word in sort_words:
        g.write(word[0]+' '+str(word[1])+'\r\n')
        #g.write(word[0]+'\r\n')

