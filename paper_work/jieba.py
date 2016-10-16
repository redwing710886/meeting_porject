
# coding: utf-8

# In[ ]:

import jieba
import jieba.posseg as pseg

jieba.set_dictionary('dict.txt.big')

n = input()

words = pseg.cut(n)

for word, flag in words:
    print('%s %s' % (word, flag))


# In[ ]:

#SCS合併
import codecs
import jieba
import os
import xml.etree.ElementTree as ET
import time

jieba.set_dictionary('dict.txt.big')
scs_path = 'C:\\Users\\user\\Desktop\\課業相關\\碩士班\\SNA\\meeting\\source\\SCS_4.0\\CKIP\\'
desktop_path = "C:\\Users\\user\\Desktop\\"

scs_list = []

for file in os.listdir(scs_path):
    scs_list.append(file)
    
for file in scs_list:
    
    tree = ET.parse(scs_path+file)
    root = tree.getroot()
    
    with codecs.open(desktop_path+'all\\'+file.split('.')[0]+'.txt','wb','utf8') as g:
    

        for sentence in root.iter('sentence'):
            try:
                temp = sentence.text.split()

                line = ''
                for i in temp:
                    line += i.split('(')[0]

                g.write(''.join(line)+'\r\n')
            
            except:
                if sentence.text != None:
                    g.write('# '+sentence.text+'\r\n') 
print ('END')


# In[ ]:

#SCS合併 使用jieba斷詞
import codecs
import jieba
import jieba.posseg as pseg
import os
import time

jieba.set_dictionary('dict.txt.big')
scs_path = 'C:\\Users\\user\\Desktop\\課業相關\\碩士班\\SNA\\meeting\\source\\SCS_4.0\\jieba\\'
desktop_path = "C:\\Users\\user\\Desktop\\"

scs_list = []

for file in os.listdir(desktop_path+'all\\'):
    scs_list.append(file)
    
for file in scs_list:
    
    with codecs.open(desktop_path+'all\\'+file,'rb','utf8') as f:
        content = f.readlines()
        
        with codecs.open(scs_path+file,'wb','utf8') as g:
        
            for line in content:
                temp = []
                words = pseg.cut(line.strip())

                for word, flag in words:
                    temp.append(word+'('+flag+')')

                g.write(' '.join(temp)+'\r\n')
print ('END')


# In[1]:

#Dfa+N合併
import codecs
import time
import os

desktop_path = "C:\\Users\\user\\Desktop\\"
out_path = "C:\\Users\\user\\Desktop\\jieba_SCS\\"
dfa_path = desktop_path+"Dfa改\\Dfa\\"

scs_list = []

for file in os.listdir(dfa_path):
    scs_list.append(file)

for file in scs_list:
    with codecs.open(dfa_path+file,'rb','utf8') as f:
        content = f.readlines()
        
        with codecs.open(out_path+file,'wb','utf8') as g:
        
            for line in content:
                line = line.split()
                
                g.write(line[0].split('(')[0]+line[1].split('(')[0]+'\r\n')

print ('END')    


# In[5]:

import codecs
import time
import os

desktop_path = "C:\\Users\\user\\Desktop\\"
com_path = desktop_path+"jieba_SCS\\"
out_path = "C:\\Users\\user\\Desktop\\jieba_SCS_out\\"
all_path = desktop_path+"all\\"

scs_list = [] #平衡語料庫句子
dfa_list = [] #Dfa+n

for file in os.listdir(all_path):
    scs_list.append(file)
    
for file in os.listdir(com_path):
    dfa_list.append(file)

#Dfa底下的Dfa+n SCS遞迴找出Dfa+n所在位址
for dfa in dfa_list:
    
    find = []
    
    with codecs.open(com_path+dfa,'rb','utf8') as f:
        content = f.readlines()
        
        for line in content:
            find.append(line.strip())
    
    with codecs.open(out_path+dfa,'wb','utf8') as g:
        for search in find:
            g.write('#'+search+'\r\n')
            for scs in scs_list:
                with codecs.open(all_path+scs,'rb','utf8') as f:
                    content = f.readlines()
                    
                    for line in content:
                        line = line.strip()
                        if search in line:
                            g.write(line+'\r\n')
            g.write('\r\n')
        
print ("END")


# In[1]:

#找出SCS內Dfa+N的句子
import codecs
import time
import os
import xml.etree.ElementTree as ET

desktop_path = "C:\\Users\\user\\Desktop\\"
dfa_path = desktop_path+"Dfa改\\Dfa\\"
scs_path = 'C:\\Users\\user\\Desktop\\課業相關\\碩士班\\SNA\\meeting\\source\\SCS_4.0\\CKIP\\'
out_path = "C:\\Users\\user\\Desktop\\jieba_SCS\\"
out2_path = "C:\\Users\\user\\Desktop\\jieba_SCS_out\\"

scs_list = [] #平衡語料庫句子
dfa_list = [] #Dfa+n

for file in os.listdir(scs_path):
    scs_list.append(file)
    
for file in os.listdir(dfa_path):
    dfa_list.append(file)

#Dfa底下的Dfa+n SCS遞迴找出Dfa+n所在位址
for dfa in dfa_list:
    
    find = []
    
    with codecs.open(dfa_path+dfa,'rb','utf8') as f:
        content = f.readlines()
        
        for line in content:
            line = line.split()
            find.append(line[0]+line[1])
    
    with codecs.open(out_path+dfa,'wb','utf8') as g:
        with codecs.open(out2_path+dfa,'wb','utf8') as g2:
            for search in find:
                g.write('#'+search+'\r\n')
                g2.write('#'+search+'\r\n')
                for scs in scs_list:

                    tree = ET.parse(scs_path+scs)
                    root = tree.getroot()

                    for sentence in root.iter('sentence'):
                        try:
                            temp = ''.join(sentence.text.split())
                            if search in temp:
                                g.write(sentence.text+'\r\n')
                                
                                for i in sentence.text.split():
                                    g2.write(i.split('(')[0])
                                g2.write('\r\n')
                        except:
                            pass
                g.write('\r\n')
                g2.write('\r\n')
            
    print (dfa)
        
print ("END")


# In[4]:

import codecs
import os
import time
import jieba
import jieba.posseg as pseg

jieba.set_dictionary('dict.txt.big')

desktop_path = "C:\\Users\\user\\Desktop\\"
scs_path = "C:\\Users\\user\\Desktop\\jieba_SCS_out\\"
out_path = "C:\\Users\\user\\Desktop\\jieba_SCS_cut\\"

scs_list = [] 

for file in os.listdir(scs_path):
    scs_list.append(file)
    
for file in scs_list:
    with codecs.open(scs_path+file,'rb','utf8') as f:
        content = f.readlines()
        
        with codecs.open(out_path+file.split('.')[0]+'.csv','wb','utf8') as g:
        
            for line in content:
                line = line.strip()
                if line == '':
                    g.write('\r\n')
                elif line[0] == '#':
                    g.write(line[1:]+'\r\n')
                else:
                    words = pseg.cut(line)
                    for word, flag in words:
                        g.write(word+'('+flag+'),')
                    g.write('\r\n')
                    

print ('END')


# In[59]:

import os
import codecs
import time

jieba_path = "C:\\Users\\user\\Desktop\\SCS_cut\\SCS_jieba\\"
ckip_path = "C:\\Users\\user\\Desktop\\SCS_cut\\SCS_CKIP\\"
out_path = "C:\\Users\\user\\Desktop\\SCS_cut\\對齊\\"
desktop_path = "C:\\Users\\user\\Desktop\\"

jieba_list = []

for file in os.listdir(jieba_path):
    jieba_list.append(file)
    
ckip_list = []

for file in os.listdir(ckip_path):
    ckip_list.append(file)

    
with codecs.open(desktop_path+'all.csv','wb','utf8') as g:

    for file in jieba_list:

        head = file.split('.')[0][0]

        with codecs.open(jieba_path+file,'rb','utf8') as f:
            content = f.readlines()

            for line in content:
                '''if line[0] == '#':
                    g.write(line)
                    continue'''
                    
                line = line.strip().split(',')
                
                '''if len(line) == 0:
                    g.write('\r\n')
                else:'''
                check = False
                temp = []
                
                if len(line) == 1 and line[0] != '':
                    if (line[0].split(')')[0]).split('(')[1] == 'Dfa':
                        continue
                elif line[0] == '':
                    continue
                
                for i in line:
                    if i == '' and not check:
                        temp = line
                        break
                    if check or i[0] == head:
                        check = True
                        temp.append(i)

                g.write(','.join(temp)+'\r\n')
                '''print (','.join(temp)+'\r\n')
                time.sleep(0.5)'''

print ('END')

