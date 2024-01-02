from bluetooth import *
import sys
import subprocess
import time
import subprocess as sp

class Speaker():
     def __init__(self):
          self.pairing_status = False
          self.connected_status = False
          self.connected_speaker = None

     def run_cmd(self, command):
          """ Execute shell commands and return STDOUT """
          process = sp.Popen(command, shell=True, stdout=sp.PIPE, stderr=sp.PIPE)
          stdout, stderr = process.communicate()
     
          return stdout.decode("utf-8")

     def check_device_connected(self , addr):
          # addr = "EF:FD:DC:17:01:1D"
          info = self.run_cmd("bluetoothctl info " + addr)
          lines = info.split("\n")
          for line in lines:
               parts = line.split(":")
               if (len(parts)>1):
                    if ("Connected" in parts[0]):
                         if ("yes" in parts[1]):
                              self.connected_speaker = addr
                              return True
          
     
     def check_devices(self):
          # get paired-devices
          response = self.run_cmd("bluetoothctl paired-devices")
          devs = response.split("\n")
          device = None
          paired = []
          for dev in devs:
               if (len(dev.split(" "))>2):
                    mac  = dev.split(" ")[1]
                    name = dev.split(" ")[2]
                    # print("name : " , name , " => mac : " , mac)
                    paired.append({"name": name, "mac":mac})
                    # print("mac==>" , mac)
                    connected = self.check_device_connected(mac)
                    # print("connected==>" , connected)
                    if (connected):
                         device = {"name": name, "mac":mac}
                         # print("connected : " , connected , "  --  " , device)
                         self.connected_speaker = mac

          if (device==None):
               self.connected_speaker = None
          return device, paired


     def disconnect(self):
          if (self.connected_speaker):
               response = self.run_cmd("bluetoothctl disconnect " + self.connected_speaker)
               if ("successful" in response):
                    self.connected_status = False
                    return True


     def connectTo(self, addr):
          self.pairing_status = False
          self.connected_status = False
          pairing = self.run_cmd("bluetoothctl pair " + addr)
          connect = self.run_cmd("bluetoothctl connect " + addr)
          info = self.run_cmd("bluetoothctl info " + addr)
          print("paring:", pairing)
          print("connect:", connect)
          print("info:", info)
          if ("successful" in pairing or "AlreadyExists" in pairing):
               self.pairing_status = True

          if ("successful" in connect):
               self.connected_status = True
               return True
          
          return False
          
     def check_connected(self):
          try:
               stdoutdata = sp.getoutput("hcitool con")
               connected_addr = stdoutdata.split()[3]
               # print(stdoutdata.split())
               if len(stdoutdata.split())>0 and len(connected_addr.split(":")) > 4:
                    print("Bluetooth device is connected")
                    connected_status = True
          except:
               print("No Device is connected!")
               connected_status = False

     def scan_devices(self):
          nearby_devices = discover_devices()
          devices = []
          for bdaddr in nearby_devices:
               # print (str(lookup_name( bdaddr )) + " [" + str(bdaddr) + "]")
               already_exist = False
               for dev in devices:
                    if (dev["mac"]==str(bdaddr)):
                         already_exist = True
               if (not already_exist) :devices.append({"name":str(lookup_name( bdaddr )), "mac":str(bdaddr)})
          
          return devices

     def scan_devices_cmd(self):
          print("scan for bluetooth devices")
          devices = self.run_cmd("timeout 10s bluetoothctl scan on")
          dev_list = []
          for dev in devices.split('\n'):
               print(dev)
               # addr = dev.split(" ")[2].strip()
               # print(addr)
         
     def scan_devices_cmd_connect(self, dev_name):
          print("scan for bluetooth devices")
          devices = self.run_cmd("timeout 5s bluetoothctl scan on")
          for dev in devices.split('\n'):
               print(dev)
               if (dev_name in dev):
                    print(dev)
                    addr = dev.split(" ")[2].strip()
                    print(addr)
                    self.connectTo(addr)
                    print("device connected : " , self.connected_status)

     def scan_devices_connect(self , dev_name):
          nearby_devices = self.scan_devices()
          for bdaddr in nearby_devices:
               print (str(lookup_name( bdaddr )) + " [" + str(bdaddr) + "]")
               
               if (str(lookup_name( bdaddr ))!=None):
                    if (dev_name in str(lookup_name( bdaddr ))):
                              print(bdaddr)
                              self.connectTo(bdaddr)
                              print("device connected : " , self.connected_status)
                              break
          
          if (not self.connected_status):
               self.scan_devices_cmd_connect(dev_name)


# scan_devices_connect()

