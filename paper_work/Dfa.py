
# coding: utf-8

# In[16]:

import codecs
import os
import time
import xml.etree.ElementTree as ET

scs_path = 'C:\\Users\\user\\Desktop\\課業相關\\碩士班\\SNA\\meeting\\source\\SCS_4.0\\'
desktop_path = "C:\\Users\\user\\Desktop\\"

scs_list = []

for file in os.listdir(scs_path):
    scs_list.append(file)
    
Dfa = {}
Dfa_len = {} 

all_different = []
    
for file in scs_list:
    
    tree = ET.parse(scs_path+file)
    root = tree.getroot()
    
    check = False
    head = ''
    
    for sentence in root.iter('sentence'):
        try:
            temp = sentence.text.split()
            
            for i in range(len(temp)-1):
                if temp[i].split('(')[1][0:-1] == 'Dfa':
                    if temp[i+1].split('(')[1][0] == 'N':
                        if temp[i+1].split('(')[1][0:-1] not in all_different:
                            all_different.append(temp[i+1].split('(')[1][0:-1])
                            
                        if temp[i] not in Dfa:
                            Dfa[temp[i]] = {temp[i+1]:1}
                            Dfa_len[temp[i]] = 1
                        else:
                            if temp[i+1] not in Dfa[temp[i]]:
                                Dfa[temp[i]][temp[i+1]] = 1
                            else:
                                Dfa[temp[i]][temp[i+1]] += 1
                            Dfa_len[temp[i]] += 1
            
        except:
            pass
        
Dfa_len = sorted(Dfa_len.items(), key=lambda d:d[1], reverse = True)

'''with codecs.open(desktop_path+'Dfa_len.txt','wb','utf8') as g:
    g.write('#後面接有N開頭詞彙的Dfa排序\r\n')
    for i in Dfa_len:
        g.write(i[0]+' '+str(i[1])+'\r\n')

for word in Dfa:
    with codecs.open(desktop_path+'Dfa\\'+word+'.txt','wb','utf8') as g:
        order = sorted(Dfa[word].items(), key=lambda d:d[1], reverse = True)
        for i in order:
            g.write(word+' '+i[0]+' '+str(i[1])+'\r\n')'''


'''for word in Dfa:
    with codecs.open(desktop_path+'Dfa\\'+word.split('(')[0]+'.csv','wb','utf8') as g:
        order = sorted(Dfa[word].items(), key=lambda d:d[1], reverse = True)
        different = []
        
        for i in order:
            if i[0].split('(')[1][0:-1] not in different:
                different.append(i[0].split('(')[1][0:-1])
        different.sort()
        for i in different:
            g.write(','+i)
        g.write(',,Count\r\n')
        
        for i in order:
            g.write(word)
            for j in range(len(different)):
                if i[0].split('(')[1][0:-1] == different[j]:
                    g.write(','+i[0].split('(')[0])
                else:
                    g.write(',')
            g.write(',,'+str(i[1])+'\r\n')'''

all_different.sort()

with codecs.open(desktop_path+'all_Dfa.csv','wb','utf8') as g:
    
    for i in all_different:
        g.write(','+i)
    g.write(',,Count\r\n')
    
    for k in Dfa_len:
        order = sorted(Dfa[k[0]].items(), key=lambda d:d[1], reverse = True)
        
        for i in order:
            g.write(k[0])
            for j in range(len(all_different)):
                if i[0].split('(')[1][0:-1] == all_different[j]:
                    g.write(','+i[0].split('(')[0])
                else:
                    g.write(',')
            g.write(',,'+str(i[1])+'\r\n')
    
print ('END')


# In[52]:

import codecs
import os
import time
import xml.etree.ElementTree as ET

scs_path = 'C:\\Users\\user\\Desktop\\課業相關\\碩士班\\SNA\\meeting\\source\\SCS_4.0\\'
desktop_path = "C:\\Users\\user\\Desktop\\"

scs_list = []

for file in os.listdir(scs_path):
    scs_list.append(file)
    
first = ['很','極','太','最','更','比較','稍','略','多','多麼']
second = ['很','忒','太','最','更','比較','較','真','好','挺','怪','非常','十分','稍微','特別','尤其','不大']
third = ['很', '極', '太', '最', '更', '比較', '稍', '略', '多', '挺', '怪', '非常', '十分', '稍微', '稍稍', '更加',          '相當', '格外', '極其', '頂', '愈', '多麼', '越加', '越發', '略為']
forth = ['忒', '太', '最', '更', '比較', '稍', '略', '多', '好', '挺', '較', '非常', '十分', '稍微', '稍稍', '甚為', '不大',          '格外', '極其', '頂', '愈', '多麼', '越加', '越發', '相當', '愈加', '過分', '特別', '特', '愈發', '過於', '更為', '倍加',          '大', '大為', '分外', '夠', '好不', '何等', '何其', '幾乎', '極度', '較為', '尤為', '老', '略略', '略微', '頗', '頗為',          '深為', '甚', '尤其', '異常', '有一點', '微微', '萬分', '最為', '更加', '稍許', '差不多', '差一點', '多少', '過', '極大',          '極力', '極為', '絕', '蠻', '尤', '覺', '微']
fifth = ['很', '極', '太', '最', '更', '比較', '稍', '略', '多', '好', '挺', '怪', '非常', '十分', '稍微', '稍稍', '甚為', '不大',         '格外', '極其', '頂', '愈', '多麼', '越', '越發', '相當', '愈加', '過分', '特別', '特', '愈發', '過於', '更為', '倍加',         '大', '大為', '分外', '夠', '好不', '何等', '何其', '幾乎', '極度', '較為', '尤為', '老', '略略', '略微', '頗', '頗為',          '深為', '甚', '尤其', '異常', '有點兒', '微微', '萬分', '最為', '更加', '稍許', '較', '滿', '還', '幾', '至', '透', '慌',         '不勝', '無比', '極端', '絕對', '萬分', '至為', '不太', '不很', '不甚', '略為', '稍為', '些微', '有些', '大大', '較比',         '更甚', '越如', '愈益', '愈為', '絕頂', '絕倫', '透頂']

find = fifth

Dfa = {}
Dfa_len = {} 
    
for file in scs_list:
    
    tree = ET.parse(scs_path+file)
    root = tree.getroot()
    
    for sentence in root.iter('sentence'):
        try:
            temp = sentence.text.split()
            
            for i in range(len(temp)-1):
                if temp[i].split('(')[0] in find:
                    if temp[i+1].split('(')[1][0] == 'N':
                            
                        if temp[i] not in Dfa:
                            Dfa[temp[i]] = {temp[i+1]:1}
                            Dfa_len[temp[i]] = 1
                        else:
                            if temp[i+1] not in Dfa[temp[i]]:
                                Dfa[temp[i]][temp[i+1]] = 1
                            else:
                                Dfa[temp[i]][temp[i+1]] += 1
                            Dfa_len[temp[i]] += 1
                
        except:
            pass
        
#Dfa_len = sorted(Dfa_len.items(), key=lambda d:d[1], reverse = True)

with codecs.open(desktop_path+'fifth.csv','wb','utf8') as g:
    
    g.write(',Dfa,非Dfa\r\n')
    
    for i in find:

        isDfa = 0
        notDfa = 0
        notDfa_list = []

        for j in Dfa_len:
            if j.split('(')[0] == i:
                if j.split('(')[1][0:-1] == 'Dfa':
                    isDfa += Dfa_len[j]
                else:
                    notDfa += Dfa_len[j]
                    notDfa_list.append((j,Dfa_len[j]))
                    
        g.write(i+','+str(isDfa)+','+str(notDfa)+',,')
        for j in notDfa_list:
            g.write(j[0]+','+str(j[1])+',')
        g.write('\r\n')
    
print ('END')


# In[37]:

import xlrd
book = xlrd.open_workbook("C:\\Users\\user\\Desktop\\常見程度副詞.xlsx")
#print("The number of worksheets is {0}".format(book.nsheets))
#print("Worksheet name(s): {0}".format(book.sheet_names()))
sh = book.sheet_by_index(0)
#print("{0} {1} {2}".format(sh.name, sh.nrows, sh.ncols))
#print("Cell D30 is {0}".format(sh.cell_value(rowx=29, colx=3)))
for rx in range(sh.nrows):
    word = []
    for i in sh.row(rx):
        if i.value != '':
            word.append(i.value)
    print (word)

