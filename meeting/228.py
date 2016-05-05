
# coding: utf-8

# In[1]:

#建立228句子
import pymysql
import time
import codecs

connection = pymysql.connect(host="140.119.164.170", user="salan40319", passwd="104753018", db="228",charset='utf8')
output_path = "C:/Users/user/Desktop/228/"

file = []

for i in range(9):
    file.append('0'+str(i+1)+'_bak')
file.append('10')

try:
    for f in file:
        with connection.cursor() as cursor:
            sql = "select * from `{}`"
            
            cursor.execute(sql.format(f))
            
            line = ''
            full = ''
            
            print (f)
            temp = ''
            temp_full = ''
            
            with codecs.open(output_path+f+'.txt','w','utf8') as t:
                for i in cursor:
                    try:
                        line = line + i[1].decode('utf8')
                        if len(i[1].decode('utf8').strip()) != 0:
                            full = full + i[1].decode('utf8') + i[2].decode('utf8') + ' '
                        if (i[2].decode('utf8') == '(PERIODCATEGORY)' or i[2].decode('utf8') == '(COMMACATEGORY)' 
                            or i[2].decode('utf8') == '(EXCLAMATIONCATEGORY)' or i[2].decode('utf8') == '(SEMICOLONCATEGORY)' 
                            or i[2].decode('utf8') == '(COLONCATEGORY)'):
                            line = line.strip()
                            if len(line) == 2:
                                temp = line
                                temp_full = full
                            elif len(line) > 2:
                                if len(temp) != 0:
                                    line = temp + line
                                    full = temp_full + full
                                    temp = ''
                                    temp_full = ''
                                #print (full)
                                t.write(full+'\r\n')
                                #time.sleep(0.3)
                            line = ''
                            full = ''
                    except:
                        #如果有無法判斷的單字
                        print (line,i)
                        line = line + 'Error'
                        full = full + 'Error' + '(error)' + ' '
                #print (full)
                t.write(full+'\r\n')
finally:
    connection.close()


# In[3]:

#情態動詞分析 86590
import codecs
import time
import os

modalverb = ["應","要","可","能","可以","須","應該","必須","會","得","需要","當","應當","能夠","該","需"]
file_path = "C:\\Users\\user\\Desktop\\228\\"

file_list = []

for file in os.listdir(file_path):
    file_list.append(file)

two_verb = {}
line_index = 0
        
for file in file_list:
    with codecs.open(file_path+file,'r','utf8') as f:
        
        content = f.readlines()
        
        for line in content:
            
            line_index = line_index + 1
            
            if line[0] != '#':
                
                words = line.split()
                verb_list = []
                
                for word in words:
                    try:
                        if word[0] == '(' or word[0] == '（':
                            word = [word[0],word[1:]]
                        else:
                            word = word.split('(')
                            word[1] = '('+word[1]

                        if word[0] in modalverb:
                            verb_list.append(''.join(word))
                    except:
                        #print (file,word)
                        pass

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

print (len(two_verb)) #143/139
print (two_verb_count) #628/607
print (line_index) #86590/88810

for i in two_verb:
    print (i[0],i[1])

