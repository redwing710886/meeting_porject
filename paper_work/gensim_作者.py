
# coding: utf-8

# In[1]:

#抓取特定作者文章
import os
import codecs
from collections import defaultdict

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
print ('END')


# In[10]:

#jieba
import jieba
import time

jieba.load_userdict("dict.txt.big")

stop_word = []

with codecs.open(desktop_path+'stop.txt','rb','utf8') as f:
    stop_word = [line.strip() for line in f.readlines()]

out_path = "C:\\Users\\user\\Desktop\\作者\\"
desktop_path = "C:\\Users\\user\\Desktop\\"

word_frequency = defaultdict(int)

for n in frequency:
    for file in frequency[n]:
        with codecs.open(path+file,'rb','utf8') as f:
            header = f.readline()
            content = (f.readline()).strip()
            text = [word.split('(')[0] for word in content.split()                     if len(word.split('(')) == 2 and word.split('(')[0] not in stop_word                     and 'CATEGORY' not in word.split('(')[1]]
            text = jieba.lcut(''.join(text),cut_all=False)
            for word in text:
                word_frequency[word] += 1 
            
            with codecs.open(out_path+n+'.txt','ab','utf8') as g:
                g.write(' '.join(text)+'\r\n')
print ('END')


# In[2]:

#CKIP
out_path = "C:\\Users\\user\\Desktop\\作者\\"
desktop_path = "C:\\Users\\user\\Desktop\\"

stop_word = []

with codecs.open(desktop_path+'stop.txt','rb','utf8') as f:
    stop_word = [line.strip() for line in f.readlines()]

word_frequency = defaultdict(int)

for n in frequency:
    for file in frequency[n]:
        with codecs.open(path+file,'rb','utf8') as f:
            header = f.readline()
            content = (f.readline()).strip()
            
            text = [word.split('(')[0] for word in content.split()                     if len(word.split('(')) == 2 and word.split('(')[0] not in stop_word                     and 'CATEGORY' not in word.split('(')[1]]
            for word in text:
                word_frequency[word] += 1 
            
            with codecs.open(out_path+n+'.txt','ab','utf8') as g:
                g.write(' '.join(text)+'\r\n')
print ('END')


# In[35]:

#查看作者間之高頻詞
import numpy as np
import matplotlib.pyplot as plt
from collections import OrderedDict

sort_words = sorted(word_frequency.items(), key=lambda d:d[1], reverse = True)
print (len(sort_words))
print (sort_words[:10])

sort_words = OrderedDict(sort_words[:100])

'''condicate = []
count = 0
for item in sort_words:
    if count % 50 == 0:
        #print (item[0],item[1])
        condicate.append(item[0])
    count += 1'''
    
xticks = np.arange(len(sort_words)) + 1
plt.bar(xticks, sort_words.values(), align='center')

#plt.xticks(xticks, list(sort_words.keys()))  
plt.show()


# In[13]:

#訓練word2vec
from gensim.models import word2vec
import logging

logging.basicConfig(format='%(asctime)s : %(levelname)s : %(message)s', level=logging.INFO)

sentences = word2vec.Text8Corpus(out_path+'雷震.txt')  # 加载语料
model = word2vec.Word2Vec(sentences, size=250,hs=1,iter=10)  
model.save_word2vec_format(desktop_path+"author.model.bin", binary=True)


# In[14]:

for i in condicate:
    find = i
    try:
        t = model.most_similar(find,topn=30)
        print ('和['+find+']最相關的詞有：\n')
        for item in t:
            print (item[0],item[1])
        print ('\n')
    except:
        continue

