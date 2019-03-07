#! /usr/bin/python

#GAP_ADTYPE_MANUFACTURER_SPECIFIC=0xFF
#DEVICE_CONNECTABLE=false;
import uuid
import urllib2
import json
import time
import datetime

dct = {'ADV_IND': 0x00, 'ADV_DIRECT_IND': 0x01, 'ADV_SCAN_IND':0x02, 'ADV_NONCONN_IND': 0x03,'ADV_SCAN_RSP':0x04}
class deviceItem:
    

    def __init__(self,bdaddress,advType=0x02):
          self.bdaddress = bdaddress         
          self.connactable = self.dType(dct[advType])
          self.services = []
          self.IpAddr = "-"
          self.name = "n/a"
          self.NameSpace = "0"
          self.lastseen  = datetime.datetime.now()
          

    def setSignatures(self,appSignature,appRevision):
       self.appSignature = appSignature
       self.appRevision = appRevision
    
    def setTime(self, mtime):
          self.lastseen = mtime
          
    def setRealAddress(self, realIP):
          self.IpAddr = realIP
    
    def setScanResponseName(self, mName):
          self.name = mName 
    
    def setIpadress(self, mIP):
          self.IpAddr = mIP 

    def setNSName(self, nsName):
          self.NameSpace = nsName                
          
    def setUUID(self, uid):
     if (uid!=0):
       self.UUID = uid
     else:
       self.UUID=uuid.uuid4()

    def addService(self,x):
          self.services.append(x)
    
    #veriyi gonder
    #v scan response
    #r rssi
    #d advdata
    def callWebAPI(self,v, r, d):
    	data = {'NodId' : 1, 'NodAddress' : self.bdaddress, 'sensorID' : '1' , 'sensorValue' : d, 'rssi':r, 'dname' : v}    	
    	req = urllib2.Request('http://IP_ADRES/CRUD_API_METHOD')
    	req.add_header('Content-type','application/json')
    	try:
	    resp=urllib2.urlopen(req,json.dumps(data))
	    self.deviceLastDataStatus=resp.info()
	    print 'JSON sonuc' + resp.read()
        except Exception, e:
            print e.code
            print resp.read()
		
    
    def dType(self,advPckt):
        switcher = {
                0x02:False,
                0x03:False,
                0x01:True,
                0x00: True
        }
        return switcher.get(advPckt,False)
