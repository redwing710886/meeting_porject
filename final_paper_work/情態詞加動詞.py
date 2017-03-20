
# coding: utf-8

# In[12]:

#2017/3/19 尋找情態詞後動詞種類
#資料庫：平衡語料庫
import codecs
import os
from collections import defaultdict
import time

SC_path = "D:\\課業相關\\論文資料\\SCS2\\"
modal_path = "D:\\課業相關\\論文資料\\謝佳玲情態詞\\"
out_path = "C:\\Users\\user\\Desktop\\"

modal = []
no_modal = []
with codecs.open(modal_path+'word.txt','rb','utf8') as f:
    content = f.readlines()
    for i in content:
        if i.strip() != '':
            modal.append(i.strip())
with codecs.open(modal_path+'no.txt','rb','utf8') as f:
    content = f.readlines()
    for i in content:
        if i.strip() != '':
            no_modal.append(i.strip())
print (len(modal))
print (len(no_modal))


# In[13]:

#尋找符合規則的組合及頻率
modal_fre = defaultdict(int)

count = 0
for file in os.listdir(SC_path):
    
    count += 1
    if count % 1000 == 0:
        print (count)
    
    with codecs.open(SC_path+file,'rb','utf8') as f:
        header = f.readline()
        content = f.readline().strip().split()
        
        for i in range(len(content)-1):
            if content[i].split('(')[0] not in no_modal and content[i].split('(')[0] in modal             and 'CATEGORY' not in content[i+1].split('(')[1] and content[i+1].split('(')[1][0] == 'V':
                modal_fre[content[i]+content[i+1]] += 1
                
answer_modal_fre = sorted(modal_fre.items(), key=lambda d:d[1], reverse = True)

with codecs.open(out_path+'modal_fre2.csv','wb','utf8') as g:
    for i in answer_modal_fre:
        g.write(i[0]+','+str(i[1])+'\r\n')
print ('END')

