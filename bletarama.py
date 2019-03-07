

import cmd
import os
import re
import subprocess
import mclsBleScanner
import sys
import threading
import urllib2
import json
from bluetoothDevice import deviceItem
import bluetooth._bluetooth as bluez
import requests

dev_id = 1
sock = None
devam = True

df = subprocess.check_output("lsusb", shell=True)
devices = []

class Scanner:

    def readDevices(self):
        global sock
        returnedList = mclsBleScanner.parse_events(sock, 1)
        #check always last item        
        if len(returnedList) > 0:            
            self.addParseDevice(returnedList[len(returnedList)-1])
        
        threading.Timer(2, self.readDevices).start()
       

    def addParseDevice(self,x):
        a=""
        b=""
        c=""
        d=""
        e=""
        print(len(x))
        if len(x)>0:
          try:
            a,b,c,d,e=x.split(",")
          except:
            x+=",-"
          a,b,c,d,e=x.split(",")
          global devices
          print(x)
          if any(dvc.bdaddress == a for dvc in devices) ==False:
             myitem=deviceItem(a,b)
             myitem.setUUID(0)
             devices.append(myitem)
             print("Cihaz Eklendi")
          else:
             dvc=next((x for x in devices if x.bdaddress == a), None)             
             if (b=="ADV_SCAN_RSP"):
             	 self.adiniyaz(a,c)
             	 dvc.callWebAPI(c,d,'-')
             elif (b=="ADV_SCAN_IND"):
             	 print "SCNRSP:-,ADVDATA: %s\tRSSI: %s" % (c , d)
             	 dvc.callWebAPI('-',d,c)
             elif (b=="ADV_NONCONN_IND"):             	 
                 print "SCNRSP:-,ADVDATA: %s\tRSSI: %s" % (c , d)
                 dvc.callWebAPI('-',d,c)
             
        #dvc=next((x for x in devices if x.bdaddress == a), None)
        #if dvc!=None:

    def adiniyaz(self,adres,adi):
        global devices
        for dvc in devices:
            if dvc!=None:
               if dvc.bdaddress == adres:
                  dvc.setScanResponseName(adi)
               	  #dvc.name=adi
               
    def goster(self):
        global devices
        for dvc in devices:
            if dvc!=None:             
               print "Adres: %s \tBaglantiTipi: %s \tAdi: %s" % (dvc.bdaddress, dvc.connactable, dvc.name.replace("name:", ""))
   

    def baslat(self):
	   os.system("hciconfig hci0 down")
	   os.system("hciconfig hci0 up")
           print 'Cihaz aktif hale getirildi'
           try:
                global dev_id
                global sock 
                dev_id=0
                sock = bluez.hci_open_dev(dev_id)
                print "ble thread started"
           except:
                print "bluetooth cihazina erisilemedi..."
                sys.exit(1)

           mclsBleScanner.hci_le_set_scan_parameters(sock)
           mclsBleScanner.hci_enable_le_scan(sock)
           mclsBleScanner.hci_connect_le(sock, "B8:27:EB:98:27:EA")
           self.readDevices()






class MyMenu(cmd.Cmd):
    
    def emptyline(self):
        pass
    
    def default(self, line):
        print 'default(%s)' % line
        return cmd.Cmd.default(self, line)
    
    def do_yardim(self, line):
        print "Komutlar\n"
        print "baslat (Taramayi baslatir)\n"
        print "durdur (Taramayi durdurur)\n"
        print "devam (Taramayi devam ettirir)\n"        
        print "cihazlar (bulunan cihazlari gosterir)\n"       
    
    def do_baslat(self,a):
        global devam
        devam = True
        p1=Scanner()
        p1.baslat()

    def do_devam(self,a):
        global devam
        devam = True
        
    def do_durdur(self,a):
        global devam
        devam = False 
    
    def do_cikis(self,a):
    	os._exit(0)
    	
    def do_cihazlar(self,b):  
        p2=Scanner()
        p2.goster()       
    
    def do_EOF(self, line):
        return True
    
    def postloop(self):
        print

if __name__ == '__main__':
    MyMenu().cmdloop()
