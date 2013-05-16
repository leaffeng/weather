#! /usr/bin/env python
# coding=utf-8

from BeautifulSoup import BeautifulSoup
import re
import urllib2
from StringIO import StringIO
BASE_URL = r'http://www.weather.com.cn/weather/'
URL_END = '.shtml'

def get3days_weather(pageid):
    url = BASE_URL + pageid + URL_END
    #print url
    request = urllib2.Request(url)
    opener = urllib2.build_opener()
    page = StringIO( opener.open(request).read() )
   # page = open("s.html")
    soup = BeautifulSoup(page)
   # print "heher"
   # f = open("s.html","w")
   # print >>f, soup.prettify()
    title = soup.find('title').text
    print title.split(":")[1]  #今日预报
    print
    today = soup.find('h1',attrs = {'class':'weatheH1','id':'live'})
    print today.text[:-18]

    yubao = soup.find('div',attrs = {'class':'weatherYubao','id':'7d'})
    print yubao.h1.text[:-16]

    box = yubao.div
    table = box.table
    #print table.contents
    head = get_table(table.contents)
    #print str(table.contents)
    #print head[0]
    days = []
    
    yubaoTable = yubao.findAll('table',attrs = {'class':"yuBaoTable", 'width':"100%" ,'border':"0" ,'cellspacing':"0" ,'cellpadding':"0"})
    for day in yubaoTable:
        for tr in day.findAll('tr'):
            t = [ td.text for td in tr.findAll('td')]
            days.append(t)
    print '='*80
    for name in head:
        print name ,"\t\t",
    print 
    print '='*80
    for day in days:
        for v in day:
            if len(v) == 2 and v is day[0]:
                print '\t\t',
            print v,'\t',
        print
    return soup


def get_table(table):
    soup = BeautifulSoup(str(table))
    d = [ th.text for th in soup.findAll('th') ]
    return d
    
def get_city_code(soup,city):
    div = soup.find('div',id="selectsionGroups")
    for li in div.findAll('li'):
        if li.text == city:
            code = li.span.a['href'].split(r'/')[-1].split('.')[0]
            return code
        
if __name__ == '__main__':
    soup = get3days_weather('101110101')
   # print get_city_code(soup,u'西安')
    
