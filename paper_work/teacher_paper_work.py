
# coding: utf-8

# In[12]:

#計算個數
import os 
import codecs
# 627464 459489 146480
path = "C:\\Users\\user\\Desktop\\雷震處理資料\\source\\文章+社論\\"

total = 0

file_list = []

for file in os.listdir(path):
    file_list.append(file)
    
for file in file_list:
    with codecs.open(path+file,'rb','utf8') as f:
        head = f.readline()
        content = f.readlines()
        
        for line in content:
            #total += len(line.split())
            line2 = line.split()
            for i in line2:
                if i.split('(')[0] != '':
                    total += len(i.split('(')[0])
    #print (file)
            
print (total)


# In[53]:

#計算頻率
import os 
import codecs
# 627464 459489 146480
path = "C:\\Users\\user\\Desktop\\mo\\"

file_list = []

for file in os.listdir(path):
    file_list.append(file)
    
for file in file_list:
    count = 0
    with codecs.open(path+file,'rb','utf8') as f:
        #head = f.readline()
        content = f.readlines()
        
        for line in content:
            count += int(line.split(',')[1])
        print (file,count)


# In[ ]:

#程式碼有少
#資料庫連接
import pymysql
import time
import codecs

#host位置為該資料庫所在ip位置，此例127.0.0.1為本機位置
connection = pymysql.connect(host="140.119.164.170", user="salan40319", passwd="104753018", db="FreeChina_updated",charset='utf8')
out_path = "C:\\Users\\user\\Desktop\\日記\\"

try:
    with connection.cursor() as cursor:
        sql = "SELECT * FROM `Leichen`" #基本sql指令
        cursor.execute(sql)
        
        #提取出的資料必須以遞迴形式拿出
        
        head = ['(DATETIME)','(SEQUENCE)','(TITLE)','(AUTHOR)']
        title = []
        content = []
        check = False
        count = 1
        
        for i in cursor:
            word = i[1].decode('utf8')
            pos = i[2].decode('utf8')
            
            if pos in head:
                if pos == '(DATETIME)':
                    if len(content) != 0:
                        with codecs.open(out_path+str(count)+'.txt','wb','utf8') as g:
                            for i in title:
                                g.write(i+' ')
                            g.write('\r\n')
                            g.write(' '.join(content)+'\r\n')
                        title = []
                        content = []
                        print (count)
                        count += 1
                title.append(word)
            else:
                content.append(word+pos)
            
            
            
finally:
    connection.close()


# In[ ]:

#資料庫連接
import pymysql
import time
import codecs

#host位置為該資料庫所在ip位置，此例127.0.0.1為本機位置
connection = pymysql.connect(host="140.119.164.170", user="salan40319", passwd="104753018", db="FreeChina_updated",charset='utf8')
out_path = "C:\\Users\\user\\Desktop\\新雷震日記母體\\"

path = "C:\\Users\\user\\Desktop\\"
book = []

with codecs.open(path+'文藝.txt','rb','utf8') as f:
    content = f.readlines()
    
    for line in content:
        line = line.strip()
        
        book.append(line)

free = ['01','02','03','04','05','06','07','08','09','10','11','12','13','14','15','16','17','18','19','20','21','22','23']
count = 1

try:
    with connection.cursor() as cursor:
        
        for k in free:
            print (k)
            sql = "SELECT * FROM `{}`" #基本sql指令
            cursor.execute(sql.format(k+'_All'))

            #提取出的資料必須以遞迴形式拿出

            head = ['(DATETIME)','(SEQUENCE)','(TITLE)','(AUTHOR)']
            title = []
            content = []
            author = ''
            title2 = ''

            for i in cursor:
                word = i[1].decode('utf8')
                pos = i[2].decode('utf8')

                if pos in head:
                    if pos == '(DATETIME)':
                        if author == '雷震' or author == '社論(雷震)' or title2 in book:
                            check = True
                            title = []
                            content = []
                        elif len(content) != 0:
                            with codecs.open(out_path+str(count)+'.txt','wb','utf8') as g:
                                for i in title:
                                    g.write(i+' ')
                                g.write('\r\n')
                                g.write(' '.join(content)+'\r\n')
                            title = []
                            content = []
                            #print (count)
                            count += 1
                    if pos == '(AUTHOR)':
                        author = word #若沒有(AUTHOR)
                    if pos == '(TITLE)':
                        title2 = word
                    title.append(word)
                else:
                    content.append(word+pos)
                    
        if author != '雷震' and author != '社論(雷震)' and title2 not in book:
            with codecs.open(out_path+str(count)+'.txt','wb','utf8') as g:
                for i in title:
                    g.write(i+' ')
                g.write('\r\n')
                g.write(' '.join(content)+'\r\n')
            
            
finally:
    connection.close()
    
print ('END')


# In[1]:

#資料庫連接
#自由中國 all update
import pymysql
import time
import codecs

#host位置為該資料庫所在ip位置，此例127.0.0.1為本機位置
connection = pymysql.connect(host="140.119.164.170", user="salan40319", passwd="104753018", db="FreeChina_updated",charset='utf8')
out_path = "C:\\Users\\user\\Desktop\\自由中國\\"

path = "C:\\Users\\user\\Desktop\\"

free = ['01','02','03','04','05','06','07','08','09','10','11','12','13','14','15','16','17','18','19','20','21','22','23']
count = 1

try:
    with connection.cursor() as cursor:
        
        for k in free:
            sql = "SELECT * FROM `{}`" #基本sql指令
            cursor.execute(sql.format(k+'_All'))

            #提取出的資料必須以遞迴形式拿出

            head = ['(DATETIME)','(SEQUENCE)','(TITLE)','(AUTHOR)']
            title = []
            content = []

            for i in cursor:
                word = i[1].decode('utf8')
                pos = i[2].decode('utf8')

                if pos in head:
                    if pos == '(DATETIME)':
                        if len(content) != 0:
                            with codecs.open(out_path+str(count)+'.txt','wb','utf8') as g:
                                for i in title:
                                    g.write(i+' ')
                                g.write('\r\n')
                                g.write(' '.join(content)+'\r\n')
                            title = []
                            content = []
                            #print (count)
                            count += 1
                    title.append(word)
                else:
                    content.append(word+pos)
                    
            with codecs.open(out_path+str(count)+'.txt','wb','utf8') as g:
                for i in title:
                    g.write(i+' ')
                g.write('\r\n')
                g.write(' '.join(content)+'\r\n')
                count += 1
            print (k,count-1)
            
            
finally:
    connection.close()
    
print ('END')


# In[ ]:

#資料庫連接
import pymysql
import time
import codecs

#host位置為該資料庫所在ip位置，此例127.0.0.1為本機位置
connection = pymysql.connect(host="140.119.164.170", user="salan40319", passwd="104753018", db="LeiChen_peryear",charset='utf8')
out_path = "C:\\Users\\user\\Desktop\\日記\\"


try:
    with connection.cursor() as cursor:
        sql = "SELECT * FROM `{}`" #基本sql指令

        for num in range(1948,1978):
            cursor.execute(sql.format(num))
            content = []

            for i in cursor:
                word = i[1].decode('utf8')
                pos = i[2].decode('utf8')
                if word == ' ' or word == '' or pos == '(FW)' or pos == '' or pos == ' ' or pos == '(':
                    continue
                content.append(word+pos)
                
            with codecs.open(out_path+str(num)+'.txt','wb','utf8') as g:
                g.write(' '.join(content)+'\r\n')

finally:
    connection.close()

print ('END')


# In[1]:

#資料庫連接
import pymysql
import time
import codecs

connection = pymysql.connect(host="140.119.164.170", user="salan40319", passwd="104753018", db="LeiChen_peryear",charset='utf8')
out_path = "C:\\Users\\user\\Desktop\\雷震處理資料\\二版\\chunk\\雷震日記\\1971~1977\\"
#N+N N+V VH+N D+V

N_N = {}
N_V = {}
VH_N = {}
D_V = {}

try:
    with connection.cursor() as cursor:
        sql = "SELECT * FROM `{}`"#基本sql指令
        
        for num in range(1971,1978):
        
            '''first = ''
            first_pos = ''
            second = ''
            second_pos = ''
            
            cursor.execute(sql.format(num))

            for i in cursor:
                first = second
                first_pos = second_pos
                second = i[1].decode('utf8')
                second_pos = i[2].decode('utf8')
                
                if len(first_pos) > 1 and len(second_pos) > 1:
                    temp = first+' '+second
                    if first_pos[1] == 'N' and second_pos[1] == 'N' and first_pos[2] != 'e' and second_pos[2] != 'e' \
                        and first_pos[2] != 'f' and second_pos[2] != 'f' and first_pos[2] != 'h' and second_pos[2] != 'h':
                        if temp not in N_N:
                            N_N[temp] = 1
                        else:
                            N_N[temp] += 1
                    elif first_pos[1] == 'N' and second_pos[1] == 'V' and first_pos[2] != 'e' and first_pos[2] != 'f' \
                        and first_pos[2] != 'h':
                        if temp not in N_V:
                            N_V[temp] = 1
                        else:
                            N_V[temp] += 1
                    elif first_pos[1] == 'V' and first_pos[2] == 'H' and second_pos[1] == 'N' and second_pos[2] != 'e' \
                        and second_pos[2] != 'f' and second_pos[2] != 'h':
                        if temp not in VH_N:
                            VH_N[temp] = 1
                        else:
                            VH_N[temp] += 1
                    elif first_pos[1] == 'D' and second_pos[1] == 'V':
                        if temp not in D_V:
                            D_V[temp] = 1
                        else:
                            D_V[temp] += 1'''
                            
finally:
    connection.close()
    
'''N_N = sorted(N_N.items(), key=lambda d:d[1], reverse = True)
N_V = sorted(N_V.items(), key=lambda d:d[1], reverse = True)
VH_N = sorted(VH_N.items(), key=lambda d:d[1], reverse = True)
D_V = sorted(D_V.items(), key=lambda d:d[1], reverse = True)

with codecs.open(out_path+'N_N.csv','wb','utf8') as g:
    for i in N_N:
        g.write(str(i[0])+','+str(i[1])+'\r\n')
        
with codecs.open(out_path+'N_V.csv','wb','utf8') as g:
    for i in N_V:
        g.write(str(i[0])+','+str(i[1])+'\r\n')

with codecs.open(out_path+'VH_N.csv','wb','utf8') as g:
    for i in VH_N:
        g.write(str(i[0])+','+str(i[1])+'\r\n')
        
with codecs.open(out_path+'D_V.csv','wb','utf8') as g:
    for i in D_V:
        g.write(str(i[0])+','+str(i[1])+'\r\n')'''
    
print ('END')


# In[ ]:

import os
import codecs
import time

path = "C:\\Users\\user\\Desktop\\雷震處理資料\\source\\文章+社論\\"
out_path = 'C:\\Users\\user\\Desktop\\雷震處理資料\\二版\\chunk\\'

N_N = {}
N_V = {}
VH_N = {}
D_V = {}

file_list = []

for file in os.listdir(path):
    file_list.append(file)
    
for file in file_list:
    with codecs.open(path+file,'rb','utf8') as f:
        head = f.readline()
        content = f.readlines()
        
        first = ''
        first_pos = ''
        second = ''
        second_pos = ''
        
        for line in content:
            line = line.split()
            for word in line:
                first = second
                first_pos = second_pos
                second = word.split('(')[0]
                second_pos = '('+word.split('(')[1]
                
                if len(first_pos) > 1 and len(second_pos) > 1:
                    temp = first+' '+second
                    if first_pos[1] == 'N' and second_pos[1] == 'N' and first_pos[2] != 'e' and second_pos[2] != 'e'                         and first_pos[2] != 'f' and second_pos[2] != 'f' and first_pos[2] != 'h' and second_pos[2] != 'h':
                        if temp not in N_N:
                            N_N[temp] = 1
                        else:
                            N_N[temp] += 1
                    elif first_pos[1] == 'N' and second_pos[1] == 'V' and first_pos[2] != 'e' and first_pos[2] != 'f'                         and first_pos[2] != 'h':
                        if temp not in N_V:
                            N_V[temp] = 1
                        else:
                            N_V[temp] += 1
                    elif first_pos[1] == 'V' and first_pos[2] == 'H' and second_pos[1] == 'N' and second_pos[2] != 'e'                         and second_pos[2] != 'f' and second_pos[2] != 'h':
                        if temp not in VH_N:
                            VH_N[temp] = 1
                        else:
                            VH_N[temp] += 1
                    elif first_pos[1] == 'D' and second_pos[1] == 'V':
                        if temp not in D_V:
                            D_V[temp] = 1
                        else:
                            D_V[temp] += 1
                            
                            
N_N = sorted(N_N.items(), key=lambda d:d[1], reverse = True)
N_V = sorted(N_V.items(), key=lambda d:d[1], reverse = True)
VH_N = sorted(VH_N.items(), key=lambda d:d[1], reverse = True)
D_V = sorted(D_V.items(), key=lambda d:d[1], reverse = True)

total = 0
with codecs.open(out_path+'N_N.csv','wb','utf8') as g:
    for i in N_N:
        '''if float(total/1179960) > 0.33:
            total = 0
            break'''
        g.write(str(i[0])+','+str(i[1])+'\r\n')
        total += i[1]
    
        
with codecs.open(out_path+'N_V.csv','wb','utf8') as g:
    for i in N_V:
        '''if float(total/551930) > 0.33:
            total = 0
            break'''
        g.write(str(i[0])+','+str(i[1])+'\r\n')
        total += i[1]

with codecs.open(out_path+'VH_N.csv','wb','utf8') as g:
    for i in VH_N:
        '''if float(total/110488) > 0.33:
            total = 0
            break'''
        g.write(str(i[0])+','+str(i[1])+'\r\n')
        total += i[1]
        
with codecs.open(out_path+'D_V.csv','wb','utf8') as g:
    for i in D_V:
        '''if float(total/661501) > 0.33:
            total = 0
            break'''
        g.write(str(i[0])+','+str(i[1])+'\r\n')
        total += i[1]
    
print ('END')


# In[ ]:

#資料庫連接
import pymysql
import time
import codecs

connection = pymysql.connect(host="140.119.164.170", user="salan40319", passwd="104753018", db="LeiChen_peryear",charset='utf8')
out_path = "C:\\Users\\user\\Desktop\\雷震處理資料\\二版\\否定\\雷震日記\\1971~1977\\"

non = ['沒','非','無','否','不','勿','毋','未','甭','莫']
non_dic = {}
for i in non:
    non_dic[i] = {}

try:
    with connection.cursor() as cursor:
        sql = "SELECT * FROM `{}`"#基本sql指令
        
        for num in range(1971,1978):
        
            first = ''
            second = ''
            
            cursor.execute(sql.format(num))

            for i in cursor:
                first = second
                second = i[1].decode('utf8')
                if 'CATEGORY' in i[2].decode('utf8'):
                    second = ''
                    continue
                
                temp = first+' '+second
                
                if first in non:
                    if temp not in non_dic[first]:
                        non_dic[first][temp] = 1
                    else:
                        non_dic[first][temp] += 1
                            
                            
finally:
    connection.close()
    
for i in non_dic:
    temp = sorted(non_dic[i].items(), key=lambda d:d[1], reverse = True)
    with codecs.open(out_path+i+'.csv','wb','utf8') as g:
        for j in temp:
            g.write(str(j[0])+','+str(j[1])+'\r\n')

print ('END')


# In[ ]:

import os
import codecs
import time

path = "C:\\Users\\user\\Desktop\\雷震處理資料\\source\\文章+社論\\"
out_path = 'C:\\Users\\user\\Desktop\\雷震處理資料\\二版\\否定\\文章+社論否定\\'

non = ['沒','非','無','否','不','勿','毋','未','甭','莫']
non_dic = {}
for i in non:
    non_dic[i] = {}

file_list = []

for file in os.listdir(path):
    file_list.append(file)
    
for file in file_list:
    with codecs.open(path+file,'rb','utf8') as f:
        head = f.readline()
        content = f.readlines()
        
        first = ''
        second = ''
        
        for line in content:
            line = line.split()
            for word in line:
                first = second
                second = word.split('(')[0]
                if 'CATEGORY' in word.split('(')[1]:
                    second = ''
                    continue

                temp = first+' '+second

                if first in non:
                    if temp not in non_dic[first]:
                        non_dic[first][temp] = 1
                    else:
                        non_dic[first][temp] += 1

total = 0
#fre = {'沒':78203,'非':92377,'無':86686,'否':92725,'不':76177,'勿':76471,'毋':92510,'未':6783,'甭':86700,'莫':87003}
for i in non_dic:  
    temp = sorted(non_dic[i].items(), key=lambda d:d[1], reverse = True)
    with codecs.open(out_path+i+'.csv','wb','utf8') as g:
        for j in temp:
            '''if float(total/fre[i]) > 0.33:
                total = 0
                break'''
            g.write(str(j[0])+','+str(j[1])+'\r\n')
            total += j[1]
print ('END')


# In[48]:

#寫入資料庫
#資料庫連接
import pymysql
import codecs
import time
import os 

find = input('請輸入資料表名稱')

path = 'C:\\Users\\user\\Desktop\\leichen\\'+find+'\\'

file_list = []

for file in os.listdir(path):
    file_list.append(file)

#host位置為該資料庫所在ip位置，此例127.0.0.1為本機位置
connection = pymysql.connect(host="127.0.0.1", user="redwing", passwd="", db="leichen",charset='utf8')

try:
    with connection.cursor() as cursor:
        
        '''check_sql = "select * from chunk where `word` = \"{}\""
        insert_sql = "INSERT into chunk(word,comparison) values(\"{}\",{})" #前者為table及其屬性，後者為要放進去的值
        update_sql = "UPDATE chunk SET `article` = {} where `word` = \"{}\""'''
        
        sql = "INSERT INTO {}(word,{}) values(\"{}\",{}) ON DUPLICATE KEY UPDATE `{}` = {}"
        
        
        for file in file_list:
            
            with codecs.open(path+file,'rb','utf8') as f:
            #with open(path+file,'rb') as f:
                head = f.readline()
                content = f.readlines()

                total = 0
                l_num = 0
                
                for line in content:
                    #line = line.decode('big5').strip()
                    line = line.strip()
                    if line.split(',')[0] == '':
                        continue
                    total += int(line.split(',')[1])
                    l_num += 1

                temp_sum = 0
                gap = 0.33

                for line in content:
                    #line = line.decode('big5').strip()
                    line = line.strip()
                    if line.split(',')[0] == '':
                        continue
                    temp_sum += int(line.split(',')[1])
                    count = 0
                    gap_count = int((int(line.split(',')[1])/total)/gap)

                    if 0.33 >= temp_sum/total:
                        count = 1
                    elif 0.66 >= temp_sum/total:
                        count = 2-gap_count
                    elif 1 >= temp_sum/total:
                        count = 3-gap_count
                        
                    if count not in [1,2,3]:
                        print (line.split(',')[0],count)
                        count = 1
                        
                    #這兩行可以直接動態加入想要的值，而不用修改程式碼
                    word = line.split(',')[0]
                    '''cursor.execute(check_sql.format(word))
                    
                    check_count = 0
                    for i in (cursor): 
                        check_count += 1
                    if check_count == 0:
                        cursor.execute(insert_sql.format(word,count))
                    else:
                        cursor.execute(update_sql.format(count,word))'''
                    cursor.execute(sql.format(find,file.split('.')[0],word,count,file.split('.')[0],count))
                        
                        
                print (file,l_num)
    
    #若有修改到資料庫，必須有這行才會執行動作
    connection.commit()   
finally:
    connection.close()
    
print ('END')


# In[32]:

#資料庫連接
import pymysql
import codecs

path = 'C:\\Users\\user\\Desktop\\mo\\'


#host位置為該資料庫所在ip位置，此例127.0.0.1為本機位置
connection = pymysql.connect(host="127.0.0.1", user="redwing", passwd="", db="leichen",charset='utf8')

dic = ['d_v','n_n','n_v','vh_n','','01_all','02_all','03_all','04_all','05_all','06_all','07_all','08_all','09_all','10_all']

try:
    with connection.cursor() as cursor:
        
        ty = []
        for one in range(3):
            for two in range(3):
                for three in range(3):
                    for four in range(2):
                        ty.append([one+1,two+1,three+1,four+1])
                    
        for roun in ty:
            
            print (roun)

            find = roun

            a = 0
            b = 0
            c = 0
            d = 0
            e = 0
            f = 0

            if find[0] == 3:
                a = 3
                b = 0
            else:
                a = find[0]
                b = find[0]

            if find[1] == 3:
                c = 3
                d = 0
            else:
                c = find[1]
                d = find[1]

            if find[2] == 3:
                e = 3
                f = 0
            else:
                e = find[2]
                f = find[2]

            name = ''
            sql = ''

            if find[3] == 1:
                name = 'time'
                sql = "select `word` from `{}` where (`year_first` = {} or `year_first` = {})                     and (`year_middle` = {} or `year_middle` = {}) and (`year_last` = {} or `year_last` = {})"
            elif find[3] == 2:
                name = 'category'
                sql = "select `word` from `{}` where (`30years` = {} or `30years` = {})                     and (`article` = {} or `article` = {}) and (`comparison` = {} or `comparison` = {})"
            

            with codecs.open(path+name+''.join(str(x) for x in find)+'.csv','wb','utf8') as g:

                for i in dic:
                    if i == '':
                        g.write('\r\n')
                        continue

                    cursor.execute(sql.format(i,a,b,c,d,e,f))
                    #print (i,a,b,c,d,e,f)
                    for j in cursor:
                        g.write(j[0]+',')
                    g.write('\r\n')
                       
finally:
    connection.close()
    
print ('END')
    


# In[5]:

import codecs
import os

path = "C:\\Users\\user\\Desktop\\新增資料夾\\"

find = input()

file_list = []

for file in os.listdir(path):
    file_list.append(file)
    
for file in file_list:
    total = 0
    count = 0
    with codecs.open(path+file,'rb','utf8') as f:
        content = f.readlines()
        
        for line in content:
            line = line.split(',')
            
            if find in line[0]:
                #if file == '02.csv':
                #print (line[0])
                count += 1
                total += int(line[1])
                
        print (file,count,total)
        

