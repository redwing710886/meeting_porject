
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


# In[9]:

#DB內容查詢
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
        
        sql = 'select `file_sentence`,`two_pos` from `verb_in_sentence` where `two_verb` = "{}"'
        
        ch = '要,要'
        
        cursor.execute(sql.format(ch))
        
        for i in cursor:
            index = i[0].split('@')

            tree = ET.parse(file_path+index[0])
            root = tree.getroot()
            
            print (root.findall('./article/text/sentence')[int(index[1])].text)
            print (i[1])
            print ()
            time.sleep(0.5)
finally:
    connection.close()

