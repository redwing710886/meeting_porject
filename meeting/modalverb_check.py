
# coding: utf-8

# In[17]:

#XML內容抓取
# 235/1396133
import codecs
import os
import xml.etree.ElementTree as ET
import time

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
        num = num + 1
        try:
            temp = sentence.text.split()

            check1 = ''
            check2 = ''        
            more_check = False
            
            for i in temp:
                word = i.split('(')
                word[1] = '('+word[1]
                if word[0] in modalverb:
                    if check1 == '':
                        check1 = word[0]
                    elif check2 == '':
                        check2 = word[0]
                    else:
                        much = much + 1
                        more_check = True
            
            if check1 != '' and check2 != '' and not more_check:
                #print (temp)
                #time.sleep(0.3)
                if (check1,check2) in two_verb:
                    two_verb[(check1,check2)] = two_verb[(check1,check2)] + 1
                else:
                    two_verb[(check1,check2)] = 1
     
        except:
            error_num = error_num + 1

pop = []

for i in two_verb:
    if (i[1],i[0]) in two_verb and i not in pop and i[0] != i[1]:
        two_verb[i] = two_verb[i] + two_verb[(i[1],i[0])]
        pop.append((i[1],i[0]))

print (len(two_verb))
print (len(pop))
for j in pop:
    two_verb.pop(j)

two_verb = sorted(two_verb.items(), key=lambda d:d[1], reverse = True)
    
print (len(two_verb))
for i in two_verb:
    print (i[0],i[1])

print (error_num)
print (much)

