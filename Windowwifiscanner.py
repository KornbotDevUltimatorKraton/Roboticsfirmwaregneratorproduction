import os 
import time 
import socket 
import multiprocessing 
import subprocess 
#wifiscanner = subprocess.check_output("netsh wlan show networks mode=bssid",shell=True)
#print(wifiscanner.decode()) 
wifidict = {}
import pywifi
import time

wifi = pywifi.PyWiFi()
iface = wifi.interfaces()[0]
iface.scan()
time.sleep(0.5)
results = iface.scan_results()

#print(results)
for er in range(0,3):
  for i in results:
     bssid = i.bssid
     ssid  = i.ssid
     #print(f"{bssid}: {ssid}")
     #print(ssid)
     wifidict[ssid] = bssid
     
print(wifidict)
print("Show list wifi scanner")
for i in list(wifidict):
        print(i) 