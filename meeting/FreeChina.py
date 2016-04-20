
# coding: utf-8

# In[ ]:

#建立句子 平均長度為9 測試版
import pymysql

connection = pymysql.connect(host="140.119.164.170", user="salan40319", passwd="104753018", db="FreeChina",charset='utf8')
file = []
for i in range(1):
    if i < 9:
        file.append('0'+str(i+1)+'_All')
    else:
        file.append(str(i+1)+'_All')
print (file)

g = 0


try:
    for i in file:
        with connection.cursor() as cursor:
            sql = "select * from `{}`"

            cursor.execute(sql.format(i))

            temp_line = ''
            #( 「 『 』

            c = 0
            check = False

            l = 0
            e = 0

            for i in cursor:
                temp_line = temp_line + i[1].decode('utf8')
                if len(temp_line) == 1 and i[2].decode('utf8') == '(PARENTHESISCATEGORY)':
                    e = e + 1
                    if i[1].decode('utf8') == '」' or i[1].decode('utf8') == '』':
                        check = True
                if i[2].decode('utf8') == '(PARENTHESISCATEGORY)':
                    c = c + 1

                if c == 2 and len(temp_line) == 2:
                    temp_line = ''
                    c = 0
                    check = False

                if i[2].decode('utf8') == '(PERIODCATEGORY)' or i[2].decode('utf8') == '(COMMACATEGORY)':
                    if len(temp_line) > 8:
                        if not check:
                            print ('*'+temp_line) 
                            pass
                        else:
                            print ('#'+temp_line[1:]) 
                            pass
                        temp_line = ''
                        l = l + 1
                        check = False
                        c = 0

            #print (l,e) #7529 168
            g = g + l

finally:
    connection.close()

print (g)


# In[58]:

#建立句子
import pymysql
import codecs

connection = pymysql.connect(host="140.119.164.170", user="salan40319", passwd="104753018", db="FreeChina",charset='utf8')

#得到所有table
file = []
for i in range(23):
    if i < 9:
        file.append('0'+str(i+1)+'_All')
    else:
        file.append(str(i+1)+'_All')
print (file)

check = False #判斷是否到達文章結尾

try:
    for i in file:
        with codecs.open("C:\\Users\\user\\Desktop\\FreeChina\\"+i+'.txt','w','utf8') as f:
            with connection.cursor() as cursor:
                sql = "select * from `{}`"

                cursor.execute(sql.format(i))

                temp_line = ''
                #( 「 『 』
                
                print (i)

                for i in cursor:

                    if check:
                        check = False
                        #若為以下字元開頭，補進上一欄
                        if (i[1].decode('utf8') == '』' or i[1].decode('utf8') == '」' 
                            or i[1].decode('utf8') == '）' or i[1].decode('utf8') == ')'):
                            temp_line = temp_line + i[1].decode('utf8') + i[2].decode('utf8')
                            #print ('*'+temp_line)
                            f.write (temp_line.strip()+'\r\n')
                            temp_line = ''
                            continue
                        #將上一行印出
                        else:
                            #print ('*'+temp_line)
                            f.write (temp_line.strip()+'\r\n')
                            temp_line = ''
                    
                    #判斷是否為datetime 獨立一行
                    if i[2].decode('utf8') == '(DATETIME)':
                        if len(temp_line) != 0:
                            #print ('#'+temp_line)
                            f.write (temp_line.strip()+'\r\n')
                        temp_line = '# '


                    temp_line = temp_line + i[1].decode('utf8') + i[2].decode('utf8') + ' '
                    
                    #判斷是否為。，？！；：結尾，author則為獨立一行
                    if (i[2].decode('utf8') == '(PERIODCATEGORY)' or i[2].decode('utf8') == '(COMMACATEGORY)' 
                        or i[2].decode('utf8') == '(QUESTIONCATEGORY)' or i[2].decode('utf8') == '(EXCLAMATIONCATEGORY)'
                        or i[2].decode('utf8') == '(SEMICOLONCATEGORY)' or i[2].decode('utf8') == '(COLONCATEGORY)'
                        or i[2].decode('utf8') == '(AUTHOR)'):
                        check = True
                
                if len(temp_line) != 0:
                    #print ('*'+temp_line)
                    f.write (temp_line.strip()+'\r\n')
                    
                check = False

finally:
    connection.close()
    
print ('END')


# In[54]:

#提取分析 1273711行 3533區分段
import codecs

path = "C:\\Users\\user\\Desktop\\FreeChina\\{}_All.txt"

files = []
for i in range(23):
    if i < 9:
        files.append('0'+str(i+1))
    else:
        files.append(str(i+1))

t = 0        
        
for file in files:
    with codecs.open(path.format(file),'r','utf8') as f:
        
        temp = f.readlines()
        
        for content in temp:
        
            if content[0] == '#':
                
                content = content.split()
                
                content[2] = ''.join(content[2:5])
                del content[3:5]
                del content[0]
                if len(content) > 4:
                    content[2] = ''.join(content[2:-1])
                    del content[3:-1]
                    #print (content)
                else:
                    #print (content)
                    pass
                
                t = t + 1
print (t)
   


# In[64]:

#情態動詞分析 1273711行 
import codecs
import time

modalverb = ["應","要","可","能","可以","須","應該","必須","會","得","需要","當","應當","能夠","該","需"]
path = "C:\\Users\\user\\Desktop\\FreeChina\\{}_All.txt"

files = []
for i in range(23):
    if i < 9:
        files.append('0'+str(i+1))
    else:
        files.append(str(i+1))

two_verb = {}
        
for file in files:
    with codecs.open(path.format(file),'r','utf8') as f:
        
        content = f.readlines()
        
        for line in content:
            
            if line[0] != '#':
                
                words = line.split()
                verb_list = []
                
                for word in words:
                    if word[0] == '(' or word[0] == '（':
                        word = [word[0],word[1:]]
                    else:
                        word = word.split('(')
                        word[1] = '('+word[1]

                    if word[0] in modalverb:
                        verb_list.append(''.join(word))

                if len(verb_list) >= 2:
                    for l in range(len(verb_list)-1):
                        k = l + 1
                        if (verb_list[l],verb_list[k]) in two_verb:
                            two_verb[(verb_list[l],verb_list[k])] = two_verb[(verb_list[l],verb_list[k])] + 1
                        else:
                            two_verb[(verb_list[l],verb_list[k])] = 1

two_verb_count = 0

for i in two_verb:
    two_verb_count = two_verb_count + two_verb[i]
    
two_verb = sorted(two_verb.items(), key=lambda d:d[1], reverse = True)

print (len(two_verb)) #488
print (two_verb_count) #6418

for i in two_verb:
    print (i[0],i[1])


# In[73]:

#情態動詞尋找 1273711行 
#02 15457 16080兩段資料似乎重複
#有引用句也會導致重複
import codecs
import time
from colorama import init

modalverb = ["應","要","可","能","可以","須","應該","必須","會","得","需要","當","應當","能夠","該","需"]
path = "C:\\Users\\user\\Desktop\\FreeChina\\{}_All.txt"

files = []
for i in range(23):
    if i < 9:
        files.append('0'+str(i+1))
    else:
        files.append(str(i+1))
        
find = ['要(D)', '能(D)']

two_verb = {}
        
for file in files:
    with codecs.open(path.format(file),'r','utf8') as f:
        
        content = f.readlines()
        print (file)
        
        for line in content:
            
            if line[0] != '#':
                
                words = line.split()
                verb_list = []
                verb_index = []
                verb_index_a = []
                check = False
                index = 0
                
                for word in words:
                    if word[0] == '(' or word[0] == '（':
                        word = [word[0],word[1:]]
                    else:
                        word = word.split('(')
                        word[1] = '('+word[1]

                    if word[0] in modalverb:
                        verb_list.append(''.join(word))
                        verb_index.append(index)
                    index = index + 1

                if len(verb_list) >= 2:
                    for l in range(len(verb_list)-1):
                        k = l + 1
                        if find[0] == verb_list[l] and find[1] == verb_list[k]:
                            check = True
                            if verb_index[l] not in verb_index_a:
                                verb_index_a.append(verb_index[l])
                            if verb_index[k] not in verb_index_a:
                                verb_index_a.append(verb_index[k])
                
                for i in verb_index_a:
                    words[i] = '\033[31;46m' + words[i] + '\033[0m'
                            
                
                if check:
                    print (''.join(words))
                    time.sleep(0.3)
                    
                    

