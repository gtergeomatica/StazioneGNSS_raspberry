#!/usr/bin/env python
# -*- coding: utf-8 -*-
#Gter copyleft 
#Lorenzo Benvenuto

import sys
import os

import netifaces as ni

def readip(ifname):
    ni.ifaddresses(ifname)
    ip = ni.ifaddresses(ifname)[ni.AF_INET][0]['addr']
    print ip


#indirizzo locale vpn
readip('tun0')

#inidirizzo locale lan
readip('eth0')
