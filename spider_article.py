# -*- coding: utf-8 -*-
import re
import os
import sys
import urllib2  
from bs4 import BeautifulSoup

'''
header = {
    'User-Agent':'Mozilla/5.0 (Windows; U; Windows NT 6.1; en-US; rv:1.9.1.6) Gecko/20091201 Firefox/3.5.6'
}
 
def getUrls(url):
    s = re.compile(r'<a href="/collection/.*" class="thumbnail">')                                            #用于抓取多个模块的文章,这段代码没用上
    #re.compile(r'<a href="/collection/.*">.*</a>')
    
    req = urllib2.Request(
        url = url,
        headers = header
        )
    urls = urllib2.urlopen(req)
    m = re.findall(s,urls.read())
    return m
'''

def save_article(filename,m):
    f = open(filename,'w+')                                                       #存储文章至本地
    #res = re.compile(r'<p>.*</p>')                                               
    res2 = re.compile(r'<div class="show-content">[\s\S]*?</div>')            #提取文章正文的正则表达式 


    n = re.findall(res2,m)
    n = n[0]
    n = re.sub(r'</p>','\n    ',n)
    n = re.sub(r'<[div|src|/div].*>','',n)
    n = re.sub(r'<.*>','',n)
    f.write(n)
    f.close()


def create_dir(path):
    if not os.path.exists(path):
        os.makedirs(path)
    os.chdir(path)


def saveArticle():
    global n,count
    x = 1
    count = 0
    i= '<a href="/collection/dqfRwQ" class="thumbnail">'                              #需要提取文章的目录URL
    start1 = i.find(r'href=')+6
    end1 = i.find(r'class=') - 2
    
    while(True):
        if count%9==0:
            x = x + 1
        s1 = 'http://www.jianshu.com'+i[start1:end1]+'/top?page=' + str(x)           #用于翻页,获取更多的文章

        m1 = urllib2.urlopen(s1).read()
        soup1 = BeautifulSoup(m1)


        contentname = soup1.title.string
        print '================================ '+contentname+'=============== '

        s2 = re.compile(r'<h4><a href="/p/.*" target="_blank">.*</a></h4>')#提取文章URL的正则表达式

        article_url = re.findall(s2,m1)
        for j in article_url:
            count += 1
            start2 = j.find(r'href=')+6
            end2 = j.find(r'target=') - 2
            s3 = 'http://www.jianshu.com'+j[start2:end2]                              #重组文章的URL
            m = urllib2.urlopen(s3).read()
            soup2 = BeautifulSoup(m)

            path = '/home/dada/pythonprogram/' + contentname                               #创建文件夹
            create_dir(path)   
            filename =soup2.title.string + '.markdown'

            print filename
            f = open(filename,'w+')

            save_article(filename,m)
            
        if(count >= 100):
            break

print 'Dowloading.....'

n="<p>sd5gsdag</p>"
n.replace("<p>","")
saveArticle()
print '      ================================ DONE ================================'
