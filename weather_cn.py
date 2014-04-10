#! /usr/bin/python
# -*- coding: utf-8 -*-
##############################
# Author: leaffeng
# E-mail: yfengye@gmail.com
##############################

import urllib2, json
from datetime import date,timedelta
import MySQLdb as mdb

m_base_url = "http://m.weather.com.cn/data/"

def instert_city():
	id_name = {}
	with open('cityid') as f:
		for c in f:
			if c and c != '\n':
				cid = c.split("=")
				print cid
				id_name[cid[1].strip()] = cid[0].strip()

	#将con设定为全局连接
	con = mdb.connect('localhost', 'root', 'root1234', 'weather')
	print "sucess"
	with con:

		cur = con.cursor()

    	for cname in id_name:
    		print cname,id_name[cname]
    		cur.execute('''INSERT INTO city VALUES(%s,%s)''',(cname,id_name[cname]))
    	con.commit()
    	cur.execute("select * from city")
    	row = cur.fetchone()
    	print row[0]


def get_cityid(city):
	con = mdb.connect('localhost', 'root', 'root1234', 'weather')
	with con:
		cur = con.cursor()
		#print "select * from city where city_name=%s" % city
		cur.execute(u"select * from city where city_name=%s",city)
		row = cur.fetchone()
		return row[1]

def forecast(cityid):
	url = m_base_url + cityid +".html"
	response = urllib2.urlopen(url)
	tw = json.load(response)
	parse_weather(tw['weatherinfo'])

def parse_weather(info):
	print info['city'],
	print "\t",info['date_y'],
	print " ", info['week']
	print_header()
	today = date.today()
	for i in range(6):		
		s = str(i+1)
		print today + timedelta(i),
		print "\t",info['temp'+s],
		print "\t",info['weather'+s],
		print "\t\t",info['wind'+s]

def print_header():
	print '='*79
	print "date\t\ttemp\t\tweather\t\twind"
	print '='*79

if __name__== '__main__':
    #instert_city()
    c = get_cityid('西安')
    forecast(c)
