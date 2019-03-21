import sys
import socket                   # Import socket module

s = socket.socket()             # Create a socket object
host = "192.168.2.4"  #Ip address that the TCPServer  is there
port = 8085           # Reserve a port for your service every new transfer wants a new port or you must wait.

s.connect((host, port))
#s.send("Hello server!") 
nomefile =  sys.argv[1]  #This script should be in the same folder of the file you want to send
print(nomefile)
s.send(nomefile)
path='/home/pi/Lorenzo/code/StazioneGNSS_raspberry/risultati_test'

f = open('{0}/{1}'.format(path,nomefile),'rb')
l = f.read(1024)
while (l):
    s.send(l)
    print('Sent ',repr(l))
    l = f.read(1024)
f.close()

# with open('received_file', 'wb') as f:
#     print 'file opened'
#     while True:
#         print('receiving data...')
#         data = s.recv(1024)
#         print('data=%s', (data))
#         if not data:
#             break
#         # write data to a file
#         f.write(data)

#f.close()
print('Successfully sent the file')

data = s.recv(1024)
print(repr(data))
s.close()
print('connection closed')