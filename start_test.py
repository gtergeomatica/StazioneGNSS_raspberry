#!/usr/bin/env python
# -*- coding: utf-8 -*-
#Gter copyleft 
#Lorenzo Benvenuto

import sys
import os
import subprocess
import time
import psutil

durata_test = int(sys.argv[1]) #specificare la durata del test in minuti (o leggo il dato da scrivi_configurazine.php)
print durata_test
durata_test_sec = durata_test*60
print durata_test_sec



os.system("sudo /home/pi/Lorenzo/RTKLIB/app/rtkrcv/gcc/rtkrcv -s -p 23 -m 24 -o /home/pi/Lorenzo/RTKLIB/app/rtkrcv/gcc/narv2.conf &")
a = []
time.sleep(2)
processi = filter(lambda p: p.name() == "rtkrcv", psutil.process_iter())
for i in processi:
    a.append(i.pid)
    print i.name, i.pid, a


process_ID = a[0]
print process_ID

time.sleep(durata_test_sec)
os.system("sudo kill %s" %process_ID)






