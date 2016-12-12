
# coding: utf-8

# In[24]:

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
                

    finally:
            connection.close()

make_modal()
print ('OK')


# In[46]:

#建立特定文本的情態詞分布並匯出
file_path = "C:\\Users\\user\\Desktop\\課業相關\\論文資料\\雷震處理資料\\source\\"
out_path = "C:\\Users\\user\\Desktop\\情態詞結果\\"

find = "日記\\all\\"
find_op = False

file_list = []

for file in os.listdir(file_path+find):
    file_list.append(file)

#讀檔並回傳字串
def read_file(file,header):
    
    with codecs.open(file_path+find+file,'rb','utf8') as f:
        if header == True:
            f.readline()
        content = f.readlines()
        
        return content[0]

alltydic = {}
len_text = []
for i in ty:
    alltydic[i] = []

for file in file_list:
    content = read_file(file,find_op).split()
    len_text.append(str(len(content)))
    
    tydic = {}

    for i in ty:
        tydic[i] = 0
    
    #文章單詞逐一比對，找出情態詞並記錄次數
    for i in content:
        count = 0
        for j in no:
            if j == i.split('(')[0]:
                count += 1
        if count == 0:
            for j in word:
                if j == i.split('(')[0]: 
                    count += 1
        if count > 0:
            tydic[word_modal[i.split('(')[0]]] += 1
            #print (i.split('(')[0],word_modal[i.split('(')[0]],count)
    
    for i in ty:
        #alltydic[i] += tydic[i]
        alltydic[i].append(str(tydic[i]))
        
    print (file.split('.')[0])
        
with codecs.open(out_path+'日記.csv','wb','utf8') as g:
    for i in ty:
        #g.write(i+','+str(alltydic[i])+'\r\n')
        g.write(i+','+','.join(alltydic[i])+'\r\n')
        '''g.write(i)
        for j in range(len(alltydic[i])):
            g.write(','+'='+str(alltydic[i][j])+'*1000000/'+str(len_text[j]))
        g.write('\r\n')'''
    g.write('總詞數,'+','.join(len_text)+'\r\n')
    
print ('END')

