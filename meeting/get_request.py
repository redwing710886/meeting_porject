
# coding: utf-8

# In[1]:

#建立搜尋詞彙的web網路
import codecs
import os
import jieba
import time
from math import log

import xlrd

class Dictionary():
    
    jieba.set_dictionary('dict.txt.big.txt')
    file_path = '../../desktop/200901/'
    #file_path = '../../desktop/IRdata/'
    d = {}
    all_text = {}
    
    def __init__(self):
        self.make_dic()
        #self.make_rank()
    
    def make_dic(self):
        
        file_list = []

        for file in os.listdir(self.file_path):
            file_list.append(file)     
        
        for file in file_list: 
            with codecs.open(self.file_path+file,'rb','utf-8') as f:
                content = f.read()
                #print (os.path.splitext(file)[0])
                words = jieba.tokenize(content)
                sd = 0
                for word in words:
                    if word[0] not in self.d:
                        self.d[word[0]] = {file:[word[1]]}
                    else:
                        if file not in self.d[word[0]]:
                            self.d[word[0]][file] = [word[1]]
                        else:
                            self.d[word[0]][file].append(word[1])               
                    sd = word[2]
                self.all_text[file] = sd
                            
    def get_dic(self):
        return self.d
                            
    def get_dic_text(self,text):
        if text not in self.d:
            return None
        return self.d[text]  
    
    def get_files(self):
        return self.all_text
    
    def get_file_end(self,text):
        if text not in self.all_text:
            return None
        return self.all_text[text] 

w = Dictionary()

#find = input().split()

find = []
book = xlrd.open_workbook('new.xlsx')
sh = book.sheet_by_index(0)
for rx in range(sh.nrows):
    find.append(sh.cell_value(rowx=rx, colx=0))

if len(find) >= 1:
    mach = []
    exist = []
    for n in find:
        if n in w.get_dic():
            pos = w.get_dic_text(n)
            if len(mach) == 0:
                for i in pos:
                    mach.append(i)
            else:
                temp = []
                for i in pos:
                    if i in mach:
                        temp.append(i)
                mach = temp
            exist.append(n)
    if len(mach) == 0:
        print ('not find')
        
    rr = []
    for l in mach:
        coco = 0
        for n in exist:
            pos = w.get_dic_text(n)
            coco = coco + len(pos[l])
        rr.append((l,coco))
    rr = sorted(rr, key = lambda x : x[1],reverse=True)
    gg = []
    for n in rr:
        gg.append(n[0])
    mach = gg
    
    for x in mach:
        ans = []
        print (x)
        for n in exist:
            pos = w.get_dic_text(n)
            print (n,len(pos[x]))
            for j in pos[x]:
                ans.append((n,j))
        ans = sorted(ans, key = lambda x : x[1])
        print (ans)
        web = []
        web.append('start')
        web.append(str(ans[0][1]))
        for i in range(len(ans)-1):
            web.append(ans[i][0])
            web.append(str(ans[i+1][1]-ans[i][1]))
        web.append(ans[-1][0])
        web.append(str(w.get_file_end(x)-ans[-1][1]))
        web.append('end')
        print ('-'.join(web))
        print ()
                
else:
    print ('error')


# In[ ]:

#excel連結測試
import xlrd

book = xlrd.open_workbook('new.xlsx')

print ("The number of worksheets is", book.nsheets)
print ("Worksheet name(s):", book.sheet_names())
sh = book.sheet_by_index(0)
print (sh.name, sh.nrows, sh.ncols)
print ("Cell D30 is", sh.cell_value(rowx=1, colx=0))
for rx in range(sh.nrows):
    #print (type(sh.row(rx)[0]))
    print (sh.cell_value(rowx=rx, colx=0))


# In[ ]:

#資料庫連接測試
import pymysql

db = pymysql.connect(host="140.119.164.170", user="salan40319", passwd="104753018", db="SinicaCorpus")
cursor = db.cursor()
cursor.execute("SELECT * FROM  `corpus_segpos_31` LIMIT 0 , 30")

for row in cursor:
    print (row[1].decode("utf-8"),'1',row[2][1:-1].decode("utf-8"))
'''a = ''
for row in cursor:
    a = a + row[1].decode("utf-8")
print (a)'''

cursor.close()  
db.close() 


# In[ ]:

#撰寫以聯合資料庫所建立gephi的node和link
import codecs
import os
import re
import jieba
import time

jieba.set_dictionary('dict.txt.big.txt')
#file_path = '../../desktop/200901/'
file_path = '../../desktop/IRdata/'


t = {}
all_text = []

file_list = []

for file in os.listdir(file_path):
    file_list.append(file)     

cc = 1
for file in file_list: 
    with codecs.open(file_path+file,'rb','utf-8') as f:
        content = f.read()
        words = jieba.tokenize(content)
            
        temp = []
        for word in words:
            if re.search(u'[\u4e00-\u9fa5]+',word[0]) and len(word[0]) > 1:
                if word[0] not in temp:
                    temp.append(word[0])
                if word[0] not in all_text:
                    all_text.append(word[0])
        
        temp = sorted(temp)
        t[file] = temp
        if cc % 100 == 0:
            print (cc)
        cc = cc + 1

all_text = sorted(all_text)
idd = {}

'''stop = []
for n in all_text[:203]:
    stop.append(n)
for n in all_text[5657:]:
    stop.append(n)

count = 1
for n in all_text[203:5657]:
    idd[n] = count
    count = count + 1'''

count = 1
for n in all_text:
    idd[n] = count
    count = count + 1
'''for n in idd:
    print (idd[n],n)
    time.sleep(1)'''
        
for w in t:
    temp = []
    for i in t[w]:
        if i not in stop:
            temp.append(i)
    t[w] = temp

for n in t:
    r = []
    for i in t[n]:
        r.append(idd[i])
    t[n] = sorted(r)

dis = {} 

for n in t:
    for i in range(len(t[n])):
        j = i + 1
        while j < len(t[n]):
            d = (t[n][i],t[n][j])
            if d not in dis:
                dis[d] = 1
            else:
                dis[d] = dis[d] + 1
            j = j + 1

with codecs.open('node.txt','w','utf-8') as f:
    f.write("id\tnode\n")
    for n in idd:
        f.write("%d\t%s\n" %(idd[n],n))
        
with codecs.open('link.txt','w','utf-8') as f:
    f.write("source\ttarget\ttype\tweight\n")
    for n in dis:
        if dis[n] > 1:
            f.write("%d\t%d\tUndirected\t%d\n" %(n[0],n[1],dis[n]))
            #time.sleep(0.01)


# In[ ]:

#資料庫連接測試
import pymysql

db = pymysql.connect(host="140.119.164.170", user="salan40319", passwd="104753018", db="SinicaCorpus",charset='utf8')
cursor = db.cursor()
cursor.execute("SELECT * FROM  `corpus_segpos` WHERE word = '要' and pos = '(D)' ")

'''for row in cursor:
    print (row[1].decode("utf-8"),row[2][1:-1].decode("utf-8"))'''
'''a = ''
for row in cursor:
    a = a + row[1].decode("utf-8")
    if row[2][1:-1].decode("utf-8") == 'PERIODCATEGORY':
        print (a)
        a=''
print (a)'''
num = 0
for i in cursor:
    num = num + 1
print (num)


cursor.close()  
db.close() 


# In[ ]:

#資料庫連接測試
import pymysql
import time

modalverb = ["應","要","可","能","可以","須","應該","必須","會","得","需要","當","應當","能夠","該","需"]
col = ["corpus_segpos","corpus_segpos_31","corpus_segpos_31_news","corpus_segpos_diary","corpus_segpos_magaz"
       ,"corpus_segpos_newspaper","corpus_segpos_newspaper2"]

db = pymysql.connect(host="140.119.164.170", user="salan40319", passwd="104753018", db="SinicaCorpus",charset='utf8')
cursor = db.cursor()

#find = "SELECT COUNT(*) FROM `corpus_segpos_31` WHERE word = %(word)s and  pos LIKE %(check)s"
find_a = "SELECT * FROM `"
find_b = "` WHERE word = %(word)s"
#print (a+col[0]+b)

total = {}

for tabel in col:
    print (tabel)
    for ch in modalverb:
        cursor.execute(find_a+tabel+find_b,{'word':ch})
    
        temp = {}
        num = 0
        for i in cursor:
            num = num + 1
            td = i[2][1:-1].decode('utf-8')
            if td not in total:
                total[td] = 1
            else:
                total[td] = total[td] + 1
                
            if td not in temp:
                temp[td] = 1
            else:
                temp[td] = temp[td] + 1
        print (ch,num,temp)
    print ()

for i in total:
    print (i,total[i])

cursor.close()  
db.close() 


# In[24]:

#依照情緒動詞表，找出各文章詞彙分布情形
import pymysql
import time
import pandas as pd


modalverb = ["應","要","可","能","可以","須","應該","必須","會","得","需要","當","應當","能夠","該","需"]
col = ["corpus_segpos","corpus_segpos_31","corpus_segpos_31_news","corpus_segpos_diary","corpus_segpos_magaz"
       ,"corpus_segpos_newspaper","corpus_segpos_newspaper2"]
connection = pymysql.connect(host="140.119.164.170", user="salan40319", passwd="104753018", db="SinicaCorpus",charset='utf8')

try:
    total = {}
    with connection.cursor() as cursor:
        sql = 'select * from `corpus_segpos` where word="{}"'
        for ch in modalverb:
            cursor.execute(sql.format(ch))
                
            t = {'V':{},'D':{},'N':{},'other':{}}
            temp = {}
            num = 0
            for i in cursor:
                num = num + 1
                td = i[2][1:-1].decode('utf-8')
                if td not in total:
                    total[td] = 1
                else:
                    total[td] = total[td] + 1

                if td not in temp:
                    temp[td] = 1
                else:
                    temp[td] = temp[td] + 1
                if td[0] in t:
                    if td in t[td[0]]:
                        t[td[0]][td] = t[td[0]][td] + 1
                    else:
                        t[td[0]][td] = 1
                else:
                    if td in t['other']:
                        t['other'][td] = t['other'][td] + 1
                    else:
                        t['other'][td] = 1
                   
            pd.options.display.float_format = '{:,.0f}'.format
            #print (ch,num,temp)
            df = pd.DataFrame(t).fillna(0)
            print (ch,num)
            print (df)
            print ('--------------------------')
                
        print ()
        '''for i in total:
            print (i,total[i])'''
                
finally:
    connection.close()


# In[5]:

#建立句子web網路
import pymysql
import time
from colorama import init
import codecs

modalverb = ["應","要","可","能","可以","須","應該","必須","會","得","需要","當","應當","能夠","該","需"]
col = ["corpus_segpos","corpus_segpos_31","corpus_segpos_31_news","corpus_segpos_diary","corpus_segpos_magaz"
       ,"corpus_segpos_newspaper","corpus_segpos_newspaper2"]
connection = pymysql.connect(host="140.119.164.170", user="salan40319", passwd="104753018", db="SinicaCorpus",charset='utf8')

try:
    with connection.cursor() as cursor:
        sql = "select * from `corpus_segpos` limit 0,1000"
        cursor.execute(sql)
        
        temp = '※'
        templist = ['head']
        check = False
        check2 = False
        count = 0
        with codecs.open('dbmap.txt','r','utf-8') as f:
            for i in cursor:
                ch = i[1].decode('utf-8')
                if ch == '。':
                    temp = temp + ch
                    if check:
                        print (temp)
                        #f.write(temp+'\n')
                    temp = '※'
                    check = False
                    #time.sleep(0.01)
                elif ch in modalverb:
                    temp = temp + '\033[31;46m' + ch + '\033[0m'
                    #temp = temp + ch
                    check = True
                else:
                    temp = temp + ch

                if ch == '。':
                    templist.append(str(count))
                    templist.append('end')
                    if check2:
                        print ('-'.join(templist))
                        #f.write('-'.join(templist)+'\n\n')
                        
                        full = -1
                        o = -1
                        for c in templist[1::2]:
                            full = full + int(c) + 1
                        for c in templist[1:-2:2]:
                            o = o + int(c) + 1
                            #print (str(round((o/full)*100,2))+'%')
                            
                        print ()
                        
                    count = 0
                    templist = ['head']
                    check2 = False
                elif ch in modalverb:
                    templist.append(str(count))
                    count = 0
                    templist.append('\033[31m'+ch+i[2].decode('utf-8')+'\033[0m')
                    #templist.append(ch+i[2].decode('utf-8'))
                    check2 = True
                else:
                    count = count + len(ch)
                
finally:
    connection.close()


# In[ ]:

#原始XML
import codecs
import os
import xml.etree.ElementTree as ET
import time

file_path = '../../desktop/SCS_4.0/'

file_list = []

for file in os.listdir(file_path):
    file_list.append(file)
    
tree = ET.parse(file_path+file_list[0])
root = tree.getroot()

'''for child in root:
    print (child.tag, child.attrib)
    print (child[0].text)'''

for child in root:
    for t in child.findall('text'):
        sen = t.findall('sentence')
        for n in sen:
            print (n.text.split())
            time.sleep(0.1)

'''with codecs.open(file_path+file_list[1],'r','utf8') as f:
    content = f.read()'''
    


# In[10]:

#測試XML
import codecs
import os
import xml.etree.ElementTree as ET
import time

file_path = '../../desktop/SCS_4.0/'

file_list = []

tag = {'genre':{},'style':{},'mode':{},'topic':{},'class':{},'medium':{}}

for file in os.listdir(file_path):
    file_list.append(file)

num = 1
allnum = 0
for file in file_list:
    
    tree = ET.parse(file_path+file)
    root = tree.getroot()

    g = 0
    for child in root:
        for i in child:
            if i.tag in tag:
                if i.text in tag[i.tag]:
                    tag[i.tag][i.text] = tag[i.tag][i.text] + 1
                else:
                    tag[i.tag][i.text] = 1
            else:
                pass
                #print (i.text)
            g = g + 1
            if g >= 6:
                g = 0
                
                '''if child[3].text == 'undefined' or child[3].text == 'None':
                    print (file)
                    print (child[11].text)'''
                
                break
        allnum = allnum + 1
    if num % 10 == 0:
        print (num)

    num = num + 1

print ()
for i in tag:
    print (i)
    for j in tag[i]:
        print (j,tag[i][j])
    print ()
#print (tag)
print ('file:'+str(allnum))
    

