
# coding: utf-8

# In[ ]:

#網頁抓取
#說明文件 https://www.crummy.com/software/BeautifulSoup/bs4/doc.zh/
import requests
from bs4 import BeautifulSoup

res = requests.get("網址列")
soup = BeautifulSoup(res.text, "lxml")

for name in soup.select("tag位址"):
    print (name.text)

#-------------------------------------------------------

#資料庫連接
import pymysql

connection = pymysql.connect(host="127.0.0.1", user="名字", passwd="密碼", db="資料庫名字",charset='utf8')

try:
    with connection.cursor() as cursor:
        sql = "INSERT into actor(name) values(\"{}\")" #前者為table及其屬性，後者為要放進去的值
        cursor.execute(sql.fortmat("放入值"))
    
    #若有修改到資料庫，必須有這行才會執行動作
    connection.commit()
    
    with connection.cursor() as cursor:
        sql = "SELECT * FROM `actor` WHERE `id`=1" #基本sql指令
        cursor.execute(sql)
            
        for i in cursor:
            print (i)    
finally:
    connection.close()
    
#--------------------------------------------------------

#正規表示法運用
#以下是判斷單字是否為中文字(已轉成ASCII)，並回傳true/false
re.search(u'[\u4e00-\u9fa5]+',"單字")

#正規表示法可參照下列網頁
#http://marco79423.twbbs.org/articles/%E6%B7%BA%E8%AB%87-regex-%E5%8F%8A%E5%85%B6%E6%87%89%E7%94%A8/
#http://ccckmit.wikidot.com/regularexpression


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


# In[4]:

#建立oscar的staff和id表
#待解決問題：staff表內的重複資訊，如：Ridley Scott
import requests
from bs4 import BeautifulSoup
from urllib.request import urlopen
import json
import pymysql
import time

connection = pymysql.connect(host="127.0.0.1", user="redwing", passwd="", db="Oscar",charset='utf8')
movie = ['Spotlight','The Big Short','Bridge of Spies','Brooklyn','Mad Max: Fury Road','The Martian','The Revenant','Room']
mid = {}

u = 'http://www.omdbapi.com/?t={}&y=&plot=short&r=json'
cast = 'http://www.imdb.com/title/{}/fullcredits?ref_=tt_cl_sm#cast'

#從電影名稱得到電影ID
for file in movie:
    url = urlopen(u.format('+'.join(file.split())))
    resp = json.loads(url.read().decode('utf-8'))
    mid[file] = resp['imdbID']


try:
    #staff
    with connection.cursor() as cursor:
        sql = "INSERT into staff(staff_name,staff_id,movie_name) values(\"{}\",\"{}\",\"{}\")"
        
        mv = {}
        
        for i in movie:
            mv[i] = []
        
        for i in mid:
            #print (cast.format(mid[i]))
            res = requests.get(cast.format(mid[i]))
            soup = BeautifulSoup(res.text,'lxml')

            print (i,mid[i])
            for name in soup.select('.itemprop')[::2]:
                #print (name.text.strip())
                #print (name.text.strip(),i,name.a['href'].split('/')[2])
                #print (sql.format(name.text.strip(),i))
                #print (name.text.strip(),i)
                temp = (name.text.strip(),name.a['href'].split('/')[2])
                if temp not in mv[i]:
                    mv[i].append(temp)
                #cursor.execute(sql.format(name.text.strip(),i))
                
            for name in soup.select('.name > a'):
                #print (name.prettify())
                #print (name.text.strip(),i,name['href'].split('/')[2])
                #print (name.text.strip(),i)
                temp = (name.text.strip(),name['href'].split('/')[2])
                if temp not in mv[i]:
                    mv[i].append(temp)
                #cursor.execute(sql.format(name.text.strip(),i))
                             
        for i in mv:
            for j in mv[i]:
                #print (sql.format(j[0],j[1],i))
                cursor.execute(sql.format(j[0],j[1],i))
                #time.sleep(0.5)
    
    #movie
    '''with connection.cursor() as cursor:
        sql = "INSERT into movie(movie_name,movie_id) values(\"{}\",\"{}\")"
        for i in mid:           
            cursor.execute(sql.format(i,mid[i]))'''
    
    #id
    '''with connection.cursor() as cursor:
        sql = "INSERT into id(staff_name,staff_id) values(\"{}\",\"{}\")"
          
        idd = {}    
            
        for i in mid:
            #print (cast.format(mid[i]))
            res = requests.get(cast.format(mid[i]))
            soup = BeautifulSoup(res.text,'lxml')
            
            print (i,mid[i])
            for name in soup.select('.itemprop')[::2]:
                nid = name.a['href'].split('/')[2]
                n = name.text.strip()
                
                if n not in idd:
                    idd[n] = [nid]
                elif nid not in idd[n]:
                    idd[n].append(nid)
                #cursor.execute(sql.format(name.text.strip(),name.a['href'].split('/')[2]))
                
            for name in soup.select('.name > a'):
                nid = name['href'].split('/')[2]
                n = name.text.strip()
                
                if n not in idd:
                    idd[n] = [nid]
                elif nid not in idd[n]:
                    idd[n].append(nid)
                #cursor.execute(sql.format(name.text.strip(),name['href'].split('/')[2]))
        
        gg = 0
        for j in idd:
            gg = gg + len(idd[j])
            #if len(idd[j]) > 1:
            #    print (len(idd[j]),j,idd[j])
            for k in idd[j]:
                #print (j,k)
                cursor.execute(sql.format(j,k))
                #time.sleep(0.5)'''
                
        #print (len(idd)) #5787
        #print (gg) #5795
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


# In[3]:

import requests
from bs4 import BeautifulSoup

url = 'http://www.imdb.com/title/tt1596363/fullcredits?ref_=tt_cl_sm#cast'

res = requests.get(url)
soup = BeautifulSoup(res.text,'lxml')

for name in soup.select('.name > a'):
    #print (name.prettify())
    print (name.text.strip(),name['href'].split('/')[2])
    print ()


# In[28]:

import pymysql
import codecs
import time

connection = pymysql.connect(host="127.0.0.1", user="redwing", passwd="", db="Oscar",charset='utf8')

try:
    with connection.cursor() as cursor:
        sql = "select distinct `staff_id` from `{}`"
    
        sst = []
        idd = []
        
        cursor.execute(sql.format('staff'))
        
        for i in cursor:
            sst.append(i[0])
        
        cursor.execute(sql.format('id'))
        
        for i in cursor:
            if i[0] not in sst:
                print (i[0])

        
    
finally:
    connection.close()


# In[28]:

#包含職位的IMDB資料提取
import requests
from bs4 import BeautifulSoup
from urllib.request import urlopen
import json
import pymysql
import time

connection = pymysql.connect(host="127.0.0.1", user="redwing", passwd="", db="Oscar",charset='utf8')

movie = ['Spotlight','The Big Short','Bridge of Spies','Brooklyn','Mad Max: Fury Road','The Martian','The Revenant','Room']
mid = {}

u = 'http://www.omdbapi.com/?t={}&y=&plot=short&r=json'
member = 'http://www.imdb.com/title/{}/fullcredits?ref_=tt_cl_sm#cast'

job = []
g = []

#從電影名稱得到電影ID
for file in movie:
    url = urlopen(u.format('+'.join(file.split())))
    resp = json.loads(url.read().decode('utf-8'))
    mid[file] = resp['imdbID']

try:
    with connection.cursor() as cursor:

        sql = "INSERT into staff(staff_name,staff_id,movie_id,job) values(\"{}\",\"{}\",\"{}\",\"{}\")"

        for file in mid:
            res = requests.get(member.format(mid[file]))
            soup = BeautifulSoup(res.text,'lxml')

            term = ''

            print (file,mid[file])
            
            #針對不同位置作抓取調整
            for i in soup.select('#fullcredits_content'):
                for j in i.find_all(class_=['dataHeaderWithBorder','simpleTable','cast_list']):
                    #print (j.get_text(strip=True))
                    #print (j['class'])

                    if j['class'][0] == 'dataHeaderWithBorder':
                        temp = j.get_text(strip=True)
                        if temp.split()[-1] != 'by' and temp.split()[-1] != 'By':
                            #print (temp)
                            term = temp
                        else:
                            #print (' '.join(temp.split()[:-1]))
                            term = ' '.join(temp.split()[:-1])
                        if term not in job:
                            job.append(term)
                    elif j['class'][0] == 'simpleTable':
                        for l in j.select('.name'):
                            #print (l.get_text(strip=True),l.a['href'].split('/')[2],term)
                            cursor.execute(sql.format(l.get_text(strip=True),l.a['href'].split('/')[2],mid[file],term))

                    elif j['class'][0] == 'cast_list':
                        '''for k in j.select('.itemprop')[::2]:
                            print (k.get_text(strip=True),k.a['href'].split('/')[2],'cast')
                            #cursor.execute(sql.format(k.get_text(strip=True),k.a['href'].split('/')[2],mid[file],'cast'))
                            pass'''
                        for k in j.find_all(class_=['itemprop','castlist_label']):
                            if k['class'][0] == 'castlist_label':
                                if k.get_text() != '':
                                    #print (k.get_text(strip=True))
                                    term = 'Rest of cast'
                                else:
                                    term = 'cast'
                                
                                if term not in job:
                                    job.append(term)
                            elif k['itemprop'] == 'actor':
                                #print (k.get_text(strip=True),k.a['href'].split('/')[2],mid[file],term)
                                cursor.execute(sql.format(k.get_text(strip=True),k.a['href'].split('/')[2],mid[file],term))

                                    
            print ()
        print (job)
        
    connection.commit()
finally:
    connection.close()


# In[6]:

#抓取資料
#Alejandro G. Iñárritu = Alejandro González Iñárritu
#Take 演員問題 Lost in Translation
import requests
#from urllib.request import urlopen
import json
import time
import codecs
from bs4 import BeautifulSoup
import re

path = "C:\\Users\\user\\Desktop\\"
movie = []

imdb_cast = 'http://www.imdb.com/title/{}/fullcredits?ref_=tt_cl_sm#cast'
u = 'http://www.omdbapi.com/?t={}&y=&plot=short&r=json&tomatoes=true' #抓取年分，導演，編劇，影片id
cast = 'http://imdb.wemakesites.net/api/{}' #抓取演員
staff = 'http://www.imdb.com/xml/find?json=1&nr=1&nm=on&q={}' #抓取演員id

with codecs.open(path+"movie.txt",'rb','utf8') as f:
    for line in f:
        movie.append(line.strip())
        
#從電影名稱得到電影ID，並生成電影相關資訊
'''with codecs.open(path+"movie.csv",'wb','utf8') as f:
    f.write("Title,imdbID,Year,Genre,tomatoMeter\r\n")
    for file in movie:
        content = requests.get(u.format('+'.join(file.split())))
        resp = json.loads(content.text)
        #print (resp['Title'],resp["imdbID"],resp["Year"],resp["tomatoMeter"])
        #加引號是要處理標題內有分號
        f.write('"'+resp['Title']+'"'+','+resp["imdbID"]+','+resp["Year"]
                +','+'&'.join(resp["Genre"].split(', '))+','+resp["tomatoMeter"]+'\r\n')'''

index = 1

#產生演員相關資訊，演員不見得是對的QQ
#新修正已OK，但須注意縮寫名字
'''with codecs.open(path+"actor.csv",'wb','utf8') as f:
    #print ("name,id,imdbID,job,job comment\r\n")
    f.write("name,id,imdbID,job,job comment\r\n")
    for file in movie:
        print (file)
        content = requests.get(u.format('+'.join(file.split())))
        resp = json.loads(content.text)
        
        res = requests.get(imdb_cast.format(resp["imdbID"]))
        soup = BeautifulSoup(res.text, "lxml")

        def name_find(job):

            for i in resp[job].split(', '):
                temp = i.split(' (')

                #content2 = requests.get(staff.format('+'.join(temp[0].split())))
                #resp2 = json.loads(content2.text)

                if len(temp) > 1:
                    job_comment = '('+temp[1]
                else:
                    job_comment = '(NaN)'

                #try:
                #    #print (temp[0],resp2['name_popular'][0]['id'],resp["imdbID"],job,job_comment)
                #    f.write(temp[0]+','+resp2['name_popular'][0]['id']+','+resp["imdbID"]+','+job+','+job_comment+'\r\n')
                #except:
                #    try:
                #        #print (temp[0],resp2['name_exact'][0]['id'],resp["imdbID"],job,job_comment)
                #        f.write(temp[0]+','+resp2['name_exact'][0]['id']+','+resp["imdbID"]+','+job+','+job_comment+'\r\n')
                #    except:
                #        #print (temp[0],resp2['name_approx'][0]['id'],resp["imdbID"],job,job_comment)
                #        f.write(temp[0]+','+resp2['name_approx'][0]['id']+','+resp["imdbID"]+','+job+','+job_comment+'\r\n')
                
                try:
                    name = temp[0]
                    idd = soup.find_all("a",text=re.compile(name))[0]['href'].split('/')[2]
                    imdbid = resp["imdbID"]

                    #print (name,idd,imdbid,job,job_comment)
                    f.write(name+','+idd+','+imdbid+','+job+','+job_comment+'\r\n')
                except:
                    print ('error',temp[0],resp["imdbID"])
                

        def actor_find():

            content3 = requests.get(cast.format(resp["imdbID"]))
            resp3 = json.loads(content3.text)

            for actor in resp3["data"]["cast"]:

                #content2 = requests.get(staff.format(actor))
                #resp2 = json.loads(content2.text)

                #try:
                #    #print (actor,resp2['name_popular'][0]['id'],resp["imdbID"],"Actor","(NaN)")
                #    f.write(actor+','+resp2['name_popular'][0]['id']+','+resp["imdbID"]+','+"Actor"+','+"(NaN)"+'\r\n')
                #except:
                #    try:
                #        #print (actor,resp2['name_exact'][0]['id'],resp["imdbID"],"Actor","(NaN)")
                #        f.write(actor+','+resp2['name_exact'][0]['id']+','+resp["imdbID"]+','+"Actor"+','+"(NaN)"+'\r\n')
                #    except:
                #        #print (actor,resp2['name_approx'][0]['id'],resp["imdbID"],"Actor","(NaN)")
                #        f.write(actor+','+resp2['name_approx'][0]['id']+','+resp["imdbID"]+','+"Actor"+','+"(NaN)"+'\r\n')
                
                try:
                    name = actor
                    idd = soup.find_all("span",text=name)[0].parent['href'].split('/')[2]
                    imdbid = resp["imdbID"]

                    #print (name,idd,imdbid,"Actor","(NaN)")
                    f.write(name+','+idd+','+imdbid+','+"Actor"+','+"(NaN)"+'\r\n')
                except:
                    print ('error',actor,resp["imdbID"])

        name_find("Director")
        name_find("Writer")
        actor_find()
        #time.sleep(40)
        
        if index % 10 == 0:
            time.sleep(30)
        
        index = index + 1'''

#確認演員是否真有出演電影
'''with codecs.open(path+'actor.csv','rb','utf8') as f:
    lines = f.readlines()
    lines.pop(0)
    
    for name in lines:
        idd = name.split(',')[1]
        imdbid = name.split(',')[2]
        
        content = requests.get(cast.format(idd))
        resp = json.loads(content.text)
        
        files = []
        
        #因為可能有長期節目，所以不用年份而單純改以imdbid做比對
        #可能只有演員會有出演電影列表
        if name.split(',')[3] == 'Actor':
            for i in resp['data']['filmography']:
                files.append(i['info'].split('/')[4])

            if imdbid not in files:
                print (resp['data']['title'],idd,imdbid)
        
        index = index + 1
        print (index)'''

#各演員出演電影
with codecs.open(path+'movie_more.csv','wb','utf8') as m:
    with codecs.open(path+'actor.csv','rb','utf8') as f:
        lines = f.readlines()
        lines.pop(0)

        for name in lines:
            idd = name.split(',')[1]

            content = requests.get(cast.format(idd))
            resp = json.loads(content.text)

            print (name.split(',')[0])
            m.write('#'+name.split(',')[0]+'\r\n')

            for i in resp['data']['filmography']:
                try:
                    year = int(i['year'].split(';')[1].split('/')[0])
                    if year >= 2001 and year <= 2015:
                        #print ('"'+i['title']+'"',year,i['info'].split('/')[4])
                        m.write('"'+i['title']+'"'+','+str(year)+','+i['info'].split('/')[4]+'\r\n')
                except ValueError:
                    continue
            index = index + 1
            time.sleep(5)
            if index % 30 == 0:
                time.sleep(30)
        
        
print ('END')


# In[29]:

#資料清理，拿掉actor內的comment，1、2層之間連結處理
import codecs
import time
import json
import requests

path = "C:\\Users\\user\\Desktop\\"
u= 'http://www.omdbapi.com/?i={}&y=&plot=short&r=json&tomatoes=true'
dic = {}

'''with codecs.open(path+'actor.csv','rb','utf8') as f:
    with codecs.open(path+'actor_com.csv','wb','utf8') as g:
        
        content = f.readlines()
        
        for i in content:
            temp = i.split(',')
            
            g.write(temp[0]+','+temp[1]+','+temp[2]+','+temp[3]+'\r\n')'''

index = 0
with codecs.open(path+"movie_more_clean.csv",'wb','utf8') as g:
    with codecs.open(path+"movie_more.csv",'rb','utf8') as f:
        content = f.readlines()

        for i in content:
            if i[0] == '#':
                continue
            temp = i.strip().split(',')

            if len(temp) > 3:
                temp = [','.join(temp[0:-2]),temp[-2],temp[-1]]

            #print (temp[0][1:-1])
            #time.sleep(0.3)

            if temp[1] not in dic:
                dic[temp[1]] = {temp[2]:temp[0]}
            else:
                if temp[2] not in dic[temp[1]]:
                    dic[temp[1]][temp[2]] = temp[0]

        g.write('Title'+','+'imdbID'+','+'Year'+','+'Genre'+','+'imdbRating'+','+'tomatoMeter'+'\r\n')
        
        for i in range(2001,2016):
            for j in dic[str(i)]: 
                
                #content = requests.get(u.format(j))
                #resp = json.loads(content.text)
                
                #print (dic[str(i)][j],j,str(i))
                g.write(dic[str(i)][j]+','+j+','+str(i)+'\r\n')
                #g.write(dic[str(i)][j]+','+j+','+str(i)+','+'&'.join(resp['Genre'].split(', '))
                #        +','+resp['imdbRating']+','+resp['tomatoMeter']+'\r\n')
                
                '''index = index + 1
                if index % 100 == 0:
                    print (index)'''

print ('END')

