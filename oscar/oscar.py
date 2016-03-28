
# coding: utf-8

# In[ ]:

#ALTER TABLE tablename AUTO_INCREMENT = 1
#update actor set id=id+12817
import requests
from bs4 import BeautifulSoup
import pymysql

connection = pymysql.connect(host="127.0.0.1", user="redwing", passwd="", db="Oscar",charset='utf8')

try:
    '''with connection.cursor() as cursor:
        res = requests.get('http://www.imdb.com/title/tt4991632/fullcredits?ref_=tt_cl_sm#cast')
        soup = BeautifulSoup(res.text,'lxml')
        sql = "INSERT into actor(name) values(%s)"
        for name in soup.select('.itemprop')[::2]:
            cursor.execute(sql,(' '.join(name.text.split())),)
            print (name.text.split())
    
    connection.commit()'''
    
    with connection.cursor() as cursor:
        sql = "SELECT * FROM `actor` WHERE `id`=1"
        cursor.execute(sql)
        with open('temp.txt','w') as f:
            for i in cursor:
                print (i)
                f.write(str(i))
    
finally:
    connection.close()


# In[2]:

from urllib.request import urlopen
import json
u = urlopen('http://www.imdb.com/xml/find?json=1&nr=1&nm=on&q=Leonardo+DiCaprio')
resp = json.loads(u.read().decode('utf-8'))
print (resp['name_popular'])
print ()
for i in resp['name_approx']:
    print (i)


# In[9]:

from urllib.request import urlopen
#http://imdb.wemakesites.net/api/IMDB_RESOURCE_ID
u = urlopen('http://imdb.wemakesites.net/api/nm0000138')
resp = json.loads(u.read().decode('utf-8'))
for i in resp['data']['filmography']:
    print (i)


# In[35]:

import requests
from bs4 import BeautifulSoup
from urllib.request import urlopen
import json
import pymysql

connection = pymysql.connect(host="127.0.0.1", user="redwing", passwd="", db="Oscar",charset='utf8')
movie = ['Spotlight','The Big Short','Bridge of Spies','Brooklyn','Mad Max: Fury Road','The Martian','The Revenant','Room']
mid = {}

u = 'http://www.omdbapi.com/?t={}&y=&plot=short&r=json'
cast = 'http://www.imdb.com/title/{}/fullcredits?ref_=tt_cl_sm#cast'

for file in movie:
    url = urlopen(u.format('+'.join(file.split())))
    resp = json.loads(url.read().decode('utf-8'))
    mid[file] = resp['imdbID']


try:
    '''with connection.cursor() as cursor:
        sql = "INSERT into staff(staff_name,movie_name) values(\"{}\",\"{}\")"
        for i in mid:
            #print (cast.format(mid[i]))
            res = requests.get(cast.format(mid[i]))
            soup = BeautifulSoup(res.text,'lxml')

            print (i,mid[i])
            for name in soup.select('.itemprop')[::2]:
                #print (name.text.strip())
                print (sql.format(name.text.strip(),i))
                cursor.execute(sql.format(name.text.strip(),i))
            print ()'''
    
    with connection.cursor() as cursor:
        sql = "INSERT into movie(movie_name,movie_id) values(\"{}\",\"{}\")"
        for i in mid:           
            cursor.execute(sql.format(i,mid[i]))
            
    connection.commit()
    
finally:
    connection.close()


# In[38]:

#建立oscar的node
import pymysql
import codecs

connection = pymysql.connect(host="127.0.0.1", user="redwing", passwd="", db="Oscar",charset='utf8')

try:
    with codecs.open('oscar_node.txt','r','utf8') as f:
        with connection.cursor() as cursor:
            sql = "select `id`,`staff_name` from `staff`"
            cursor.execute(sql)
            
            for i in cursor:
                print (i)
            
            f.write("id\tnode\n")
            
            temp = []
            con = 0
            for name in cursor:
                try:
                    if name[1] in temp:
                        print (name[1])
                        con = con + 1
                    else:
                        temp.append(name[1])
                        f.write("{}\t{}\n".format(name[0]-con,name[1]))
                except:
                    print (name)
                    continue
finally:
    connection.close()


# In[36]:

#建立oscar的link
import pymysql
import codecs
import time

connection = pymysql.connect(host="127.0.0.1", user="redwing", passwd="", db="Oscar",charset='utf8')

try:
    with codecs.open('oscar_link.txt','w','utf8') as f:
        with connection.cursor() as cursor:
            sql = "select `id`,`staff_name` from `staff`"
            cursor.execute(sql)
            
            dic = {}
            con = 0
            for i in cursor:
                if i[1] not in dic:
                    dic[i[1]] = i[0] - con
                else:
                    con = con + 1
                    
            sql = "select `staff_name`,`movie_name` from `staff`"
            cursor.execute(sql)
            
            movie = {}
            for i in cursor:
                if i[1] in movie:
                    movie[i[1]].append(dic[i[0]])
                else:
                    movie[i[1]] = [dic[i[0]]]
                    
            link = {}
            for file in movie:
                l = len(movie[file])
                n = sorted(movie[file])
                for i in range(l):
                    for j in range(l-i-1):
                        c = j + i + 1
                        temp = (n[i],n[c])
                        if temp in link:
                            link[temp] = link[temp] + 1
                        else:
                            link[temp] = 1
            

            f.write("source\ttarget\ttype\tweight\n")
            for idd in link:
                try:
                    f.write("{}\t{}\t{}\t{}\n".format(idd[0],idd[1],'Undirected',link[idd]))
                except:
                    print (name)
                    continue
finally:
    connection.close()

