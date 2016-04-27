
# coding: utf-8

# In[ ]:

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


# In[ ]:

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


# In[ ]:

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
output_file = "C:/Users/user/Desktop/new_diary/diary_{}.xml"
book = xlrd.open_workbook(file)
sh = book.sheet_by_index(0)
 
#title author bookname publisher publishdate page theme keyword text

li = ['title','author','bookname','publisher','publishdate','page','theme','keyword']

root = Element('root')

ci = 0
fail = False

for rx in range(sh.nrows-ci):
    #rx = rx + ci
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
    
    #文章終句例外判斷?
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
            #fail = True
    
    if rx % 10 == 0:
        '''if fail:
            root = Element('root')
            rx = rx - 10
            print ('return')
            fail = False
            continue'''
        tree = ElementTree(root)
        num = str(int(rx / 10))
        if len(num) == 1:
            num = '00'+num
        elif len(num) == 2:
            num = '0'+num
        tree.write(output_file.format(num), encoding='utf-8')
        root = Element('root')

tree = ElementTree(root)
tree.write(output_file.format('945'), encoding='utf-8')

#xml_string = etree.tostring(root,'utf-8')
#print (xml_string.decode('utf8'))
print ('end')


# In[16]:

#問題句子所在比例分析
import xml.etree.ElementTree as ET
import os
import time

file_path = "C:/Users/user/Desktop/temp/"
file_list = []

for file in os.listdir(file_path):
    file_list.append(file)

all_num = 0
all_error_word = 0  
all_error_split = 0

for file in file_list:
    tree = ET.parse(file_path+file)
    root = tree.getroot()
    
    num = 0
    error_word = 0
    error_split = 0

    
    for child in root:
        for sentence in child[8]:
            num = num + 1
            if len(sentence.attrib) > 0:
                if sentence.attrib['error'] == '古字':
                    error_word = error_word + 1
                elif sentence.attrib['error'] == '斷詞失敗':
                    error_split = error_split + 1
                else:
                    print ('other')
    error_count = (error_word+error_split)*100/num
    print (file,num,error_word,error_split,str(round(error_count,2))+'%')
    
    all_num = all_num + num
    all_error_word = all_error_word + error_word
    all_error_split = all_error_split + error_split
    
print (all_num,all_error_word,all_error_split,str(round((all_error_split+all_error_word)*100/all_num,2))+'%')


# In[7]:

#diary XML內容抓取 one 情態動詞
import codecs
import os
import xml.etree.ElementTree as ET
import time
import sys

modalverb = ["應","要","可","能","可以","須","應該","必須","會","得","需要","當","應當","能夠","該","需"]
file_path = '../../desktop/temp/'

file_list = []

for file in os.listdir(file_path):
    file_list.append(file)

one_verb = {} 
    
error_num = 0
skip = 0

for file in file_list:
    
    tree = ET.parse(file_path+file)
    root = tree.getroot()

    for sentence in root.iter('sentence'):
        if len(sentence.attrib) > 0:
            skip = skip + 1
            continue
            
        try:
            temp = sentence.text.split()

            verb_list = []
            
            for i in temp:
                word = i.split('(')
                word[1] = '('+word[1].split('[')[0]

                if word[0] in modalverb:
                    verb_list.append(''.join(word))

            if len(verb_list) > 0:
                for l in verb_list:
                    if l in one_verb:
                        one_verb[l] = one_verb[l] + 1
                    else:
                        one_verb[l] = 1
     
        except:
            '''e = sys.exc_info()[0]
            print (e)
            time.sleep(0.3)'''
            error_num = error_num + 1

one_verb_count = 0

for i in one_verb:
    one_verb_count = one_verb_count + one_verb[i]

print (error_num) #0
print (len(one_verb)) #37
print (one_verb_count) #14964
print (skip) #18031

one_verb = sorted(one_verb.items(), key=lambda d:d[1], reverse = True)

for i in one_verb:
    print (i[0],i[1])


# In[1]:

#diary XML內容抓取 pair情態動詞
import codecs
import os
import xml.etree.ElementTree as ET
import time
import sys

modalverb = ["應","要","可","能","可以","須","應該","必須","會","得","需要","當","應當","能夠","該","需"]
file_path = '../../desktop/temp/'

file_list = []

for file in os.listdir(file_path):
    file_list.append(file)

two_verb = {} 
    
error_num = 0
much = 0
skip = 0

for file in file_list:
    
    tree = ET.parse(file_path+file)
    root = tree.getroot()

    for sentence in root.iter('sentence'):
        if len(sentence.attrib) > 0:
            skip = skip + 1
            continue
            
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
                for l in range(len(verb_list)-1):
                    k = l + 1
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

two_verb_count = 0

for i in two_verb:
    two_verb_count = two_verb_count + two_verb[i]

two_verb = sorted(two_verb.items(), key=lambda d:d[1], reverse = True)

print (error_num) #0
print (much) #14
print (len(two_verb)) #160
print (two_verb_count) #561
print (skip) #18031

for i in two_verb:
    print (i[0],i[1])


# In[1]:

#找出符合要求的句子(重複句沒抓) one
import xml.etree.ElementTree as ET
import os
import time
from colorama import init

modalverb = ["應","要","可","能","可以","須","應該","必須","會","得","需要","當","應當","能夠","該","需"]
file_path = "C:/Users/user/Desktop/temp/"
file_list = []

for file in os.listdir(file_path):
    file_list.append(file)

find = '可(ADV)'   
    
for file in file_list:
    tree = ET.parse(file_path+file)
    root = tree.getroot()

    for child in root:
        for sentence in child[8]:
            if len(sentence.attrib) == 0:
                temp = sentence.text.split()
                
                lis = []
                
                if find in temp:
                    for ch in temp:
                        if ch == find:
                            lis.append('\033[31;46m' + ch + '\033[0m') 
                        else:
                            lis.append(ch)
                    print (''.join(lis))

                '''for i in temp:

                    word = i.split('(')
                    word[1] = '('+word[1].split('[')[0]

                    if word[0] in modalverb:
                        verb_list.append(''.join(word))
                        verb_index.append(vi)

                    vi = vi + 1
                    
                if len(verb_list) == 2:
                    if verb_list[0] == find[0] and verb_list[1] == find[1]:
                        print (''.join(sentence.text.split()))'''
        time.sleep(0.01)


# In[3]:

#找出符合要求的句子(重複句沒抓) two
import xml.etree.ElementTree as ET
import os
import time

modalverb = ["應","要","可","能","可以","須","應該","必須","會","得","需要","當","應當","能夠","該","需"]
file_path = "C:/Users/user/Desktop/temp/"
file_list = []

for file in os.listdir(file_path):
    file_list.append(file)

find = ['當(P)', '可(ADV)']    
    
for file in file_list:
    tree = ET.parse(file_path+file)
    root = tree.getroot()

    for child in root:
        for sentence in child[8]:
            if len(sentence.attrib) == 0:
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
                    
                if len(verb_list) == 2:
                    if verb_list[0] == find[0] and verb_list[1] == find[1]:
                        print (''.join(sentence.text.split()))


# In[21]:

#雷震日記內容匯出及抓取
import xlrd
import codecs
import time

file = "C:/Users/user/Desktop/雷震日記全表單-資訊處理-20160329.xls"
book = xlrd.open_workbook(file)

sh = book.sheet_by_index(0)

num = 0

with codecs.open("C:/Users/user/Desktop/雷震日記.txt",'w','utf8') as f:
    for rx in range(sh.nrows):
        if rx == 0:
            continue
        content = sh.cell_value(rowx=rx, colx=8)
        num = num + len(''.join(content.strip().split())) #1856456/1868713/1810901 strip/no_strip/strip&split 
        f.write(''.join(content.strip().split())+'\r\n')
        f.write('\r\n')
print (num)


# In[1]:

#修正雷震日記XML部分斷詞失敗問題
from xml.etree import ElementTree as ET
from xml.etree.ElementTree import Element, SubElement, ElementTree
import xlrd
import time
import os
import codecs

from ckip import CKIPSegmenter, CKIPParser
segmenter = CKIPSegmenter('104753018', 'sayanouta')

file = "C:/Users/user/Desktop/雷震日記全表單-資訊處理-20160329.xls"
input_file = "C:/Users/user/Desktop/diary/"
book = xlrd.open_workbook(file)
sh = book.sheet_by_index(0)

file_list = []

for file in os.listdir(input_file):
    file_list.append(file)

with codecs.open("C:/Users/user/Desktop/new.txt",'w','utf8') as f:
    
    for file in file_list:

        tree = ET.parse(input_file+file)
        root = tree.getroot()

        for article in root:

            index = int(article.get('no'))
            content = sh.cell_value(rowx=index, colx=8)

            lines = []
            temp = ''

            for word in content:
                temp = temp + word
                if word == '。' or word == '，':
                    lines.append(temp.strip())
                    temp = ''

            num = len(article[8])

            if len(lines) != num:
                print (file,index,len(lines),num)
                
                f.write(file+' no.'+str(index)+'\r\n')

                for line in lines:
                    
                    try:
                        segmented_result = segmenter.process(line)

                        words = []
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
                                f.write('古字：'+line+'\r\n')
                            else:
                                f.write(' '.join(words)+'\r\n')
                    except:
                        f.write('斷詞失敗：'+line+'\r\n')
                
                f.write('\r\n')

