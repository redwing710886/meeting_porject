
# coding: utf-8

# In[14]:

#否定
#程度副詞
import os
import codecs
import time

path = "C:\\Users\\user\\Desktop\\課業相關\\碩士班\\SNA\\meeting\\source\\FreeChina\\"
out_path = 'C:\\Users\\user\\Desktop\\否定\\'

file_list = []
find = ['不','沒','沒有','無','非']

for file in os.listdir(path):
    file_list.append(file)
    
author = {}

for file in file_list:
    with codecs.open(path+file,'rb','utf8') as f:
        content = f.readlines()
        
        name = ''
        
        for line in content:
            line = line.split()
            
            if line[0] == '#':
                if line[-1].split('(')[1][0:-1] == 'AUTHOR':
                    name = line[-1].split('(')[0]
                    
                    if name not in author:
                        author[name] = {}
            elif name != '':
                for i in range(len(line)-1):
                    if line[i].split('(')[0] in find:
                        temp = line[i].split('(')[0]+line[i+1].split('(')[0]
                        try:
                            if temp not in author[name]:
                                author[name][temp] = 1
                            else:
                                author[name][temp] += 1
                        except:
                            print (name)
                            print (line)
                            print (temp)
                            
for i in author:
    temp = author[i]
    temp = sorted(temp.items(), key=lambda d:d[1], reverse = True)
    print (i)
    with codecs.open(out_path+i+'.txt','wb','utf8') as g:
        for j in temp:
            g.write(j[0]+' '+str(j[1])+'\r\n')

print ('END')


# In[2]:

#比較
#程度副詞
import xml.etree.ElementTree as ET
import os
import codecs
import time

path = "C:\\Users\\user\\Desktop\\課業相關\\碩士班\\SNA\\meeting\\source\\diary\\"
out_path = 'C:\\Users\\user\\Desktop\\程度副詞\\'

file_list = []
find = ['很','非常']
#,'比較','特別','最','太','更','挺','多','越','有點','特','稍微','尤其','幾乎','相當','大','好','差不多','極']

for file in os.listdir(path):
    file_list.append(file)

for file in file_list:
    
    tree = ET.parse(path+file)
    root = tree.getroot()
    
    for sentence in root.iter('sentence'):
        temp = sentence.text.split()
        
        for i in range(len(temp)-1):
            if temp[i].split('(')[0] in find:
                if temp[i+1].split('(')[1][0] == 'N':
                    print (file,temp[i],temp[i+1])
                    time.sleep(0.5)
        
    
print ('END')

