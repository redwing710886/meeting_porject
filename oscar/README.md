# OSCAR
##資料收集
為了蒐集入圍OSCAR最佳影片獎的作品與底下主要演員，
我們先透過wikipedia得到2001~2015年所有入圍最佳影片的候選名單，

得到影片名單後，再透過以下API進行資料爬取(皆為json型式)：
1.http://www.omdbapi.com/ 得到電影在imdb上的id,年分,影片類別,導演,編劇,imdbRating,tomatoMeter
2.http://www.imdb.com/xml/find?json=1&nr=1&nm=on&q={NAME+OF+ACTOR} 透過名字找出演員在imdb上的id
3.http://imdb.wemakesites.net/ 得到電影內的主要演員及演員所參與過的電影

當然這裡也有些問題點存在，如：
1.


##資料清洗
