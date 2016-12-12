
# coding: utf-8

# In[1]:

#建立情態詞字典
import codecs
import pymysql
import time
import os

path = "C:\\Users\\user\\Desktop\\"
   
ty = [] #情態種類
no = [] #複數情態詞
word = [] #單一情態詞
word_modal = {} #情態詞與其情態種類
no_modal = {}

#建立modal
def make_modal():

    with codecs.open(path+'no.txt','rb','utf8') as f:
        content = f.readlines()

        for i in content:
            no.append(i.strip())

    with codecs.open(path+'word.txt','rb','utf8') as f:
        content = f.readlines()

        for i in content:
            #排除掉word裡面的no
            if i.strip() not in no: 
                word.append(i.strip())

    connection = pymysql.connect(host="127.0.0.1", user="redwing", passwd="", db="word",charset='utf8')

    try:
        with connection.cursor() as cursor:
            sql = "select distinct(`class`) from `word`"
            
            cursor.execute(sql)
            for i in cursor:
                ty.append(i[0])
            ty.append('重複')
            
        for i in word:
            with connection.cursor() as cursor:
                sql = "select `class` from `word` where `word` = \"{}\" "

                cursor.execute(sql.format(i))

                for j in cursor:
                    if i not in word_modal:
                        word_modal[i] = j[0]
                    else:
                        print (i,j[0],'ERROR')
        for i in no:
            word_modal[i] = '重複'
            
            with connection.cursor() as cursor:
                sql = "select `class` from `word` where `word` = \"{}\" "

                cursor.execute(sql.format(i))
                
                for j in cursor:
                    if i not in no_modal:
                        no_modal[i] = [j[0]]
                    else:
                        no_modal[i].append(j[0])                      

    finally:
            connection.close()

make_modal()
print ('OK')


# In[2]:

#file_path = "C:\\Users\\user\\Desktop\\課業相關\\論文資料\\雷震處理資料\\source\\"
file_path = "C:\\Users\\user\\Desktop\\課業相關\\論文資料\\SCS2"
out_path = "C:\\Users\\user\\Desktop\\情態詞結果\\無重複\\"

#find = "日記\\all\\"
#find = "文章+社論\\"
#find = "自由中國母體(無文藝類)\\"
find = "\\"

find_category = '義務-允許 denotic-permissive'

file_list = []

for file in os.listdir(file_path+find):
    file_list.append(file)
    
print ('OK')


# In[5]:

#抓取情態詞與後面接的詞
count_no_dic = {}
for file in file_list:
    with codecs.open(file_path+find+file,'rb','utf8') as f:
        content = f.readlines()
        
        check = False
        first = ''
        second = ''
        
        for w in content[0].split():
            first = second
            second = w
            if check:
                temp = first+' '+second
                if 'CATEGORY' not in second:
                    if temp not in count_no_dic:
                        count_no_dic[temp] = 1
                    else:
                        count_no_dic[temp] += 1
                check = False
            if w.split('(')[0] in word:
                if word_modal[w.split('(')[0]] == find_category:
                    check = True   
                
result = sorted(count_no_dic.items(), key=lambda d:d[1], reverse = True)
for i in result:
    print (i[0],i[1])
    time.sleep(0.3)


# In[24]:

#印出情態詞總類中各文件詞頻向量
condicate_word = []
connection = pymysql.connect(host="127.0.0.1", user="redwing", passwd="", db="word",charset='utf8')
try:
    with connection.cursor() as cursor:
        sql = "select `word` from `word` where `class` = \'{}\'"
        
        cursor.execute(sql.format(find_category))
        
        for i in cursor:
            if i[0] in word and i[0] not in no:
                condicate_word.append(i[0])
                
finally:
    connection.close()
    
with codecs.open(out_path+find_category+'.csv','wb','utf8') as g:
    g.write(','+','.join(condicate_word)+'\r\n')
    for file in file_list:
        with codecs.open(file_path+find+file,'rb','utf8') as f:
            content = f.readlines()

            temp_list = []
            for i in range(len(condicate_word)):
                temp_list.append(0)

            for i in content[1].split():
                if i.split('(')[0] in condicate_word:
                    temp_list[condicate_word.index(i.split('(')[0])] += 1
            #if not all(v == 0 for v in temp_list):
            g.write(file.split('.')[0]+','+','.join(str(x) for x in temp_list)+'\r\n')
            
print ('END')


# In[5]:

#處理重複情態詞並歸類
alltydic = {}
article_title = []
for i in ty:
    if i != '重複':
        #alltydic[i] = []
        alltydic[i] = 0
len_text = []
for file in file_list:
    article_title.append(file.split('.')[0])
    with codecs.open(file_path+find+file,'rb','utf8') as f:
        if find.split('\\')[0] != '日記':
            f.readline()
        content = f.readline() 
        content = (content.strip()).split()
        len_text.append(len(content))
        
        tydic = {}
        for i in ty:
            if i != '重複':
                tydic[i] = 0
        
        for i in content:
            if i.split('(')[0] in word:
                tydic[word_modal[i.split('(')[0]]] += 1
            elif i.split('(')[0] in no:
                setcount = 0
                if len(no_modal[i.split('(')[0]]) == 2:
                    setcount = 0.5
                elif len(no_modal[i.split('(')[0]]) == 3:
                    setcount = 0.33
                else:
                    print ('ERROR')
                for j in no_modal[i.split('(')[0]]:
                    tydic[j] += setcount
                    tydic[j] = round(tydic[j],2)
                    
        for i in ty:
            if i != '重複':
                #alltydic[i].append(tydic[i])
                alltydic[i] += tydic[i]

with codecs.open(out_path+'ans.csv','wb','utf8') as g:
    #g.write(','+','.join(article_title)+'\r\n')
    for i in ty:
        if i != '重複':
            #g.write(i+','+','.join(str(x) for x in alltydic[i])+'\r\n')
            g.write(i+','+str(round(alltydic[i],2))+'\r\n')
    #g.write('總詞數,'+','.join(str(x) for x in len_text)+'\r\n')
    print (sum(len_text))
            
print ('END')

