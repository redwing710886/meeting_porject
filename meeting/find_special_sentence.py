
# coding: utf-8

# In[ ]:

import pymysql
import time
import codecs

connection = pymysql.connect(host="140.119.164.170", user="salan40319", passwd="104753018", db="SinicaCorpus",charset='utf8')
find = {'我':[],'你':[],'他':[],'我們':[],'你們':[],'他們':[]}
node = {'1':{},'2':{},'3':{},'4':{},'5':{}}
out_path = 'C:\\Users\\user\\Desktop\\six\\'

try:
    for i in find:
        with connection.cursor() as cursor:
            sql = "select `id` from `corpus_segpos` where word = '{}'"
            cursor.execute(sql.format(i))
            
            for j in cursor:
                find[i].append(j[0])
    
    print ('first ok')
                
    with connection.cursor() as cursor:
        sql = "select * from `corpus_segpos` where id >= '{}' and id < '{}'"
        
        for k in find:
            with codecs.open(out_path+k+'.txt','wb','utf8') as f:
                for i in find[k]:
                    line = ''
                    cursor.execute(sql.format(i,i+6))
                    line_check = True
                    #count = 0

                    for j in cursor:
                        check = j[2].decode('utf8')
                        if check != '(PERIODCATEGORY)' and check != '(PAUSECATEGORY)' and check != '(PARENTHESISCATEGORY)'                             and check != '(QUESTIONCATEGORY)' and check != '(COMMACATEGORY)' and check != '(EXCLAMATIONCATEGORY)'                             and check != '(SEMICOLONCATEGORY)':
                            line = line + j[1].decode('utf8') + check
                        else:
                            line_check = False
                            break
                        '''if count != 0:
                            if (j[1].decode('utf8') + j[2].decode('utf8')) not in node[str(count)]:
                                node[str(count)][j[1].decode('utf8') + j[2].decode('utf8')] = 1
                            else:
                                node[str(count)][j[1].decode('utf8') + j[2].decode('utf8')] = \
                                    node[str(count)][j[1].decode('utf8') + j[2].decode('utf8')] + 1'''
                        #count += 1

                    #print (line)
                    #time.sleep(0.3)
                    if line_check:
                        f.write(line+'\r\n')
        
finally:
    connection.close()

'''for i in find:
    print (i,find[i][0:10])

for i in range(1,6):
    temp = sorted(node[str(i)].items(), key=lambda d:d[1], reverse = True)
    count = 0
    print (i)
    for j in temp:
        print (j[0],j[1])
        count += 1
        if count == 10:
            break
    print ()
    count = 0
    for j in temp:
        if j[0][1] != '(':
            print (j[0],j[1])
            count += 1
        if count == 10:
            break
    print ()'''

print ('end')


# In[6]:

import time
import codecs
import os
import xml.etree.ElementTree as ET
from ipywidgets import IntProgress
from IPython.display import display

find = ['我','你','他','我們','你們','他們']
find_dict = {'我':[],'你':[],'他':[],'我們':[],'你們':[],'他們':[]}
out_path = 'C:\\Users\\user\\Desktop\\six\\'
file_path = 'C:\\Users\\user\\Desktop\\課業相關\\碩士班\\SNA\\meeting\\source\\SCS_4.0\\'

file_list = []

for file in os.listdir(file_path):
    file_list.append(file)

p = IntProgress()
p.max = len(file_list)
p.description = 'start'
display(p)
all_count = 0

for file in file_list:
    
    tree = ET.parse(file_path+file)
    root = tree.getroot()

    for sentence in root.iter('sentence'):
        try:
            temp = sentence.text.split()
            count = 0
            line = []
            
            for word in temp:
                if word.split('(')[0] in find:# and len(temp)-count >= 6:
                    line.append(count)
                count += 1
            for i in line:
                find_dict[temp[i].split('(')[0]].append(' '.join(temp[i:]))
            line = []
        except:
            print ('error')
            continue
    
    all_count = all_count + 1
    p.value = all_count
    p.description = str(all_count)
            
for i in find_dict:
    with codecs.open(out_path+i+'.txt','wb','utf8') as f:
        for j in find_dict[i]:
            f.write(j+'\r\n')
    
                       
p.description = 'end'
print ('end')


# In[20]:

import codecs
import os 
import time

input_path = 'C:\\Users\\user\\Desktop\\six\\'
output_path = 'C:\\Users\\user\\Desktop\\six_out\\'

file_list = []

for file in os.listdir(input_path):
    file_list.append(file)
    
num = 6

for i in file_list:
    with codecs.open(input_path+i,'rb','utf8') as f:
        content = f.readlines()
        
        with codecs.open(output_path+i.split('.')[0]+'_out.txt','wb','utf8') as g:
            for j in content:
                temp = j.split()
                if len(temp) < (num+1):
                    continue
                count = 0
                line = ''
                
                for word in temp:
                    try:
                        check = '(' + word.split('(')[1]
                        if check != '(PERIODCATEGORY)' and check != '(PAUSECATEGORY)' and check != '(PARENTHESISCATEGORY)'                             and check != '(QUESTIONCATEGORY)' and check != '(COMMACATEGORY)' and check != '(EXCLAMATIONCATEGORY)'                             and check != '(SEMICOLONCATEGORY)' and count < num:
                                line = line + ' ' + word.split('[')[0]
                                count += 1
                        elif count >= num:
                            g.write(line[1:]+'\r\n')
                            #print (line)
                            #time.sleep(0.3)
                            break
                        else:
                            break
                    except:
                        print ('error'+word)
                        break
print ('end')


# In[8]:

import codecs
import os 
import time

input_path =  'C:\\Users\\user\\Desktop\\six_out\\'

file_list = []

for file in os.listdir(input_path):
    file_list.append(file)
    
for i in file_list:
    with codecs.open(input_path+i,'rb','utf8') as f:
        content = f.readlines()
        
        node = {'1':{},'2':{},'3':{},'4':{},'5':{}}
        
        for j in content:
            temp = j.split()[1:]
            count = 1
            
            for k in temp:
                #k = '('+k.split('(')[1]
                if k not in node[str(count)]:
                    node[str(count)][k] = 1
                else:
                    node[str(count)][k] += 1
                count += 1
        
        print (i)
        
        with codecs.open('C:\\Users\\user\\Desktop\\final\\'+i.split('.')[0]+'.csv','wb','utf8') as g:
            for j in range(1,6):
                temp = sorted(node[str(j)].items(), key=lambda d:d[1], reverse = True)
                count = 0
                #print (j)
                g.write(str(j)+'\r\n')
                for k in temp:
                    '''if k[0][0] == '的':
                        continue'''
                    #print (k[0],k[1])
                    g.write(k[0]+','+str(k[1])+'\r\n')
                    count += 1
                    '''if count == 20:
                        break'''
                g.write('\r\n')


# In[3]:

import xlwt
from datetime import datetime

style0 = xlwt.easyxf('font: name Times New Roman, color-index red, bold on',
    num_format_str='#,##0.00')
style1 = xlwt.easyxf(num_format_str='D-MMM-YY')

wb = xlwt.Workbook()
ws = wb.add_sheet('A Test Sheet')

ws.write(0, 0, 1234.56, style0)
ws.write(1, 0, datetime.now(), style1)
ws.write(2, 0, 1)
ws.write(2, 1, 1)
ws.write(2, 2, xlwt.Formula("A3+B3"))

wb.save('C:\\Users\\user\\Desktop\\example.xls')

