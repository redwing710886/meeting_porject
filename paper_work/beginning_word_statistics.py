
# coding: utf-8

# In[8]:

#自由中國開頭資料匯入
import os
import codecs
import time

path = "C:\\Users\\user\\Desktop\\課業相關\\碩士班\\SNA\\meeting\\source\\FreeChina\\"
out_path = "C:\\Users\\user\\Desktop\\Cbb&P\\作者\\"
desktop_path = "C:\\Users\\user\\Desktop\\"

file_list = []

for file in os.listdir(path):
    file_list.append(file)


# In[2]:

#自由中國作者計算
author = {} 

count = 0 #無作者

for file in file_list:
    with codecs.open(path+file,'rb','utf8') as f:
        content = f.readlines()

        for line in content:
            if line[0] == '#':
                lines = line.split()

                if lines[-1].split('(')[1][0:-1] == 'AUTHOR':
                    name = lines[-1].split('(')[0]

                    if name not in author:
                        author[name] = 1
                    else:
                        author[name] += 1
                else:
                    count += 1

authors = sorted(author.items(), key=lambda d:d[1], reverse = True) 

print ("無作者",count)

#印出作者與發表篇數
for i in authors:
    print (i[0],i[1])


# In[9]:

#開頭詞彙數量比較
header = {}

for file in file_list:
    with codecs.open(path+file,'rb','utf8') as f:
        content = f.readlines()

        check = False
        head = ""

        for line in content:
            if line[0] != '#':
                lines = line.split()

                if not check:
                    head = lines[0]#.split('(')[0]
                    check = True
                if len(lines[-1].split('(')) == 2:
                    if lines[-1].split('(')[1][0:-1] == 'PERIODCATEGORY':
                        if head.split('(')[1][0:-1] == 'Cbb' or head.split('(')[1][0:-1] == 'P':
                            if head not in header:
                                header[head] = 1
                            else:
                                header[head] += 1
                        check = False
                    
header = sorted(header.items(), key=lambda d:d[1], reverse = True) 

with codecs.open(desktop_path+'all2.txt','wb','utf8') as g:
    for i in header:
        #print (i[0],i[1])
        g.write(str(i[0])+' '+str(i[1])+'\r\n')

print ("END")


# In[12]:

#匯出各作者的開頭詞彙分布
import time

for file in file_list:
    
    block = False
    information = ''
    author = ''
    head = ''
    header = {}
    check = False
    count = 0
    
    with codecs.open(path+file,'rb','utf8') as f:
        content = f.readlines()
                
        
        for line in content:
            line = line.split()
            
            if line[0] == '#':
                check = False
                if block:
                    with codecs.open(out_path+author+'.txt','ab','utf8') as g:
                        g.write(information+' '+file+' '+str(count)+' \r\n')
                        headers = sorted(header.items(), key=lambda d:d[1], reverse = True)
                        for i in headers:
                            g.write(str(i[0])+' '+str(i[1])+'\r\n')
                    information = ''
                    author = ''
                    head = ''
                    header = {}
                    count = 0
                block = True        
                information = ' '.join(line)        
                if line[-1].split('(')[1][0:-1] == 'AUTHOR':
                    author = line[-1].split('(')[0]
                else:
                    author = 'UNKNOWN'
            else:
                
                count += len(line)
                
                if not check:
                    #if len(line[0]) != 0:
                    #head = line[0].split('(')[0]
                    head = line[0]
                    check = True
                if len(line[-1].split('(')) == 2:
                    if line[-1].split('(')[1][0:-1] == 'PERIODCATEGORY':
                        if head.split('(')[1][0:-1] == 'Cbb' or head.split('(')[1][0:-1] == 'P':
                            if head not in header:
                                header[head] = 1
                            else:
                                header[head] += 1
                        check = False
                        
    if block:
        with codecs.open(out_path+author+'.txt','ab','utf8') as g:
            g.write(information+' '+file+' '+str(count)+' \r\n')
            headers = sorted(header.items(), key=lambda d:d[1], reverse = True)
            for i in headers:
                g.write(str(i[0])+' '+str(i[1])+'\r\n')
                        
'''with codecs.open(out_path+author+'.txt','ab','utf8') as g:
    g.write(information+'\r\n')
    headers = sorted(header.items(), key=lambda d:d[1], reverse = True)
    for i in headers:
        g.write(str(i[0])+' '+str(i[1])+'\r\n')'''
        
print ('END')


# In[4]:

#整理出各作者的詞彙向量
out_path2 = 'C:\\Users\\user\\Desktop\\Cbb&P\\開頭詞向量空間\\'

author_list = []

for file in os.listdir(out_path):
    author_list.append(file)

for name in author_list:    

    bag = {}

    with codecs.open(out_path+name,'rb','utf8') as f:
        content = f.readlines()

        for line in content:
            line = line.split()

            if line[0] != '#' and len(line) != 0:
                if line[0] not in bag:
                    bag[line[0]] = int(line[1])
                else:
                    bag[line[0]] += int(line[1])

    bags = sorted(bag.items(), key=lambda d:d[1], reverse = True)

    bag_list = []
    bag_table = {}
    title_list = []

    for i in bags:
        bag_list.append(i[0])
        bag_table[i[0]] = []

    with codecs.open(out_path+name,'rb','utf8') as f:
        content = f.readlines()

        head_temp = []

        for line in content:
            line = line.split()

            check = False

            if line[0] == '#':
                title_list.append(' '.join(line[5:-4])+' '+line[-4].split('(')[0])
                if len(head_temp) != 0:
                    for i in bag_list:
                        if i in head_temp:
                            bag_table[i].append(1)
                        else:
                            bag_table[i].append(0)
                    head_temp = []
            elif len(line) != 0:
                head_temp.append(line[0])

        if len(head_temp) != 0:
            for i in bag_list:
                if i in head_temp:
                    bag_table[i].append(1)
                else:
                    bag_table[i].append(0)

    with codecs.open(out_path2+'.'.join(name.split('.')[0:-1])+'.csv','wb','utf8') as g:
        temp = ''
        for i in title_list:
            temp += i+','
        g.write('詞彙,'+temp[0:-1]+'\r\n')
        for i in bag_list:
            #print (i,bag_table[i])
            g.write(i)
            for j in bag_table[i]:
                g.write(','+str(j))
            g.write('\r\n')
            
print ('END')


# In[34]:

#對特定作者找出特定詞彙的分布網路
out_path3 = "C:\\Users\\user\\Desktop\\Cbb&P\\以自由中國為基準\\特定作者開頭詞向量空間(比例)\\"
out_path4 = "C:\\Users\\user\\Desktop\\Cbb&P\\以自由中國為基準\\特定作者開頭詞向量空間(正規化)\\"

author_names = ["雷震","龍平甫","殷海光","蔣勻田","徐訏","胡適","羅鴻詔","陳之藩","孟瑤","朱伴耘"]
beginning = []

with codecs.open(desktop_path+"all2.txt",'rb','utf8') as f:
    content = f.readlines()
    
    for i in content:
        if int(i.split()[1]) > 1000:
            beginning.append(i.split()[0])
        else:
            break
            
for name in author_names:
    
    
    context = {}
    title = ''
    pair = {}
    
    with codecs.open(out_path+name+'.txt','rb','utf8') as f:
        content = f.readlines()
        
        for line in content:
            line = line.split()
            
            if line[0] == '#':
                if len(pair) != 0 and title != '':
                    for i in beginning:
                        if i in pair:
                            context[title].append(pair[i])
                        else:
                            context[title].append(0)
                    title = ''
                    pair = {}
                            
                title = ' '.join(line[5:-4])+' '+line[-4].split('(')[0]
                title = ' '.join(title.split(','))+'@'+line[-1]
                context[title] = []
            else:
                pair[line[0]] = int(line[1])
            
        if len(pair) != 0 and title != '':
            for i in beginning:
                if i in pair:
                    context[title].append(pair[i])
                else:
                    context[title].append(0)
        
    with codecs.open(out_path4+name+'.csv','wb','utf8') as g:
        
        g.write("題目\開頭詞")
        for i in beginning:
            g.write(','+i)
        g.write('\r\n')
        
        for i in context:
            g.write(i.split('@')[0])
            
            temp = 0
            for j in context[i]:
                temp += j
                
            for j in context[i]:
                '''if temp != 0:
                    g.write(','+str(round(j/temp,5)))
                else:
                    g.write(','+str(0))'''
                try:
                    g.write(','+str(round((j/int(i.split('@')[1]))*1000000,5)))
                except:
                    print (name,i)
            g.write('\r\n')
            
print ('END')


# In[23]:

#抓出平衡語料庫的Cbb&P
import xml.etree.ElementTree as ET

scs_path = 'C:\\Users\\user\\Desktop\\課業相關\\碩士班\\SNA\\meeting\\source\\SCS_4.0\\'

scs_list = []

for file in os.listdir(scs_path):
    scs_list.append(file)
    
beginning = {}
    
for file in scs_list:
    
    tree = ET.parse(scs_path+file)
    root = tree.getroot()
    
    check = False
    head = ''
    
    for sentence in root.iter('sentence'):
        try:
            temp = sentence.text.split()
            if not check:
                if len(temp[0].split('(')) == 2:
                    head = temp[0]
                    check = True
            if len(head) != 0 and temp[-1].split('(')[1][0:-1] == 'PERIODCATEGORY':
                if head.split('(')[1][0:-1] == 'Cbb' or head.split('(')[1][0:-1] == 'P':
                    if head not in beginning:
                        beginning[head] = 1
                    else:
                        beginning[head] += 1
                head = ''
                check = False
        except:
            #print (head,sentence.text)
            #time.sleep(0.5)
            continue

beginning = sorted(beginning.items(), key=lambda d:d[1], reverse = True)

with codecs.open(desktop_path+'scs_all.txt','wb','utf8') as g:
    for i in beginning:
        #print (i[0],i[1])
        g.write(i[0]+' '+str(i[1])+'\r\n')
    
print ('END')

