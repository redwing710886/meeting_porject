
# coding: utf-8

# In[1]:

class color():
    
    RED = '\033[31m'
    GREEN = '\033[32m'
    YELLOW = '\033[33m'
    BLUE = '\033[34m'
    MAGENTA = '\033[35m'
    CYAN = '\033[36m'
    RED_WHITE = '\033[41m'
    GREEN_RED = '\033[31;42m'
    YELLOW_RED = '\033[33;43m'
    BLUE_WHITE = '\033[44m'
    MAGENTA_BLUE = '\033[35;45m'
    CYAN_RED = '\033[31;46m'
    END = '\033[0m'


# In[5]:

import pymysql
import codecs
import os
import time

modal = [] #情態類別 
modal_color = {} #情態類別顏色
word_modal = {} #情態詞:類別
exception = {} #情態詞:複數類別

def color_set(model):
    modal_color[modal[0]] = color.RED
    modal_color[modal[1]] = color.GREEN
    modal_color[modal[2]] = color.YELLOW
    modal_color[modal[3]] = color.BLUE
    modal_color[modal[4]] = color.MAGENTA
    modal_color[modal[5]] = color.CYAN
    modal_color[modal[6]] = color.RED_WHITE
    modal_color[modal[7]] = color.GREEN_RED
    modal_color[modal[8]] = color.YELLOW_RED
    modal_color[modal[9]] = color.BLUE_WHITE
    modal_color[modal[10]] = color.MAGENTA_BLUE
    modal_color[modal[11]] = color.CYAN_RED
    
    for i in modal:
        print (modal_color[i]+i+color.END)
    
    
def sql_search(sql_command):

    connection = pymysql.connect(host="127.0.0.1", user="redwing", passwd="", db="word",charset='utf8')

    result = []

    try:
        with connection.cursor() as cursor:
            cursor.execute(sql_command)

            for i in cursor:
                result.append(i) 

            return result
    finally:
        connection.close()

def make_modal():

    for i in sql_search("SELECT distinct `class` FROM `word`"):
        modal.append(i[0])
        
    color_set(modal)

    for i in sql_search("select * from `word`"):
        if i[2] in exception: #情態詞在例外內
            exception[i[2]].append(i[1])
        elif i[2] not in word_modal: #情態詞不在索引內
            word_modal[i[2]] = i[1]
        elif i[1] != word_modal[i[2]]: #情態詞在索引內重複且不相等
            exception[i[2]] = [word_modal[i[2]],i[1]]
            word_modal.pop(i[2])
            
def get_article(file_address):
    
    path = 'C:\\Users\\user\\Desktop\\article\\'
    result = {}
    
    with codecs.open(path+file_address,'rb','utf8') as f:
        content = f.readlines()
        
        for line in content:
            if line[0] == '#':
                print (line.strip())
                continue
            try:
                line = line.split()
                
                for word in line:
                    word = word.split('(')[0]
                    if word in exception:
                        print ('['+word+'(例外)]',end='')
                        if '例外'  not in result:
                            result['例外'] = [word]
                        else:
                            result['例外'].append(word)
                    elif word in word_modal:
                        print (modal_color[word_modal[word]]+'['+word+']'+color.END,end='')
                        if word_modal[word] not in result:
                            result[word_modal[word]] = [word]
                        else:
                            result[word_modal[word]].append(word)
                    else:
                        print (word,end='')
            except:
                print (line)
    return result

make_modal()


# In[57]:

#圓餅圖
import matplotlib
import matplotlib.pyplot as plt 
myfont = matplotlib.font_manager.FontProperties(fname='c:\\windows\\fonts\\msyh.ttc', size=14)

def pie_Chart(label,size):
    
    labels = label
    sizes = []
    explode = []
    
    sum_size = 0
    for i in size:
        sum_size += i
        explode.append(0)
    for i in size:
        sizes.append(round((i/sum_size)*100,2))
    
    explode[0] = 0.05
    explode = tuple(explode)
    #print (labels)
    #print (sizes)
    for i in range(len(labels)):
        print (labels[i]+':'+str(sizes[i])+'%',end = ' ')
    

    #调节图形大小，宽，高
    plt.figure(figsize=(6,9))
    #定义饼状图的标签，标签是列表
    #labels = ['第一部分','第二部分','第三部分']
    #每个标签占多大，会自动去算百分比
    #sizes = [30,40,30]
    #colors = ['red','yellowgreen','lightskyblue']
    colors = ['b','yellowgreen','r','c','m','y','w']
    #将某部分爆炸出来， 使用括号，将第一块分割出来，数值的大小是分割出来的与其他两块的间隙
    #explode = (0,0.05,0)

    patches,l_text,p_text = plt.pie(sizes,explode=explode,labels=labels,colors=colors,
                                    labeldistance = 1.1,autopct = '%3.1f%%',shadow = False,
                                    startangle = 90,pctdistance = 0.6)

    #labeldistance，文本的位置离远点有多远，1.1指1.1倍半径的位置
    #autopct，圆里面的文本格式，%3.1f%%表示小数有三位，整数有一位的浮点数
    #shadow，饼是否有阴影
    #startangle，起始角度，0，表示从0开始逆时针转，为第一块。一般选择从90度开始比较好看
    #pctdistance，百分比的text离圆心的距离
    #patches, l_texts, p_texts，为了得到饼图的返回值，p_texts饼图内部文本的，l_texts饼图外label的文本

    #改变文本的大小
    #方法是把每一个text遍历。调用set_size方法设置它的属性
    for t in l_text:
        t.set_size=(30)
        t.set_fontproperties(myfont)
    for t in p_text:
        t.set_size=(20)
        #t.set_fontproperties(myfont)
    # 设置x，y轴刻度一致，这样饼图才能是圆的
    plt.axis('equal')
    plt.legend(prop=myfont,loc=1)
    plt.show()


# In[58]:

find = 0
find = input()
while(find != 'x'):
    result = get_article(str(find).zfill(5)+'.txt')
    
    pie_label = []
    pie_size = []
    
    print ()
    for i in result:
        if i != '例外':
            print (i,len(result[i]),end=' ')
            pie_label.append(i)
            pie_size.append(len(result[i]))
            temp = []
            
            print ('[',end = ' ')
            for j in result[i]:
                if j not in temp:
                    temp.append(j)
                    print (j+':'+str(result[i].count(j)),end = ' ')
            print (']')
    if '例外' in result:
        print ('例外',len(result['例外']),end = ' ')
        pie_label.append('例外')
        pie_size.append(len(result['例外']))
        temp = []
        
        print ('[',end = ' ')
        for j in result['例外']:
            if j not in temp:
                temp.append(j)
                print (j+':'+str(result['例外'].count(j)),end = ' ')
        print (']')
        
    pie_Chart(pie_label,pie_size)
        
    find = input()

