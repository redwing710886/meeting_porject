
# coding: utf-8

# In[18]:

#找出平衡語料庫主要tag與值
import os
import xml.etree.ElementTree as ET
import time
import codecs

file_path = 'C:\\Users\\user\\Desktop\\課業相關\\碩士班\\SNA\\meeting\\source\\SCS_4.0\\CKIP\\'
out_path = 'C:\\Users\\user\\Desktop\\category\\'

file_list = []

for file in os.listdir(file_path):
    file_list.append(file)
    
tagging = {'genre':[], 'style':[], 'mode':[], 'topic':[], 'class':[], 'medium':[]}
    
for file in file_list:
    
    tree = ET.parse(file_path+file)
    root = tree.getroot()
    
    count = 0
    
    for article in root:
        for tag in article:
            if tag.tag in tagging:
                if tag.text not in tagging[tag.tag]:
                    tagging[tag.tag].append(tag.text)
        

    '''for sentence in root.iter('sentence'):
        line_index = line_index + 1
        try:
            temp = sentence.text.split()'''
    
for i in tagging:
    with codecs.open(out_path+i+'.txt','wb','utf8') as g:
        for j in tagging[i]:
            if j != 'undefined' and j != None:
                g.write(j+'\r\n')
                #print (i,j)
print ('END')


# In[38]:

#提出所有SC文章
import os
import xml.etree.ElementTree as ET
import time
import codecs

file_path = 'C:\\Users\\user\\Desktop\\課業相關\\碩士班\\SNA\\meeting\\source\\SCS_4.0\\CKIP\\'
out_path = 'C:\\Users\\user\\Desktop\\SCS\\'

file_list = []

for file in os.listdir(file_path):
    file_list.append(file)
    
for file in file_list:

    tree = ET.parse(file_path+file)
    root = tree.getroot()

    for article in root:
        with codecs.open(out_path+article.attrib['no']+'.txt','wb','utf8') as g:
            if article.find('title').text == None:
                g.write('#no_title\r\n')
            else:
                g.write('#'+article.find('title').text+'\r\n')
            for sentence in article.iter('sentence'):
                if sentence.text != None:
                    g.write(sentence.text+'\r\n')

print ('END')                    


# In[27]:

#將各article加上tag寫入資料庫
import os
import xml.etree.ElementTree as ET
import time
import codecs
import pymysql

file_path = 'C:\\Users\\user\\Desktop\\課業相關\\碩士班\\SNA\\meeting\\source\\SCS_4.0\\CKIP\\'

connection = pymysql.connect(host="127.0.0.1", user="redwing", passwd="", db="sinicacorpus",charset='utf8')

file_list = []

for file in os.listdir(file_path):
    file_list.append(file)
    
try:
    with connection.cursor() as cursor:
        sql = "INSERT into article_tag(`no_id`,`genre`,`style`,`mode`,`topic`,`class`,`medium`,`text`) values(\"{}\",\"{}\",\"{}\",\"{}\",\"{}\",\"{}\",\"{}\",\"{}\")" 
    
        for file in file_list:

            tree = ET.parse(file_path+file)
            root = tree.getroot()

            for article in root:
                no = article.attrib['no']
                genre = article[0].text
                style = article[1].text
                mode = article[2].text
                if article[3] != 'undefined' and article[3] != None:
                    topic = article[3].text
                else:
                    topic = 'no_topic'
                classs = article[4].text
                medium = article[5].text
                cursor.execute(sql.format(no,genre,style,mode,topic,classs,medium,file.split('.')[0]))
                #print (no,genre,style,mode,topic,classs,medium,file.split('.')[0])
                
        connection.commit()            
finally:
    connection.close()     

print ('END')                    


# In[2]:

#情態詞尋找(1/2)
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
            word.append(i.strip())

    connection = pymysql.connect(host="127.0.0.1", user="redwing", passwd="", db="word",charset='utf8')

    try:
        with connection.cursor() as cursor:
            sql = "select distinct(`class`) from `word`"
            
            cursor.execute(sql)
            for i in cursor:
                ty.append(i[0])
            
        for i in word:
            with connection.cursor() as cursor:
                sql = "select `class` from `word` where `word` = \"{}\" "

                cursor.execute(sql.format(i))

                for j in cursor:
                    if i in no:
                        continue
                    elif i not in word_modal:
                        word_modal[i] = j[0]
                    else:
                        print (i,j[0],'ERROR')

    finally:
            connection.close()

make_modal()
print ('OK')


# In[6]:

#情態詞尋找(2/2)
#找出符合條件的文章
def find_article(find):
    
    connection = pymysql.connect(host="127.0.0.1", user="redwing", passwd="", db="sinicacorpus",charset='utf8')

    condicate_article = []

    try:
        with connection.cursor() as cursor:
            sql = "SELECT `no_id` FROM `article_tag` WHERE `{}`=\"{}\"" #基本sql指令
            cursor.execute(sql.format(find.split()[0],find.split()[1]))

            for i in cursor:
                condicate_article.append(i[0]+'.txt')

    finally:
        connection.close()
        
    return condicate_article

#找出文章內的情態詞
def get_article(condicate_article):
    
    path = 'C:\\Users\\user\\Desktop\\SCS\\'
    result = {}
    for file_address in condicate_article:
        with codecs.open(path+file_address,'rb','utf8') as f:
            content = f.readlines()

            for line in content:
                if line[0] == '#':
                    continue
                try:
                    line = line.split()

                    for word in line:
                        word = word.split('(')[0]
                        if word in no:
                            if '重複'  not in result:
                                result['重複'] = {word:1}
                            else:
                                if word not in result['重複']:
                                    result['重複'][word] = 1
                                else:
                                    result['重複'][word] += 1
                        elif word in word_modal:
                            if word_modal[word] not in result:
                                result[word_modal[word]] = {word:1}
                            else:
                                if word not in result[word_modal[word]]:
                                    result[word_modal[word]][word] = 1
                                else:
                                    result[word_modal[word]][word] += 1
                except:
                    print (line)
    return result

#得到各文本情態詞彙數
def get_article_num(condicate_article):
    
    path = 'C:\\Users\\user\\Desktop\\SCS\\'
    modal_count = 0
    word_count = 0
    
    for file_address in condicate_article:
        with codecs.open(path+file_address,'rb','utf8') as f:
            content = f.readlines()

            for line in content:
                if line[0] == '#':
                    continue
                try:
                    line = line.split()

                    for word in line:
                        word = word.split('(')[0]
                        if word in no or word in word_modal:
                            modal_count += 1
                        word_count += 1
                except:
                    print (line)
                    
    return modal_count,word_count

#建立比例，arg決定回傳是排序的list還是為排序的dic
def make_pie(condicate_article,arg):
    
    num_ty = {}
    all_num = 0
    
    for ca in ty:
        temp = 0
        if ca in condicate_article:
            for pair in condicate_article[ca]:
                temp += condicate_article[ca][pair]
        num_ty[ca] = temp
        all_num += temp
    
    temp = 0
    for pair in condicate_article['重複']:
        temp += condicate_article['重複'][pair]
    num_ty['重複'] = temp   
    all_num += temp
    
    for i in num_ty:
        #num_ty[i] = round(num_ty[i]*100/all_num,3)
        num_ty[i] = num_ty[i]/all_num
        
    if arg == 'sort':
        
        num_ty = sorted(num_ty.items(), key=lambda d:d[1], reverse = True)
    
    '''for i in num_ty:
        print (i[0],str(i[1])+'%')'''
    
    return num_ty

#手動輸入
'''find = input()

while (find != 'x'):
    condicate_article = find_article(find)
    print (len(condicate_article))
    result = get_article(condicate_article)
    for i in make_pie(result):
        print (i[0],i[1])
        
    find = input()'''


#得到各類別並統一匯出，值為個別比例
'''title = ['']
out_ca = {}
for i in ty:
    out_ca[i] = [i]
out_ca['重複'] = ['重複']
find = 'medium'

with codecs.open(path+'category\\'+find+'.txt','rb','utf8') as f:
    content = f.readlines()
    
    for tag in content:
        tag = tag.strip()
        condicate_article = find_article(find+' '+tag)
        print (len(condicate_article))
        result = get_article(condicate_article)
        pie = make_pie(result,'no_sort')
        title.append(tag+'('+str(len(condicate_article))+')')
        for i in ty:
            out_ca[i].append(str(pie[i]))
        out_ca['重複'].append(str(pie['重複']))
        
with codecs.open(path+"all\\"+find+".csv",'wb','utf8') as g:
    g.write(','.join(title)+'\r\n')
    for i in ty:
        g.write(','.join(out_ca[i])+'\r\n')
    g.write(','.join(out_ca['重複'])+'\r\n')'''

#找出各類別情態詞出現比例
'''find = 'medium'

with codecs.open(path+'category\\'+find+'.txt','rb','utf8') as f:
    content = f.readlines()
    
    with codecs.open(path+'temp.csv','wb','utf8') as g:
        for tag in content:
            tag = tag.strip()
            condicate_article = find_article(find+' '+tag)
            modal_count,word_count = get_article_num(condicate_article)
            print (tag,'='+str(modal_count)+'*1000000/'+str(word_count))
            g.write(tag+',='+str(modal_count)+'*1000000/'+str(word_count)+'\r\n')
''' 

#找出特別情態類別內的值
'''find = 'medium'

with codecs.open(path+'category\\'+find+'.txt','rb','utf8') as f:
    content = f.readlines()
    
    with codecs.open(path+'temp.csv','wb','utf8') as g:
        for tag in content:
            tag = tag.strip()
            condicate_article = find_article(find+' '+tag)
            result = get_article(condicate_article)
            words = []
            nums = []
            #for i in sorted(result['認知-真偽 epistemic-alethic'].items(), key=lambda d:d[1], reverse = True):
            #    words.append(str(i[0]))
            #    nums.append(str(i[1]))
            for i in sorted(result['重複'].items(), key=lambda d:d[1], reverse = True):
                words.append(str(i[0]))
                nums.append(str(i[1]))
            g.write(tag+'('+str(len(condicate_article))+')'+','+','.join(words)+'\r\n')
            g.write(','+','.join(nums)+'\r\n')'''

#母體類別情態詞比例與總情態詞比例
condicate_article = []

for file in os.listdir(path+'SCS\\'):
    condicate_article.append(file)

print (len(condicate_article))
result = get_article(condicate_article)
pie = make_pie(result,'no_sort')
for i in ty:
    print (i+','+str(pie[i]))
    
print ('重複'+','+str(pie['重複']))

modal_count,word_count = get_article_num(condicate_article)
print ('='+str(modal_count)+'*1000000/'+str(word_count))

print ('END')

