#!/usr/bin/env python
# Copyleft Gter srl 2019
#Lorenzo Benvenuto, Roberto Marzocchi, Gianluca Gambari



'''
    Simple socket server using threads
'''
 
import socket
import sys

import RPi.GPIO as GPIO
import os
import subprocess
import time
import psutil
import shutil #shell utilities

from datetime import datetime,  date




def start_test(author, tempo):
    #durata_test = int(dati[1]) #specificare la durata del test in minuti (o leggo il dato da scrivi_configurazine.php)
    durata_test = int(tempo)
    print durata_test
    durata_test_sec = durata_test*60
    print durata_test_sec
    autore = author

    time.sleep(1)


    run_rtkrcv = "sudo /home/pi/Lorenzo/RTKLIB/app/rtkrcv/gcc/rtkrcv -s -p 23 -m 24 -o /home/pi/Lorenzo/code/StazioneGNSS_raspberry/configurazioni_output/prova_{0}.conf &" .format(autore)
    print run_rtkrcv
    os.system(run_rtkrcv)
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



def scriviConfig (p1, p2, p3, p4, p5, p6, p7, p8, p9, p10, p11, p12, p13):
    #prendo i parametri e li salvo in un array
    parametri = [p2, p3, p4, p5, p6, p7, p8, p9, p10, p11, p12, p13]

    #copio il file su una cartella di rete
    #shutil.copy("./prova.conf", "../progetti_convegni/ricerca/2018_2022_PhD_Lorenzo/stazione_permanente/configurazioni/prova_{0}.conf".format(p1))   #copio il file prova conf e lo rinomino con il nome dell'autore
    #copio il file il locale
    shutil.copy("./prova.conf", "./configurazioni_output/prova_{0}.conf".format(p1))   #copio il file prova conf e lo rinomino con il nome dell'autore

    testo_config = ['=pos1-posmode', '=pos1-elmask', '=pos1-ionoopt', '=pos1-tropopt', '=pos1-sateph', '=pos1-navsys', '=out-solformat', '=out-timesys', '=out-timeform', '=out-height', '=out-geoid', '=outstr1-format']

    #percorso cartella di rete
    #config_autore = '../progetti_convegni/ricerca/2018_2022_PhD_Lorenzo/stazione_permanente/configurazioni/prova_{0}.conf'.format(p1)
    #percorso in locale
    config_autore ='./configurazioni_output/prova_{0}.conf'.format(p1)


    for i, j in zip(parametri, testo_config):
        with open(config_autore, 'r') as config:
            config_nuova = config.read()
            config_nuova = config_nuova.replace('%s' %j, '=%s' %i)
        with open(config_autore, 'w') as config:
            config.write(config_nuova)
    #per ultimo e fuori dal ciclo aggiungo il nome autore
    with open(config_autore, 'r') as config:
        config_nuova = config.read()
        config_nuova = config_nuova.replace('/test_villa', '/test_%s' % p1)
    with open(config_autore, 'w') as config:
        config.write(config_nuova)






def main():

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
        
        dati=data.split(' ')
        nome_autore = dati[0]
        pos1_posmode = dati[1]
        pos1_elmask = dati[2]
        pos1_ionoopt = dati[3]
        pos1_tropopt = dati[4]
        pos1_sateph = dati[5]
        pos1_navsys = dati[6]
        out_solformat = dati[7]
        out_timesys = dati[8]
        out_timeform = dati[9]
        out_height = dati[10]
        out_geoid = dati[11]
        outstr1_format = dati[12]
        durata_test = dati[13]

        print data
        print dati

        print nome_autore
        print pos1_posmode
        print pos1_elmask
        print pos1_ionoopt
        print pos1_tropopt
        print pos1_sateph
        print pos1_navsys
        print out_solformat
        print out_timesys
        print out_timeform
        print out_height
        print out_geoid
        print outstr1_format
        print durata_test

        print "scrittura della configurazione"

        scriviConfig(nome_autore, pos1_posmode, pos1_elmask, pos1_ionoopt, pos1_tropopt, pos1_sateph, pos1_navsys, out_solformat, out_timesys, out_timeform, out_height, out_geoid, outstr1_format)

        print "fine scrittura della configurazione"



        print "inizio del test"

        start_test(nome_autore, durata_test)

        print "fine del test"


        conn.send('OK ricevuto\0')
        
        #start_test()
    #s.close()


if __name__ == "__main__":
    main()    
quit()


    


