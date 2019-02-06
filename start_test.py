#!/usr/bin/env python
# -*- coding: utf-8 -*-
#Gter copyleft 
#Lorenzo Benvenuto

import sys
import os
import subprocess
import time
import psutil
processo= "lxpanel"


durata_test=int(raw_input("specificare la durata del test in minuti "))
print durata_test
durata_test_sec = durata_test*60
print durata_test_sec


os.system("sudo /home/pi/Lorenzo/RTKLIB/app/rtkrcv/gcc/rtkrcv -s -p 23 -m 24 -o /home/pi/Lorenzo/RTKLIB/app/rtkrcv/gcc/narv2.conf &")

processi = filter(lambda p: p.name() == "rtkrcv", psutil.process_iter())
for i in processi:
    a= i.pid
    print i.name,i.pid,a

#intervallo di tempo 
time.sleep(durata_test_sec)

os.system("sudo killall rtkrcv")
