import sys
import getopt
import random
import socket
import math
import os
import threading
import time
from collections import defaultdict


import Checksum
import BasicSender

'''
This is a skeleton sender class. Create a fantastic transport protocol here.
'''
class Sender(BasicSender.BasicSender):
    def __init__(self, dest, port, filename, debug=False, sackMode=False):
        super(Sender, self).__init__(dest, port, filename, debug)
        self.sackMode = sackMode
        self.debug = debug

    # Main sending loop.

    
    def start(self): #stop and wait version commented out.
        gobackN(self) #gobackN version being run.
##        seekto=0
##        seq_num=0
##        message=self.make_packet("syn",seq_num,"")#Start of handshake
##        self.send(message)
##        rcvd=self.receive(timeout=0.5)#End of handshake 
##        if rcvd!=None:#Start of sending actual data
##            msg_type,seqno,rcvdata,checksum=self.split_packet(rcvd)
##            seqnumber=int((seqno.split(';'))[0])
##            filesend = self.infile
##            file_size=os.path.getsize(filesend.name)
##            typ="dat"
##            while(filesend.read()):
##                filesend.seek(seekto,0)#controlling file pointer
##                seekto=seekto+1471#controlling file pointer
##                data = filesend.read(1471)#reading 1471 bytes of data from file each time
##                msg=self.make_packet(typ,seqnumber,data)
##                self.send(msg)
##                rcvd=self.receive(timeout=0.5)
##                if rcvd!=None:
##                    msg_type,seqno,rcvdata,checksum=self.split_packet(rcvd)
##                    seqno=int((seqno.split(';'))[0])
##                    if((file_size-seekto)<1471):#identifies when to send fin packet
##                        typ="fin"
##                    if (seqno==seqnumber+1):
##                        seqnumber=seqno
##                    elif (seqno==seqnumber):
##                        seekto=seekto-1471
##                        self.send(msg)
##                        rcvd=self.receive(timeout=0.5)
##                else:
##                    seekto=seekto-1471
##                    self.send(msg)
##                    rcvd=self.receive(timeout=0.5)
##        else:
##            self.start()
            
            
            
              # add things here  



def gobackN(self):
    base=1
    nextseqnum=1
    filesend=self.infile
    file_size=os.path.getsize(filesend.name) #gets the size of the file
    sntpkt=[] #list of all packets sent
    rcvdack=[] #list of all acks received
    seekto=0
    cwnd=7
    msg_type="syn"
    msg=self.make_packet(msg_type,0,"")#makes the syn packet
    self.send(msg)#sends the syn packet
    sntpkt.append(msg)
    rcvd=self.receive(0.5)
    if rcvd!=None:
        while(filesend.read()):
            filesend.seek(seekto,0)#controls the file pointer
            seekto=seekto+1471
            data=filesend.read(1471)#reading 1471 bytes of data from the file each time
            if(nextseqnum<base+cwnd):
                if file_size-seekto<=1471:
                    msg_type="fin" #applies the fin message tag to the last packet that is sent
                else:
                    msg_type="dat"
                msg=self.make_packet(msg_type,nextseqnum,data)
                self.send(msg)#sends the messages back to back as long as the nextseqnumber is less than or equal to the window size
                sntpkt.append(msg)
                nextseqnum=nextseqnum+1
                if(base==nextseqnum):
                    nextseqnum=nextseqnum+1
            rcvd=self.receive(0.5)
            while rcvd!=None:
                msg_type,ackno,rcvdata,checksum=self.split_packet(rcvd)
                ackno=int((ackno.split(';'))[0])
                rcvdack.append(ackno)
                for i in range(ackno,len(sntpkt)): #Resends from the last packet received if a packet is lost.
                    self.send(sntpkt[i])
                rcvd=self.receive(0.5)
            while rcvd==None: 
                rcvdack.append(None)
                for i in range(1, len(sntpkt)):#Resends the entire window if there is a timeout
                    self.send(sntpkt[i])
                rcvd=self.receive(0.5)
    else:
        gobackN(self)
            
        

def selective_ack(rcvdack,sntpkt,self):
    for i in sntpkt:
        msg_type,ackno,rcvdata,checksum=self.split_packet(i)
        if ackno not in rcvdack: #checks the rcvdack list and only sends packets from the sntpkt list that aren't in the rcvdack list
            self.send(i)
    rcvd=self.receive(0.5)
    





              
'''
This will be run if you run this script from the command line. You should not
change any of this; the grader may rely on the behavior here to test your
submission.
'''
if __name__ == "__main__":
    def usage():
        print ("BEARS-TP Sender")
        print ("-f FILE | --file=FILE The file to transfer; if empty reads from STDIN")
        print ("-p PORT | --port=PORT The destination port, defaults to 33122")
        print ("-a ADDRESS | --address=ADDRESS The receiver address or hostname, defaults to localhost")
        print ("-d | --debug Print debug messages")
        print ("-h | --help Print this usage message")
        print ("-k | --sack Enable selective acknowledgement mode")

    try:
        opts, args = getopt.getopt(sys.argv[1:],
                               "f:p:a:dk", ["file=", "port=", "address=", "debug=", "sack="])
    except:
        usage()
        exit()

    port = 33122
    dest = "localhost"
    filename = None
    debug = False
    sackMode = False

    for o,a in opts:
        if o in ("-f", "--file="):
            filename = a
        elif o in ("-p", "--port="):
            port = int(a)
        elif o in ("-a", "--address="):
            dest = a
        elif o in ("-d", "--debug="):
            debug = True
        elif o in ("-k", "--sack="):
            sackMode = True

    s = Sender(dest,port,filename,debug, sackMode)
    try:
        s.start()
    except (KeyboardInterrupt, SystemExit):
        exit()
