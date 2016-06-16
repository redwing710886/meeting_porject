
# coding: utf-8

# In[52]:

import csv
import codecs
import time
from ipywidgets import IntProgress
from IPython.display import display

movie = {}
actor = []
genre = []
        
with codecs.open('C:\\Users\\user\\Desktop\\all_movie.csv','rb','utf8') as f:
    content = csv.reader(f, delimiter=',', quotechar='|')
    for row in content:
        movie[row[0][1:-1]] = {"genre":[],"actor":[],"imdbRating":0,"tomatoMeter":0}
        
with codecs.open('C:\\Users\\user\\Desktop\\all_actor.csv','rb','utf8') as f:
    content = csv.reader(f, delimiter=',', quotechar='|')
    for row in content:
        actor.append(row[0][1:-1])
        
with codecs.open('C:\\Users\\user\\Desktop\\all_genre.csv','rb','utf8') as f:
    content = csv.reader(f, delimiter=',', quotechar='|')
    for row in content:
        genre.append(row[0][1:-1])

with codecs.open('C:\\Users\\user\\Desktop\\actor_without_job.csv','rb','utf8') as f:
    content = csv.reader(f, delimiter=',', quotechar='|')
    first = True
    genre_check = True
    for row in content:
        if first:
            first = False
            continue
        movieID = row[1][1:-1]
        if len(movie[movieID]["actor"]) == 0:
            genre_check = True
            movie[movieID]["actor"].append(row[0][1:-1])
            movie[movieID]["genre"].append(row[2][1:-1])
            movie[movieID]["imdbRating"] = row[3][1:-1]
            movie[movieID]["tomatoMeter"] = row[4][1:-1]
        elif genre_check and row[2][1:-1] not in movie[movieID]["genre"]:
            movie[movieID]["genre"].append(row[2][1:-1])
        elif row[0][1:-1] not in movie[movieID]["actor"]:
            movie[movieID]["actor"].append(row[0][1:-1])
            genre_check = False
            
p = IntProgress()
p.max = len(movie)
p.description = 'start'
display(p)
count = 0

with codecs.open('C:\\Users\\user\\Desktop\\title.csv','wb','utf8') as f:
    f.write(','.join(actor)+','+','.join(genre)+',imdbRating,tomatoMeter\r\n')
    for movieID in movie:
        line = ''
        for name in actor:
            if name in movie[movieID]["actor"]:
                line = line + '1,'
            else:
                line = line + '0,'
        for gen in genre:
            if gen in movie[movieID]["genre"]:
                line = line + '1,'
            else:
                line = line + '0,'
        line = line + movie[movieID]["imdbRating"] + ',' + movie[movieID]["tomatoMeter"] + '\r\n'
        f.write(line)
        
        count = count + 1
        p.value = count
        p.description = str(count)
        
p.description = 'end'


# In[1]:

import csv
import codecs
import time
from ipywidgets import IntProgress
from IPython.display import display

movie = {}
actor = []
genre = []
        
with codecs.open('C:\\Users\\user\\Desktop\\all_movie.csv','rb','utf8') as f:
    content = csv.reader(f, delimiter=',', quotechar='|')
    for row in content:
        movie[row[0][1:-1]] = {"genre":[],"actor":[],"imdbRating":0,"tomatoMeter":0}
        
with codecs.open('C:\\Users\\user\\Desktop\\all_actor.csv','rb','utf8') as f:
    content = csv.reader(f, delimiter=',', quotechar='|')
    for row in content:
        actor.append(row[0][1:-1])
        
with codecs.open('C:\\Users\\user\\Desktop\\all_genre.csv','rb','utf8') as f:
    content = csv.reader(f, delimiter=',', quotechar='|')
    for row in content:
        genre.append(row[0][1:-1])

with codecs.open('C:\\Users\\user\\Desktop\\actor_without_job.csv','rb','utf8') as f:
    content = csv.reader(f, delimiter=',', quotechar='|')
    first = True
    genre_check = True
    for row in content:
        if first:
            first = False
            continue
        movieID = row[1][1:-1]
        if len(movie[movieID]["actor"]) == 0:
            genre_check = True
            movie[movieID]["actor"].append(row[0][1:-1])
            movie[movieID]["genre"].append(row[2][1:-1])
            movie[movieID]["imdbRating"] = row[3][1:-1]
            movie[movieID]["tomatoMeter"] = row[4][1:-1]
        elif genre_check and row[2][1:-1] not in movie[movieID]["genre"]:
            movie[movieID]["genre"].append(row[2][1:-1])
        elif row[0][1:-1] not in movie[movieID]["actor"]:
            movie[movieID]["actor"].append(row[0][1:-1])
            genre_check = False
            
p = IntProgress()
p.max = len(movie)
p.description = 'start'
display(p)
count = 0
#53 3
'''long = 0
temp = []
for i in movie:
    if len(movie[i]["genre"]) > long:
        long = len(movie[i]["genre"])
        temp = movie[i]["genre"]
print (long,temp)'''

with codecs.open('C:\\Users\\user\\Desktop\\ass_title2.csv','wb','utf8') as f:
    temp = ''
    for i in range(53):
        temp = temp + 'actor' + str(i+1) + ','
    for i in range(3):
        temp = temp + 'genre' + str(i+1) + ','
    f.write(temp+'imdbRating,tomatoMeter\r\n')
    
    for movieID in movie:
        line = ''
        actor_count = 0
        
        for name in movie[movieID]["actor"]:
            line = line + name + ','
            actor_count += 1
            
        while actor_count < 53:
            line = line + '0,'
            actor_count += 1
            
        genre_count = 0
            
        for gen in movie[movieID]["genre"]:
            line = line + gen + ','
            genre_count += 1
            
        while genre_count < 3:
            line = line + '0,'
            genre_count += 1
            
        line = line + movie[movieID]["imdbRating"] + ',' + movie[movieID]["tomatoMeter"] + '\r\n'
        f.write(line)
        
        count = count + 1
        p.value = count
        p.description = str(count)
        
p.description = 'end'


# In[60]:

temp_list = {"actor1":['nm0003506', 'nm0737216', 'nm0000212', 'nm0413168', 'nm0000630', 'nm0005227', 'nm0005169', 
                       'nm0925966', 'nm0925717', 'nm0336960'],
             "actor2":["0","1"],
             "actor3":["0"],
             "actor4":["0"]}

act = ["actor1","actor2","actor3","actor4"]
line = ''

def loop(list_a,line_b):
    if len(list_a) == 0:
        print (line_b[1:])
    elif len(temp_list[list_a[0]]) > 1:
        for i in temp_list[list_a[0]]:
            loop(list_a[1:],line_b+','+i)
    else:
        return loop(list_a[1:],line_b+','+temp_list[list_a[0]][0])
    
loop(act,line)


# In[134]:

import csv
import codecs
import time
import random
from ipywidgets import IntProgress
from IPython.display import display

actor = []
actor_split = {} #分類
actor_find = {} #演員在哪類
actor_title = [] #演員標頭

movie = {}
genre = []
title = []

#屬性標投分類
with codecs.open('C:\\Users\\user\\Desktop\\all_actor.csv','rb','utf8') as f:
    content = csv.reader(f, delimiter=',', quotechar='|')
    for row in content:
        actor.append(row[0][1:-1])

actor = random.sample(actor,len(actor))
        
temp = []
count = 1
for i in actor:
    if len(temp) < 10:
        temp.append(i)
    elif count == 4260:
        temp.append(i)
        actor_split["actor"+str(count).zfill(4)] = temp
        actor_title.append("actor"+str(count).zfill(4))
    else:
        actor_split["actor"+str(count).zfill(4)] = temp
        actor_title.append("actor"+str(count).zfill(4))
        count += 1
        temp = [i]

for i in actor_split:
    for j in actor_split[i]:
        actor_find[j] = i

#電影資料匯入
with codecs.open('C:\\Users\\user\\Desktop\\all_movie.csv','rb','utf8') as f:
    content = csv.reader(f, delimiter=',', quotechar='|')
    for row in content:
        movie[row[0][1:-1]] = {"genre":[],"actor":[],"imdbRating":0,"tomatoMeter":0}

with codecs.open('C:\\Users\\user\\Desktop\\all_genre.csv','rb','utf8') as f:
    content = csv.reader(f, delimiter=',', quotechar='|')
    for row in content:
        genre.append(row[0][1:-1])
        
with codecs.open('C:\\Users\\user\\Desktop\\actor_without_job.csv','rb','utf8') as f:
    content = csv.reader(f, delimiter=',', quotechar='|')
    first = True
    genre_check = True
    for row in content:
        if first:
            first = False
            continue
        movieID = row[1][1:-1]
        if len(movie[movieID]["actor"]) == 0:
            genre_check = True
            movie[movieID]["actor"].append(row[0][1:-1])
            movie[movieID]["genre"].append(row[2][1:-1])
            movie[movieID]["imdbRating"] = row[3][1:-1]
            movie[movieID]["tomatoMeter"] = row[4][1:-1]
        elif genre_check and row[2][1:-1] not in movie[movieID]["genre"]:
            movie[movieID]["genre"].append(row[2][1:-1])
        elif row[0][1:-1] not in movie[movieID]["actor"]:
            movie[movieID]["actor"].append(row[0][1:-1])
            genre_check = False
            
for i in actor_title:
    title.append(i)

for i in genre:
    title.append(i)
title.append("imdbRating")
title.append("tomatoMeter")

p = IntProgress()
p.max = len(movie)
p.description = 'start'
display(p)
bar_count = 0

with codecs.open('C:\\Users\\user\\Desktop\\ass_title3.csv','wb','utf8') as f:
    
    tt_line = ','.join(actor_title) + ',' + ','.join(genre) + ',' + "imdbRating,tomatoMeter\r\n"
    f.write(tt_line)
        
    for m in movie:
        temp_list = {}
        temp_actor_list = []
        for i in movie[m]["actor"]:
            if actor_find[i] not in temp_list:
                temp_list[actor_find[i]] = [i]
                temp_actor_list.append(actor_find[i])
            else:
                temp_list[actor_find[i]].append(i)

        temp_actor_list = sorted(temp_actor_list)

        line = ''
        ans_list = []
        def loop(list_a,line_b):
            if len(list_a) == 0:
                ans_list.append(line_b[1:].split(','))
            elif len(temp_list[list_a[0]]) > 1:
                for i in temp_list[list_a[0]]:
                    loop(list_a[1:],line_b+','+i)
            else:
                return loop(list_a[1:],line_b+','+temp_list[list_a[0]][0])

        loop(temp_actor_list,line)
        '''for i in ans_list:
            print (i)
        print (','.join(temp_actor_list))'''

        zero_input = []
        count = 0
        z_line = ''
        for i in actor_title:
            if count >= len(temp_actor_list) or i != temp_actor_list[count]:
                z_line = z_line + '0,'
            else:
                zero_input.append(z_line[:-1])
                count += 1
                z_line = ''
        zero_input.append(z_line[:-1])
        
        end_line = ''
        for gen in genre:
            if gen in movie[m]["genre"]:
                end_line = end_line + '1,'
            else:
                end_line = end_line + '0,' 
        end_line = end_line + movie[m]["imdbRating"] + ',' + movie[m]["tomatoMeter"]
        if len(end_line.split(',')) != 24:
            print (m,end_line)

        fin = []
        for j in range(len(ans_list)): 
            for i in range(len(ans_list[0])):
                if zero_input[i] != '':
                    fin.append(zero_input[i])
                fin.append(ans_list[j][i])
            if zero_input[-1] != '':    
                fin.append(zero_input[-1])
            if len((','.join(fin)).split(',')) != 4260:
                print (m,len((','.join(fin)).split(',')))
                print (fin)
            f.write(','.join(fin)+','+end_line+'\r\n')
            fin = []
            
        bar_count = bar_count + 1
        p.value = bar_count
        p.description = str(bar_count)
        
p.description = 'end'

