#!/usr/bin/python
#coding=utf-8

'''
Created on Dec 10, 2014

@author: liufei
'''

import time, sched, os, string
from datetime import datetime
import MySQLdb
 
s = sched.scheduler(time.time,time.sleep)

def event_func():
    try:
        name = os.popen(""" hostname """).read()
        cpu_num = os.popen(""" cat /proc/cpuinfo | grep processor | wc -l """).read()
        mem = os.popen(""" free | grep Mem | awk '{print $2}' """).read()
        brand = os.popen(""" dmidecode | grep 'Vendor' | head -1 | awk -F: '{print $2}' """).read()
        model = os.popen(""" dmidecode | grep 'Product Name' | head -1 | awk -F: '{print $2}' """).read()
        storage = os.popen(""" fdisk -l | grep 'Disk /dev/sd' | awk 'BEGIN{sum=0}{sum=sum+$3}END{print sum}' """).read()
        mac = os.popen(""" ifconfig -a | grep HWaddr | head -1 | awk '{print $5}' """).read()
        
    
        
        name = name.replace("\n","").lstrip()
        cpu_num =  cpu_num.replace("\n","").lstrip()
        memory_gb = round(string.atof(mem.replace("\n","").lstrip())/1000.0/1000.0, 1)
        brand = brand.replace("\n","").lstrip()
        model = model.replace("\n","").lstrip()
        storage_gb = storage.replace("\n","").lstrip()
        mac = mac.replace("\n","").lstrip()
        
        #print name
        #print cpu_num
        #print memory_gb
        #print storage_gb
        #print brand
        #print model
        #print mac
    
        conn=MySQLdb.connect(host='hostip',user='username',passwd='password',db='dbname',port=3306)
        cur=conn.cursor()
        cur.execute('select mac from servers where mac=%s',mac)
        data = cur.fetchone()

        if data is None:
            value = [name, brand, model, memory_gb, storage_gb, cpu_num, mac, datetime.now(), datetime.now()]
            cur.execute("insert into servers(name, brand, model, memory_gb, storage_gb, cpu_num, mac,  created_at, updated_at) values(%s, %s, %s, %s, %s, %s, %s, %s, %s)",value)            
        else:
            value1 = [name, brand, model, memory_gb, storage_gb, cpu_num, datetime.now(), mac]
            cur.execute("update servers set name=%s,brand=%s,model=%s,memory_gb=%s,storage_gb=%s,cpu_num=%s, updated_at=%s where mac=%s",value1)
           
        conn.commit()
        cur.close()
        conn.close()
        
    except MySQLdb.Error,e:
        print "Mysql Error %d: %s" % (e.args[0], e.args[1])
    
def perform(inc):
    s.enter(inc,0,perform,(inc,))
    event_func()
    
def mymain(inc=60):
    s.enter(0,0,perform,(inc,))
    s.run()
 
if __name__ == "__main__":
    mymain()
