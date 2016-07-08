
# coding: utf-8

# In[1]:

#將各文本依出現次數排序合併後，取中位數
import codecs
import statistics

path = 'C:\\Users\\user\\Desktop\\課業相關\\碩士班\\SNA\\meeting\\情態動詞\\兩兩情態動詞整理\\output and conbine\\'
out_path = 'C:\\Users\\user\\Desktop\\'

file = {}
num = {}

with codecs.open(path+'new_conbine.txt','r','utf8') as f:
    content = f.readlines()
    
    check = ''
    
    for line in content:
        if line[0] == '#':
            file[line[1:].strip()] = []
            num[line[1:].strip()] = 0
            check = line[1:].strip()
        elif line[0] == '@':
            num[check] = int(line[1:])
        elif len(line.strip()) == 0:
            continue
        else:
            l = line.split()
            wc = l[0].split('_')
            #file[check].append([l[0][2:-2],l[1][1:-2],l[2]])
            if wc[0][0] != '該' and wc[1][0] != '會':
                file[check].append([wc[0],wc[1],l[1]])
        '''else:
            num[check] = int(line)'''
            
#with codecs.open(path+'a.csv','w','utf8') as f: 
#for i in file:
    #print (i)
    #for j in file[i]:
        #print (j[0],j[1],round(int(j[2])*1000000/num[i],2))
        #pass
        #f.write(j[0]+'_'+j[1]+','+str(round(int(j[2])*1000000/num[i],2))+'\r\n')

k = {} #數值
o = {} #名次數值

for i in file:
    #if i != 'diary':
    count = 1
    s = 1
    temp = 0
    for j in file[i]:
        if temp == round(int(j[2])*1000000/num[i],2):
            s = s - 1
        else:
            s = count
        if j[0]+'_'+j[1] in k:
            #k[j[0]+'_'+j[1]].append([i,round(int(j[2])*1000000/num[i],2)])
            k[j[0]+'_'+j[1]].append([i,s,round(int(j[2])*1000000/num[i],2)])
            o[j[0]+'_'+j[1]].append(s)
        else:
            #k[j[0]+'_'+j[1]] = [[i,round(int(j[2])*1000000/num[i],2)]]
            k[j[0]+'_'+j[1]] = [[i,s,round(int(j[2])*1000000/num[i],2)]]
            o[j[0]+'_'+j[1]] = [s]
        count = count + 1
        s = s + 1
        temp = round(int(j[2])*1000000/num[i],2)

#中位數
for i in o:
    o[i] = statistics.median(o[i])
                
o = sorted(o.items(), key=lambda d:d[1], reverse = False)

with codecs.open(out_path+'conbine_final.csv','w','utf8') as g:
    g.write('兩兩情態動詞'+','+'分數'+','+'FreeChina'+','+'SCS'+','+'diary'+','+'228'+'\r\n')
    lll = ['FreeChina','SCS','diary','228']
    for i in o:
        if len(k[i[0]]) == 0:
            continue
        print (i[0],i[1],k[i[0]])
        tt = i[0]+','+str(round(i[1],2))
        
        temp_dic = {}
        
        for j in k[i[0]]:
            #tt = tt + ',' + j[0] + '_' + str(j[1]) + '_' + str(j[2])
            temp_dic[j[0]] = j[1]
            
        for c in lll:
            if c not in temp_dic:
                tt = tt + ',' + '0'
            else:
                tt = tt + ',' + str(temp_dic[c])
        g.write(tt+'\r\n')
print ('END')

