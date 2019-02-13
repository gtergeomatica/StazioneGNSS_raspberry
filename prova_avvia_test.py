#!/usr/bin/env python
# -*- coding: utf-8 -*-
#Gter copyleft
#Lorenzo Benvenuto

import sys
import os
import subprocess
import time
import psutil

path = '/home/pi/Lorenzo/RTKLIB/app/rtkrcv/gcc/'

os.chdir(path)

cwd = os.getcwd()

print cwd

config_file = '/home/pi/Lorenzo/RTKLIB/app/rtkrcv/gcc/narv2.conf'

os.system("./rtkrcv -o /home/pi/Lorenzo/RTKLIB/app/rtkrcv/gcc/narv2.conf")