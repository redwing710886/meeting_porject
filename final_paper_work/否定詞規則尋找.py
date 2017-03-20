
# coding: utf-8

# In[6]:

#2017/3/17 找尋否定詞後面規則
#2017/3/19 規則改寫，完成搜尋功能
#2017/3/20 修改一開始尋找，加入輸出綜合頻率排序，增加搜尋功能選項
#否/無/非/不/沒+任意詞 (主要是否定概念+後續詞)
#先找出否定詞+後續N個字
#資料庫：平衡語料庫
#找尋範圍：n=1~5、詞彙與詞性、否定詞有無包含
import codecs
import os
from collections import defaultdict
import time
from IPython.display import clear_output

SC_path = "D:\\課業相關\\論文資料\\SCS2\\"
out_path = "C:\\Users\\user\\Desktop\\否定詞\\未包含\\"

condicate = ['未','無','非','不','沒']


# In[7]:

#尋找符合需求的詞性詞彙組合
#以建立就不用跑
def find_answer(num):
    word_fre = defaultdict(int) #詞彙頻率
    pos_fre = defaultdict(int) #詞性頻率
    count = 0
    for file in os.listdir(SC_path):
        count += 1
        if count % 1000 == 0:
            print (num,count)
        with codecs.open(SC_path+file,'rb','utf8') as f:
            header = f.readline()
            content = f.readline().strip().split()

            for i in range(len(content)-num):
                for w in condicate:
                    #if w in content[i].split('(')[0]: #否定詞有包含
                    if w == content[i].split('(')[0]: #否定詞無包含
                        temp_word = []
                        temp_pos = []
                        check = False #判斷組合中是否有雜質
                        for t in range(num+1):
                            if 'CATEGORY' in content[i+t].split('(')[1]: #組合中移除標點符號
                                check = True
                                break
                            temp_word.append(content[i+t])
                            temp_pos.append('('+content[i+t].split('(')[1].split(')')[0]+')')
                        if not check:
                            word_fre[''.join(temp_word)+','+''.join(temp_pos)] += 1
                            pos_fre[''.join(temp_pos)] += 1
    return word_fre,pos_fre
        

def print_answer(num,word_fre,pos_fre):
    answer_word_fre = sorted(word_fre.items(), key=lambda d:d[1], reverse = True)
    answer_pos_fre = sorted(pos_fre.items(), key=lambda d:d[1], reverse = True)
    
    with codecs.open(out_path+'n_'+str(num)+'_word.csv','wb','utf8') as g:
        for i in answer_word_fre:
            g.write(i[0]+','+str(i[1])+'\r\n')
    with codecs.open(out_path+'n_'+str(num)+'_pos.csv','wb','utf8') as g:
        for i in answer_pos_fre:
            g.write(i[0]+','+str(i[1])+'\r\n')


def main():
    print (out_path)
    all_word_fre = defaultdict(int)
    all_pos_fre = defaultdict(int)
    for num in range(1,6):
        word_fre,pos_fre = find_answer(num)
        print_answer(num,word_fre,pos_fre)
        for i in word_fre:
            all_word_fre[i] += word_fre[i]
        for i in pos_fre:
            all_pos_fre[i] += pos_fre[i]
        print (str(num)+' END')
        clear_output()
    print_answer('all',all_word_fre,all_pos_fre)    
    print ('END')
    
main()


# In[2]:

#從以提取資料建成資料庫(舊版)
input_path = out_path

all_word_fre = defaultdict(int)
all_pos_fre = defaultdict(int)
pos_word_set = defaultdict(dict)

def pos_set(pos):
    temp_count = len(pos.split(')'))-1 #計算為多少個詞性
    temp_set = []
    for i in range(1,temp_count):
        temp_set.append(')'.join(pos.split(')')[:i+1])+')')
    return temp_set

for file in os.listdir(input_path):
    with codecs.open(input_path+file,'rb','utf8') as f:
        content = f.readlines()
        for line in content:
            if line.strip() == '':
                continue
            if 'pos' in file:
                line = line.strip().split(',')
                all_pos_fre[line[0]] += int(line[1])
            elif 'word' in file:
                line = line.strip().split(',')
                all_word_fre[line[0]] += int(line[2])
                
                temp_set = pos_set(line[1])
                for i in temp_set:
                    if line[0] not in pos_word_set[i]:
                        pos_word_set[i][line[0]] = int(line[2])
                    else:
                        pos_word_set[i][line[0]] += int(line[2])

answer_pos_fre = sorted(all_pos_fre.items(), key=lambda d:d[1], reverse = True)
answer_word_fre = sorted(all_word_fre.items(), key=lambda d:d[1], reverse = True)
#print(answer_pos_fre[:10])
#print(answer_word_fre[:10])
print ('END')


# In[13]:

#從以提取資料建成資料庫(新版)
input_path = out_path

answer_pos_fre = [] #詞性頻率
answer_word_fre = [] #詞彙頻率
pos_word_set = defaultdict(dict) #用詞性找包含該詞性的詞彙頻率
word_word_set = defaultdict(dict) #用詞彙找包含該詞彙的詞彙頻率

def pos_set(pos): #找出詞性所有組合
    temp_count = len(pos.split(')'))-1 #計算為多少個詞性
    temp_set = []
    for i in range(1,temp_count):
        temp_set.append(')'.join(pos.split(')')[:i+1])+')')
    return temp_set

with codecs.open(input_path+'n_all_word.csv','rb','utf8') as f:
    content = f.readlines()
    for line in content:
        line = line.strip()
        if line != '':
            line = line.split(',')
            answer_word_fre.append((line[0],int(line[2])))
            
            temp_set = pos_set(line[1])
            for i in temp_set:
                if line[0] not in pos_word_set[i]:
                    pos_word_set[i][line[0]] = int(line[2])
                else:
                    pos_word_set[i][line[0]] += int(line[2])
                    
            temp_set = pos_set(line[0])
            for i in temp_set:
                if line[0] not in word_word_set[i]:
                    word_word_set[i][line[0]] = int(line[2])
                else:
                    word_word_set[i][line[0]] += int(line[2])
            
with codecs.open(input_path+'n_all_pos.csv','rb','utf8') as f:
    content = f.readlines()
    for line in content:
        line = line.strip()
        if line != '':
            line = line.split(',')
            answer_pos_fre.append((line[0],int(line[1])))

print ('END')


# In[22]:

#查詢功能，包含：
#1.頻率前20個的詞性
#2.頻率前20個的詞彙
#3.頻率前20個且長度大於2的詞性
#4.頻率前20個且長度大於2的詞彙
#5.依詞性或詞彙做搜尋，可在之後加上數字表示最少幾位

while(1):
    fd = input()
    find = ''
    find2 = 0
    if len(fd.split()) > 1:
        find = fd.split()[0]  
        find2 = int(fd.split()[1])
    else:
        find = fd
    
    clear_output()
    print (out_path)
    print ('find:',find,find2)
    if find == '1': #頻率前20個的詞性
        for i in range(20):
            print (i+1,answer_pos_fre[i][0],answer_pos_fre[i][1])
    elif find == '2': #頻率前20個的詞彙
        for i in range(20):
            print (i+1,answer_word_fre[i][0],answer_word_fre[i][1])
    elif find == '3': #頻率前20個且長度大於2的詞性
        count = 0
        for i in answer_pos_fre:
            if len(i[0].split(')')) > 3:
                print (count+1,i[0],i[1])
                count += 1
            if count == 20:
                break
    elif find == '4': #頻率前20個且長度大於2的詞彙
        count = 0
        for i in answer_word_fre:
            if len(i[0].split(')')) > 3:
                print (count+1,i[0],i[1])
                count += 1
            if count == 20:
                break
    else: #依詞性或詞彙做搜尋，可在之後加上數字表示最少幾位
        if find in pos_word_set:
            temp = sorted(pos_word_set[find].items(), key=lambda d:d[1], reverse = True)
            if find2 == 0:
                for i in range(20):
                    print (i+1,temp[i][0],temp[i][1])
            else:
                count = 0
                for i in temp:
                    if len(i[0].split(')')) > find2:
                        print (count+1,i[0],i[1])
                        count += 1
                    if count == 20:
                        break
        elif find in word_word_set:
            temp = sorted(word_word_set[find].items(), key=lambda d:d[1], reverse = True)
            if find2 == 0:
                for i in range(20):
                    print (i+1,temp[i][0],temp[i][1])
            else:
                count = 0
                for i in temp:
                    if len(i[0].split(')')) > find2:
                        print (count+1,i[0],i[1])
                        count += 1
                    if count == 20:
                        break
        elif find == 'e': #離開
            break
print ('END')


# In[27]:

#特定組合尋找並計算結果
import statistics

find = input().split(')')
find = [x+')' for x in find][:-1]

file_find_fre = defaultdict(int)
count = 0

check = False  #判斷是詞性還是詞彙組合
if find[0].split('(')[0] == '':
    check = True

for file in os.listdir(SC_path):
    count += 1
    if count % 1000 == 0:
        print (count)
    with codecs.open(SC_path+file,'rb','utf8') as f:
        header = f.readline()
        content = f.readline().strip().split()
        
        file_find_fre[file] = 0
        
        for i in range(len(content)-len(find)+1):
            if not check and ''.join(content[i:i+len(find)]) == ''.join(find):
                file_find_fre[file] += 1
            elif check and content[i].split('(')[0] in condicate:
                if ''.join(['('+x.split('(')[1].split(')')[0]+')' for x in content[i:i+len(find)]]) == ''.join(find):
                    file_find_fre[file] += 1

clear_output()
print (''.join(find))

file_find_fre = sorted(file_find_fre.items(), key=lambda d:d[1], reverse = True)     

number = []
for i in file_find_fre:
    number.append(int(i[1]))

print ('平均數：',round(statistics.mean(number),2))
#print ('中位數：',statistics.median(number))
#print ('眾數：',statistics.mode(number))
print ('標準差：',round(statistics.stdev(number),2))
print ('非0：',len([x for x in number if x > 0]),str(round(len([x for x in number if x > 0])*100/len(number),2))+'%')
    
for i in range(20):
    print (i+1,file_find_fre[i][0],file_find_fre[i][1])

print ('END')

