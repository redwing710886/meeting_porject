
# coding: utf-8

# In[3]:

#XML內容抓取
# 235/1396133
import codecs
import os
import xml.etree.ElementTree as ET
import time
import sys

modalverb = ["應","要","可","能","可以","須","應該","必須","會","得","需要","當","應當","能夠","該","需"]
file_path = '../../desktop/SCS_4.0/'

file_list = []

for file in os.listdir(file_path):
    file_list.append(file)

two_verb = {} 
    
error_num = 0
much = 0

for file in file_list:
    
    tree = ET.parse(file_path+file)
    root = tree.getroot()

    for sentence in root.iter('sentence'):
        try:
            temp = sentence.text.split()

            verb_list = []
            
            for i in temp:
                word = i.split('(')
                word[1] = '('+word[1].split('[')[0]

                if word[0] in modalverb:
                    verb_list.append(''.join(word))

            if len(verb_list) >= 2:
                if len(verb_list) >= 3:
                    much = much + 1
                for l in range(len(verb_list)):
                    for k in range(len(verb_list)-l-1):
                        k = k + l + 1
                        if (verb_list[l],verb_list[k]) in two_verb:
                            two_verb[(verb_list[l],verb_list[k])] = two_verb[(verb_list[l],verb_list[k])] + 1
                        else:
                            two_verb[(verb_list[l],verb_list[k])] = 1
     
        except:
            '''e = sys.exc_info()[0]
            print (e)
            time.sleep(0.3)'''
            error_num = error_num + 1

pop = []

#是否照順序
'''for i in two_verb:
    if (i[1],i[0]) in two_verb and i not in pop and i[0] != i[1]:
        two_verb[i] = two_verb[i] + two_verb[(i[1],i[0])]
        pop.append((i[1],i[0]))

print (len(two_verb)) #230/614
print (len(pop)) #101/188
for j in pop:
    two_verb.pop(j)'''

two_verb = sorted(two_verb.items(), key=lambda d:d[1], reverse = True)

print (error_num) #235
print (much) #465
print (len(two_verb)) #129(2個,無前後)/426(2個,有前後)/641(多個,有前後)

for i in two_verb:
    print (i[0],i[1])


# In[4]:

#情態動詞存入DB內
# 235/1396133
import os
import xml.etree.ElementTree as ET
import sys
import time
import pymysql

modalverb = ["應","要","可","能","可以","須","應該","必須","會","得","需要","當","應當","能夠","該","需"]
file_path = '../../desktop/SCS_4.0/'
connection = pymysql.connect(host="127.0.0.1", user="redwing", passwd="", db="modalverb",charset='utf8')

file_list = []

for file in os.listdir(file_path):
    file_list.append(file)

two_verb = {} 
    

with connection.cursor() as cursor:
    
    sql = "INSERT into verb_in_sentence(two_verb,two_pos,verb_index,file_sentence) value(\"{}\",\"{}\",\"{}\",\"{}\")"
    
    for file in file_list:

        tree = ET.parse(file_path+file)
        root = tree.getroot()

        slen = 0 #句子數目計算

        for sentence in root.iter('sentence'):

            try:
                temp = sentence.text.split()

                verb_list = []  #情態動詞陣列
                verb_index = []  #情態動詞所在位置陣列
                vi = 0 #index計算

                for i in temp:

                    word = i.split('(')
                    word[1] = '('+word[1].split('[')[0]

                    if word[0] in modalverb:
                        verb_list.append(''.join(word))
                        verb_index.append(vi)

                    vi = vi + 1

                if len(verb_list) >= 2:
                    for l in range(len(verb_list)):
                        for k in range(len(verb_list)-l-1):
                            k = k + l + 1

                            com1 = verb_list[l].split('(')
                            com2 = verb_list[k].split('(')

                            verb1 = com1[0]
                            verb2 = com2[0]
                            index1 = str(verb_index[l])
                            index2 = str(verb_index[k])
                            pos1 = '('+com1[1]
                            pos2 = '('+com2[1]
                            
                            cursor.execute(sql.format(verb1+','+verb2 ,pos1+','+pos2 ,index1+','+index2 ,file+'@'+str(slen)))
                            
                            
                            '''print (verb1,verb2,index1,index2,pos1,pos2,file+'@'+str(slen))
                            time.sleep(0.3)'''
            except:
                '''e = sys.exc_info()[0]
                print (e)
                time.sleep(0.3)'''
                continue
            finally:
                slen = slen + 1

connection.commit()
connection.close()
print ('OK')


# In[2]:

#情態動詞存入DB內(修改)
# 235/1396133
# 8744/9285/9939 包含情態動詞的不重複句子數/包含情態動詞的重複句子數(A,B)(B,C)/包含情態動詞的完整重複句子數(A,B)(B,C)(A,C)
# 4928/9285 詞性為(D),(D)/同上
import os
import xml.etree.ElementTree as ET
import sys
import time
import pymysql

modalverb = ["應","要","可","能","可以","須","應該","必須","會","得","需要","當","應當","能夠","該","需"]
file_path = '../../desktop/SCS_4.0/'
connection = pymysql.connect(host="127.0.0.1", user="redwing", passwd="", db="modalverb",charset='utf8')

file_list = []

for file in os.listdir(file_path):
    file_list.append(file)

two_verb = {} 
match_line = 0  
match_line2 = 0

with connection.cursor() as cursor:
    
    sql = "INSERT into verb_in_sentence(two_verb,two_pos,verb_index,file_sentence) value(\"{}\",\"{}\",\"{}\",\"{}\")"
    
    for file in file_list:
        
        verbline_in_file = 0

        tree = ET.parse(file_path+file)
        root = tree.getroot()

        slen = 0 #句子數目計算

        for sentence in root.iter('sentence'):

            try:
                temp = sentence.text.split()

                verb_list = []  #情態動詞陣列
                verb_index = []  #情態動詞所在位置陣列
                vi = 0 #index計算

                for i in temp:

                    word = i.split('(')
                    word[1] = '('+word[1].split('[')[0]

                    if word[0] in modalverb:
                        verb_list.append(''.join(word))
                        verb_index.append(vi)

                    vi = vi + 1

                if len(verb_list) >= 2:
                    match_line = match_line + 1
                    verbline_in_file = verbline_in_file + 1
                    for l in range(len(verb_list)-1):
                        k = l + 1
                        match_line2 = match_line2 + 1
                        com1 = verb_list[l].split('(')
                        com2 = verb_list[k].split('(')

                        verb1 = com1[0]
                        verb2 = com2[0]
                        index1 = str(verb_index[l])
                        index2 = str(verb_index[k])
                        pos1 = '('+com1[1]
                        pos2 = '('+com2[1]
                            
                        cursor.execute(sql.format(verb1+','+verb2 ,pos1+','+pos2 ,index1+','+index2 ,file+'@'+str(slen)))
                            
                            
                        #print (verb1,verb2,index1,index2,pos1,pos2,file+'@'+str(slen))
                        #time.sleep(1)
                    #print (temp)
            except:
                '''e = sys.exc_info()[0]
                print (e)
                time.sleep(0.3)'''
                continue
            finally:
                slen = slen + 1
    
        print (file,verbline_in_file)
    
connection.commit()
connection.close()

print (match_line)
print (match_line2)
print ('OK')


# In[3]:

#DB句子查詢
# 235/1396133
import os
import xml.etree.ElementTree as ET
import time
import pymysql
from colorama import init

modalverb = ["應","要","可","能","可以","須","應該","必須","會","得","需要","當","應當","能夠","該","需"]
file_path = '../../desktop/SCS_4.0/'
connection = pymysql.connect(host="127.0.0.1", user="redwing", passwd="", db="modalverb",charset='utf8')

file_list = []

for file in os.listdir(file_path):
    file_list.append(file)

try:
    with connection.cursor() as cursor:
        
        sql = 'select `file_sentence`,`verb_index`,`two_pos` from `verb_in_sentence` where `two_verb` = "{}"'
        
        ch = '得,得'
        pos = '(D),(D)'
        
        cursor.execute(sql.format(ch))
        
        for i in cursor:
            
            '''#選擇何種詞性
            if i[2] != pos:
                continue'''
            
            index = i[0].split('@')

            tree = ET.parse(file_path+index[0])
            root = tree.getroot()
            
            sentence = root.findall('./article/text/sentence')[int(index[1])].text
            
            temp = ''
            
            count = 0
            for j in sentence.split():
                vi = [int(i[1].split(',')[0]),int(i[1].split(',')[1])] #verb index
                if count in vi:
                    temp = temp + '\033[31;46m' + j + '\033[0m'
                else:
                    temp = temp + j#j.split('(')[0]
                count = count + 1
                    
            sentence = temp
            
            '''#印出前後句
            sentence_pre = 'head'
            sentence_next = 'end'
            
            if int(index[1]) > 0:
                sentence_pre = root.findall('./article/text/sentence')[int(index[1])-1].text
            if int(index[1]) < len(root.findall('./article/text/sentence'))-1:
                sentence_next = root.findall('./article/text/sentence')[int(index[1])+1].text'''
            
            #print (sentence_pre)
            print (sentence)
            #print (sentence_next)
            
            print (i[1])
            print ()
            time.sleep(0.3)
finally:
    connection.close()


# In[1]:

#從DB查詢某verb其詞性各別出現頻率
# 235/1396133
import os
import xml.etree.ElementTree as ET
import time
import pymysql

modalverb = ["應","要","可","能","可以","須","應該","必須","會","得","需要","當","應當","能夠","該","需"]
file_path = '../../desktop/SCS_4.0/'
connection = pymysql.connect(host="127.0.0.1", user="redwing", passwd="", db="modalverb",charset='utf8')

file_list = []

for file in os.listdir(file_path):
    file_list.append(file)

try:
    with connection.cursor() as cursor:
        
        sql = 'select `two_pos` from `verb_in_sentence` where `two_verb` = "{}"'
        
        ch = '要,能'
        
        cursor.execute(sql.format(ch))
        
        pos_num = {}
        
        psum = 0
        
        for i in cursor:
            psum = psum + 1
            if i[0] not in pos_num:
                pos_num[i[0]] = 1
            else:
                pos_num[i[0]] = pos_num[i[0]] + 1
        
        pos_num = sorted(pos_num.items(), key=lambda d:d[1], reverse = True)
        
        print (ch,len(pos_num),psum)
        for i in pos_num:
            print (i[0],i[1])
        
finally:
    connection.close()


# In[ ]:

#DB句子查詢(修改)
# 235/1396133
import os
import xml.etree.ElementTree as ET
import time
import pymysql
from colorama import init

modalverb = ["應","要","可","能","可以","須","應該","必須","會","得","需要","當","應當","能夠","該","需"]
file_path = '../../desktop/SCS_4.0/'
connection = pymysql.connect(host="127.0.0.1", user="redwing", passwd="", db="modalverb",charset='utf8')

file_list = []

for file in os.listdir(file_path):
    file_list.append(file)

try:
    with connection.cursor() as cursor:
        
        sql = 'select `file_sentence`,`verb_index`,`two_pos` from `verb_in_sentence` where `two_verb` = "{}"'
        
        ch = '得,得'
        pos = '(D),(D)'
        
        cursor.execute(sql.format(ch))
        
        for i in cursor:
            
            '''#選擇何種詞性
            if i[2] != pos:
                continue'''
            
            index = i[0].split('@')

            tree = ET.parse(file_path+index[0])
            root = tree.getroot()
            
            sentence = root.findall('./article/text/sentence')[int(index[1])].text
            
            temp = ''
            
            count = 0
            for j in sentence.split():
                vi = [int(i[1].split(',')[0]),int(i[1].split(',')[1])] #verb index
                if count in vi:
                    temp = temp + '\033[31;46m' + j + '\033[0m'
                else:
                    temp = temp + j#j.split('(')[0]
                count = count + 1
                    
            sentence = temp
            
            '''#印出前後句
            sentence_pre = 'head'
            sentence_next = 'end'
            
            if int(index[1]) > 0:
                sentence_pre = root.findall('./article/text/sentence')[int(index[1])-1].text
            if int(index[1]) < len(root.findall('./article/text/sentence'))-1:
                sentence_next = root.findall('./article/text/sentence')[int(index[1])+1].text'''
            
            #print (sentence_pre)
            print (sentence)
            #print (sentence_next)
            
            print (i[1])
            print ()
            time.sleep(0.3)
finally:
    connection.close()


# In[1]:

#雷震日記
#有些字無法判斷
import xlrd
import time
import sys

from ckip import CKIPSegmenter, CKIPParser
segmenter = CKIPSegmenter('104753018', 'sayanouta')

file = "C:/Users/user/Desktop/雷震日記全表單-資訊處理-20160329.xls"
book = xlrd.open_workbook(file)

#print ("The number of worksheets is", book.nsheets)
#print ("Worksheet name(s):", book.sheet_names())
sh = book.sheet_by_index(0)
#print (sh.name, sh.nrows, sh.ncols)
'''print ("Cell D30 is", sh.cell_value(rowx=1, colx=0))
for rx in range(sh.nrows):
    #print (type(sh.row(rx)[0]))
    print (sh.cell_value(rowx=rx, colx=0))'''

#16 21 29 34 36 53 55 66 68
for rx in range(sh.nrows):
    if rx == 0:
        continue
    content = sh.cell_value(rowx=rx, colx=8)
    
    print (rx)
    
    lines = []
    temp = ''
    
    for word in content:
        temp = temp + word
        if word == '。' or word == '，':
            lines.append(temp)
            temp = ''
    
    for line in lines:
        try:
            segmented_result = segmenter.process(line)

            words = []

            if segmented_result['status_code'] != '0':
                    print ('Process Failed: ' + segmented_result['status'])
            else:
                for sentence in segmented_result['result']:
                    for term in sentence:
                        words.append(term['term']+'('+term['pos']+')')
                        '''if term['pos'] == 'COMMACATEGORY' or term['pos'] == 'PERIODCATEGORY' or (term['pos'] == 'QUESTIONCATEGORY' and 
                            term['pos'] == '?'):
                            #print (' '.join(words))
                            #print ()
                            words = []'''
                print (' '.join(words))
        except:
            e = sys.exc_info()[0]
            print (rx,e)
    break


# In[26]:

#XML排版
from xml.etree import ElementTree as etree
from xml.etree.ElementTree import Element, SubElement, ElementTree
 
#title author bookname publisher publishdate page theme keyword text

root = Element('root')

article = SubElement(root, 'acticle')
article.set("no", "1")

title = SubElement(article, 'title')
author = SubElement(article, 'author')
bookname = SubElement(article, 'bookname')
publisher = SubElement(article, 'publisher')
publishdate = SubElement(article, 'publishdate')
page = SubElement(article, 'page')
theme= SubElement(article, 'theme')
keyword = SubElement(article, 'keyword')
text = SubElement(article, 'text')
text.text = '雷震日記'

tree = ElementTree(root)

#tree.write('C:/Users/user/Desktop/result.xml', encoding='utf-8')

xml_string = etree.tostring(root,'utf-8')
print (xml_string.decode('utf8'))


# In[32]:

#建立雷震日記XML
from xml.etree import ElementTree as etree
from xml.etree.ElementTree import Element, SubElement, ElementTree
import xlrd
import time
import sys
import datetime

from ckip import CKIPSegmenter, CKIPParser
segmenter = CKIPSegmenter('104753018', 'sayanouta')

file = "C:/Users/user/Desktop/雷震日記全表單-資訊處理-20160329.xls"
book = xlrd.open_workbook(file)
sh = book.sheet_by_index(0)
 
#title author bookname publisher publishdate page theme keyword text

li = ['title','author','bookname','publisher','publishdate','page','theme','keyword']

root = Element('root')

for rx in range(sh.nrows):
    if rx == 0:
        continue
    
    article = SubElement(root, 'acticle')
    article.set("no", str(rx))
    
    for i in range(len(li)):
        temp = SubElement(article,li[i])
        if li[i] == 'publishdate':
            a1_as_datetime = datetime.date(*xlrd.xldate_as_tuple(sh.cell_value(rowx=rx, colx=i), 0)[:3])
            temp.text = str(a1_as_datetime)
        else:
            temp.text = str(sh.cell_value(rowx=rx, colx=i))
    text = SubElement(article,'text')
    
    content = sh.cell_value(rowx=rx, colx=8)
    
    print (rx)
    
    lines = []
    temp = ''
    
    for word in content:
        temp = temp + word
        if word == '。' or word == '，':
            lines.append(temp.strip())
            temp = ''
    
    for line in lines:
        try:
            segmented_result = segmenter.process(line)

            words = []
            sentence = SubElement(text, 'sentence')
            check = False

            if segmented_result['status_code'] != '0':
                    print ('Process Failed: ' + segmented_result['status'])
            else:
                for sentences in segmented_result['result']:
                    for term in sentences:
                        if term['pos'] == 'QUESTIONCATEGORY':
                            check = True
                        words.append(term['term']+'('+term['pos']+')')
                
                if check:
                    sentence.text = str(line)
                    sentence.set('error','古字')
                else:
                    sentence.text = ' '.join(words)
                
        except:
            sentence.text = str(line)
            sentence.set('error','斷詞失敗')
            e = sys.exc_info()[0]
            print (rx,e)
    
    if rx == 2:
        break
    
tree = ElementTree(root)

tree.write('C:/Users/user/Desktop/result.xml', encoding='utf-8')

#xml_string = etree.tostring(root,'utf-8')
#print (xml_string.decode('utf8'))
print ('end')

