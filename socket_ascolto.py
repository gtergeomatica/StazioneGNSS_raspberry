#!/usr/bin/env python
# Copyleft Gter srl 2019
#Lorenzo Benvenuto, Roberto Marzocchi



'''
    Simple socket server using threads
'''
 
import socket
import sys
import time
import RPi.GPIO as GPIO


from datetime import datetime, date

HOST = ''   # Symbolic name, meaning all available interfaces
PORT = 8082 # Arbitrary non-privileged port
BUFFER_SIZE = 2024 

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
print 'Socket created'
 
#Bind socket to local host and port
s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

output_test=1 # LEGEND: 1 test ON - 0 test OFF

if output_test == 1:
    ora_client0=datetime.now()
    ora_file=ora_client0.strftime("%Y_%m_%d_%H_%M_%S") 
    #nome_file="/home/pi/Lorenzo/code/output_test_time_%s.csv" % ora_file
    #print nome_file
    #out_file = open(nome_file,"w")
    #out_file.write("date_time_GNSS, date_time_led, differenza (s)\n")

while True:
    try:
        s.bind((HOST, PORT))
    except socket.error as msg:
        print 'Bind failed. Error Code : ' + str(msg[0]) + ' Message ' + msg[1]
        #s.close()
        #sys.exit()
        continue
    break
     
print 'Socket bind complete'
 
#Start listening on socket
s.listen(10)
print 'Socket now listening'

# set non blocking mode per gestire l'accept con un try-except
s.setblocking(0)

#quit()
check=0

#now keep talking with the client
while True:
    try:    
        conn, addr = s.accept()
        check=0
    except:
        if check==0:        
            print "Non arriva niente"
        check=1
        continue
    #break
    #print conn    
    # calcolo ora UTC nello stesso formato dell'output di RTKLIB
    #per ora potrebbero non servire
    dt=datetime.utcnow()
    ora_client=datetime.now()
    #sovrascrivo il time start per il check sul funzionamento degradato
    start = time.time()
    # Formatting datetime
    #ora=ora_client.strftime("%Y/%m/%d %H:%M:%S.%f") 
    ora=dt.strftime("%Y/%m/%d %H:%M:%S.%f") #test sui tempi
    print "\nora=",ora
    print 'Connected with ' + addr[0] + ':' + str(addr[1])
    #data = unicode(conn.recv(BUFFER_SIZE))
    data = conn.recv(BUFFER_SIZE)            
    #dati=data.split('|')
    print data
    conn.send('OK\0')

s.close()



quit()


#socket data
TCP_IP = '192.168.2.126'
TCP_PORT = 8082
BUFFER_SIZE = 1024
check_connection=0



while True:  
    try:
        if (check_connection==0):
            s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            s.connect((TCP_IP, TCP_PORT))
        #s.send(MESSAGE)
        data = s.recv(BUFFER_SIZE)
        #s.close()
        check_connection=1
        print "received data:", data
    except: 
        print "Connessione socket non riuscita"
        check_connection=0   
    #time.sleep(0.5)
