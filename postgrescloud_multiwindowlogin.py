#using the input data from the pyqt5 to login into the system with the client login app to checking with the database 
import os 
import sys 
import csv
import json
import requests
import socket
import pywifi
import getpass 
import psycopg2 # Login for the client side on the app machine 
import pandas as pd 
import subprocess # Getting the subprocess 
import multiprocessing
import cv2, imutils, socket # Getting the opencv to connect with the web socket base to report the camera output to display on the gui firmware uploader 
import numpy as np
import time
import base64
import random # Random the function of the nodes inside the flow chart function 
import pywifi # using pywifi to sniff the wifi using in the range of network detection 
from PyQt5.QtCore import Qt, QSize, QTimer, QThread
from PyQt5 import QtCore, QtWidgets, uic,Qt,QtGui 
from PyQt5.QtWidgets import QApplication,QTreeView,QDirModel,QFileSystemModel,QVBoxLayout, QTreeWidget,QStyledItemDelegate, QTreeWidgetItem,QLabel,QGridLayout,QLineEdit,QDial,QComboBox,QTextEdit,QTabWidget,QLineEdit,QPushButton
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.QtCore import *
from PyQt5.QtGui import QPixmap,QIcon,QImage,QPalette,QBrush
from pyqtgraph.Qt import QtCore, QtGui   #PyQt graph to control the model grphic loaded  
#>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>
#Pyqt5 opengl 
import pyqtgraph as pg 
from pyqtgraph.flowchart import Flowchart, Node 
import pyqtgraph.flowchart.library as fclib 
from pyqtgraph.flowchart.library.common import CtrlNode
import pyqtgraph.metaarray as metaarray
import pyqtgraph.opengl as gl
from paramiko import SSHClient, AutoAddPolicy # SSH remote command to activate the host machine control
import win32api 
drives = win32api.GetLogicalDriveStrings() 
drives = drives.split('\000')[:-1] 
  
#>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>
#Query database from the remote postgresql 
#using this postgresql-opaque-57490 #heroku cloud postgresql roboreactoruser https://roboreactoruser.herokuapp.com/ | https://git.heroku.com/roboreactoruser.git
#*postgresql-rigid-15553  #heroku cloud postgresql robouserdb https://robouserdb.herokuapp.com/ | https://git.heroku.com/robouserdb.git
#postgresql-amorphous-76096 as DATABASE_URL https://robotuserinterface.herokuapp.com/
#Database url can be get from this command heroku config:get DATABASE_URL -a app name
DATABASE_URL = "postgres://wwpxpsshftlinh:b85574f77cd76ccbaef7a0f661086c6b28724d236c730c74c2d8021934e8bbe1@ec2-18-215-96-54.compute-1.amazonaws.com:5432/d8rl9i6joj63v8"
Host = "ec2-18-215-96-54.compute-1.amazonaws.com"
Database = "d8rl9i6joj63v8"
Password = "b85574f77cd76ccbaef7a0f661086c6b28724d236c730c74c2d8021934e8bbe1"
Port = "5432"
username = getpass.getuser()
print(username)
memwrite = [] #Getting the status of the writing process 
OS_name = [] #Getting the operating system choosing for uploadinto the robot
network_name = []
dict_cc = {} #Getting the dictionary
ip = []  # Getting the current machine ip data 
Memhostpartip = []  # Getting the Memhostpartip of the machine 
Gateway_router = [] # Getting the gateway router 
wifidict = {}
username = getpass.getuser()
print(username)
PATH_SD_CARD = "/media/"+str(username)   #Path of the SD card 
name = "name"
code = "code"
ssidmem = [] #Getting the array ssid mem for the data of the wifi host name 
#>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>
# Component classification function
dict_components = {} # Getting the dictionary of the component in the json array data 
Check_found_components = [] # Get the found components data inside the list
Concatinate_components = [] # Getting the data of component in list together 
Classified_list_components = []
# list of buyable part components data 
# *Board = microcontroller spec and specification data these data will be extracted from the pins output from the pdf file 
components = ['Imagesensor','Board','Computeronboard','ActuatorDriverIC','CellularLTEmod','SensorArray','Navigationsensor','AmplifiermoduleIC','Battery','BMSmodule'] # Getting the components  
# list of the function on the software data 
Software_data = ['Objectdetection','Objectrecognition','Facerecognition','Posedetection','Poserecognition'] # Getting the data of software camera detection components 
#list of the communication type data
communication_component = ['Serial-baudrate','CANBUS-baudrate']

listcommatch = {"Board":"Boarddata","Computeronboard":"Computernode","Imagesensor":"Imagecameramodule","Sensors":"Sensormodule","Acousticamplifier":"Acousticampmodule","Navigationsensor":"Navigationmodule","CellularLTEmod":"Cellularmodule","Battery":"Batterymodule","BMSmodule":"BMSmoduledata","ActuatorDriverIC":"Actuatormodule","SensorArray":"Sensorarraymodule","Materials":"MaterialsSkin"}
Matching_component_list = {}
#>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>
country = [{name: 'Afghanistan', code: 'AF'}, 
  {name: 'Åland Islands', code: 'AX'}, 
  {name: 'Albania', code: 'AL'}, 
  {name: 'Algeria', code: 'DZ'}, 
  {name: 'American Samoa', code: 'AS'}, 
  {name: 'AndorrA', code: 'AD'}, 
  {name: 'Angola', code: 'AO'}, 
  {name: 'Anguilla', code: 'AI'}, 
  {name: 'Antarctica', code: 'AQ'}, 
  {name: 'Antigua and Barbuda', code: 'AG'}, 
  {name: 'Argentina', code: 'AR'}, 
  {name: 'Armenia', code: 'AM'}, 
  {name: 'Aruba', code: 'AW'}, 
  {name: 'Australia', code: 'AU'}, 
  {name: 'Austria', code: 'AT'}, 
  {name: 'Azerbaijan', code: 'AZ'}, 
  {name: 'Bahamas', code: 'BS'}, 
  {name: 'Bahrain', code: 'BH'}, 
  {name: 'Bangladesh', code: 'BD'}, 
  {name: 'Barbados', code: 'BB'}, 
  {name: 'Belarus', code: 'BY'}, 
  {name: 'Belgium', code: 'BE'}, 
  {name: 'Belize', code: 'BZ'}, 
  {name: 'Benin', code: 'BJ'}, 
  {name: 'Bermuda', code: 'BM'}, 
  {name: 'Bhutan', code: 'BT'}, 
  {name: 'Bolivia', code: 'BO'}, 
  {name: 'Bosnia and Herzegovina', code: 'BA'}, 
  {name: 'Botswana', code: 'BW'}, 
  {name: 'Bouvet Island', code: 'BV'}, 
  {name: 'Brazil', code: 'BR'}, 
  {name: 'British Indian Ocean Territory', code: 'IO'}, 
  {name: 'Brunei Darussalam', code: 'BN'}, 
  {name: 'Bulgaria', code: 'BG'}, 
  {name: 'Burkina Faso', code: 'BF'}, 
  {name: 'Burundi', code: 'BI'}, 
  {name: 'Cambodia', code: 'KH'}, 
  {name: 'Cameroon', code: 'CM'}, 
  {name: 'Canada', code: 'CA'}, 
  {name: 'Cape Verde', code: 'CV'}, 
  {name: 'Cayman Islands', code: 'KY'}, 
  {name: 'Central African Republic', code: 'CF'}, 
  {name: 'Chad', code: 'TD'}, 
  {name: 'Chile', code: 'CL'}, 
  {name: 'China', code: 'CN'}, 
  {name: 'Christmas Island', code: 'CX'}, 
  {name: 'Cocos (Keeling) Islands', code: 'CC'}, 
  {name: 'Colombia', code: 'CO'}, 
  {name: 'Comoros', code: 'KM'}, 
  {name: 'Congo', code: 'CG'}, 
  {name: 'Congo, The Democratic Republic of the', code: 'CD'}, 
  {name: 'Cook Islands', code: 'CK'}, 
  {name: 'Costa Rica', code: 'CR'}, 
  {name: 'Cote D\'Ivoire', code: 'CI'}, 
  {name: 'Croatia', code: 'HR'}, 
  {name: 'Cuba', code: 'CU'}, 
  {name: 'Cyprus', code: 'CY'}, 
  {name: 'Czech Republic', code: 'CZ'}, 
  {name: 'Denmark', code: 'DK'}, 
  {name: 'Djibouti', code: 'DJ'}, 
  {name: 'Dominica', code: 'DM'}, 
  {name: 'Dominican Republic', code: 'DO'}, 
  {name: 'Ecuador', code: 'EC'}, 
  {name: 'Egypt', code: 'EG'}, 
  {name: 'El Salvador', code: 'SV'}, 
  {name: 'Equatorial Guinea', code: 'GQ'}, 
  {name: 'Eritrea', code: 'ER'}, 
  {name: 'Estonia', code: 'EE'}, 
  {name: 'Ethiopia', code: 'ET'}, 
  {name: 'Falkland Islands (Malvinas)', code: 'FK'}, 
  {name: 'Faroe Islands', code: 'FO'}, 
  {name: 'Fiji', code: 'FJ'}, 
  {name: 'Finland', code: 'FI'}, 
  {name: 'France', code: 'FR'}, 
  {name: 'French Guiana', code: 'GF'}, 
  {name: 'French Polynesia', code: 'PF'}, 
  {name: 'French Southern Territories', code: 'TF'}, 
  {name: 'Gabon', code: 'GA'}, 
  {name: 'Gambia', code: 'GM'}, 
  {name: 'Georgia', code: 'GE'}, 
  {name: 'Germany', code: 'DE'}, 
  {name: 'Ghana', code: 'GH'}, 
  {name: 'Gibraltar', code: 'GI'}, 
  {name: 'Greece', code: 'GR'}, 
  {name: 'Greenland', code: 'GL'}, 
  {name: 'Grenada', code: 'GD'}, 
  {name: 'Guadeloupe', code: 'GP'}, 
  {name: 'Guam', code: 'GU'}, 
  {name: 'Guatemala', code: 'GT'}, 
  {name: 'Guernsey', code: 'GG'}, 
  {name: 'Guinea', code: 'GN'}, 
  {name: 'Guinea-Bissau', code: 'GW'}, 
  {name: 'Guyana', code: 'GY'}, 
  {name: 'Haiti', code: 'HT'}, 
  {name: 'Heard Island and Mcdonald Islands', code: 'HM'}, 
  {name: 'Holy See (Vatican City State)', code: 'VA'}, 
  {name: 'Honduras', code: 'HN'}, 
  {name: 'Hong Kong', code: 'HK'}, 
  {name: 'Hungary', code: 'HU'}, 
  {name: 'Iceland', code: 'IS'}, 
  {name: 'India', code: 'IN'}, 
  {name: 'Indonesia', code: 'ID'}, 
  {name: 'Iran, Islamic Republic Of', code: 'IR'}, 
  {name: 'Iraq', code: 'IQ'}, 
  {name: 'Ireland', code: 'IE'}, 
  {name: 'Isle of Man', code: 'IM'}, 
  {name: 'Israel', code: 'IL'}, 
  {name: 'Italy', code: 'IT'}, 
  {name: 'Jamaica', code: 'JM'}, 
  {name: 'Japan', code: 'JP'}, 
  {name: 'Jersey', code: 'JE'}, 
  {name: 'Jordan', code: 'JO'}, 
  {name: 'Kazakhstan', code: 'KZ'}, 
  {name: 'Kenya', code: 'KE'}, 
  {name: 'Kiribati', code: 'KI'}, 
  {name: 'Korea, Democratic People\'S Republic of', code: 'KP'}, 
  {name: 'Korea, Republic of', code: 'KR'}, 
  {name: 'Kuwait', code: 'KW'}, 
  {name: 'Kyrgyzstan', code: 'KG'}, 
  {name: 'Lao People\'S Democratic Republic', code: 'LA'}, 
  {name: 'Latvia', code: 'LV'}, 
  {name: 'Lebanon', code: 'LB'}, 
  {name: 'Lesotho', code: 'LS'}, 
  {name: 'Liberia', code: 'LR'}, 
  {name: 'Libyan Arab Jamahiriya', code: 'LY'}, 
  {name: 'Liechtenstein', code: 'LI'}, 
  {name: 'Lithuania', code: 'LT'}, 
  {name: 'Luxembourg', code: 'LU'}, 
  {name: 'Macao', code: 'MO'}, 
  {name: 'Macedonia, The Former Yugoslav Republic of', code: 'MK'}, 
  {name: 'Madagascar', code: 'MG'}, 
  {name: 'Malawi', code: 'MW'}, 
  {name: 'Malaysia', code: 'MY'}, 
  {name: 'Maldives', code: 'MV'}, 
  {name: 'Mali', code: 'ML'}, 
  {name: 'Malta', code: 'MT'}, 
  {name: 'Marshall Islands', code: 'MH'}, 
  {name: 'Martinique', code: 'MQ'}, 
  {name: 'Mauritania', code: 'MR'}, 
  {name: 'Mauritius', code: 'MU'}, 
  {name: 'Mayotte', code: 'YT'}, 
  {name: 'Mexico', code: 'MX'}, 
  {name: 'Micronesia, Federated States of', code: 'FM'}, 
  {name: 'Moldova, Republic of', code: 'MD'}, 
  {name: 'Monaco', code: 'MC'}, 
  {name: 'Mongolia', code: 'MN'}, 
  {name: 'Montserrat', code: 'MS'}, 
  {name: 'Morocco', code: 'MA'}, 
  {name: 'Mozambique', code: 'MZ'}, 
  {name: 'Myanmar', code: 'MM'}, 
  {name: 'Namibia', code: 'NA'}, 
  {name: 'Nauru', code: 'NR'}, 
  {name: 'Nepal', code: 'NP'}, 
  {name: 'Netherlands', code: 'NL'}, 
  {name: 'Netherlands Antilles', code: 'AN'}, 
  {name: 'New Caledonia', code: 'NC'}, 
  {name: 'New Zealand', code: 'NZ'}, 
  {name: 'Nicaragua', code: 'NI'}, 
  {name: 'Niger', code: 'NE'}, 
  {name: 'Nigeria', code: 'NG'}, 
  {name: 'Niue', code: 'NU'}, 
  {name: 'Norfolk Island', code: 'NF'}, 
  {name: 'Northern Mariana Islands', code: 'MP'}, 
  {name: 'Norway', code: 'NO'}, 
  {name: 'Oman', code: 'OM'}, 
  {name: 'Pakistan', code: 'PK'}, 
  {name: 'Palau', code: 'PW'}, 
  {name: 'Palestinian Territory, Occupied', code: 'PS'}, 
  {name: 'Panama', code: 'PA'}, 
  {name: 'Papua New Guinea', code: 'PG'}, 
  {name: 'Paraguay', code: 'PY'}, 
  {name: 'Peru', code: 'PE'}, 
  {name: 'Philippines', code: 'PH'}, 
  {name: 'Pitcairn', code: 'PN'}, 
  {name: 'Poland', code: 'PL'}, 
  {name: 'Portugal', code: 'PT'}, 
  {name: 'Puerto Rico', code: 'PR'}, 
  {name: 'Qatar', code: 'QA'}, 
  {name: 'Reunion', code: 'RE'}, 
  {name: 'Romania', code: 'RO'}, 
  {name: 'Russian Federation', code: 'RU'}, 
  {name: 'RWANDA', code: 'RW'}, 
  {name: 'Saint Helena', code: 'SH'}, 
  {name: 'Saint Kitts and Nevis', code: 'KN'}, 
  {name: 'Saint Lucia', code: 'LC'}, 
  {name: 'Saint Pierre and Miquelon', code: 'PM'}, 
  {name: 'Saint Vincent and the Grenadines', code: 'VC'}, 
  {name: 'Samoa', code: 'WS'}, 
  {name: 'San Marino', code: 'SM'}, 
  {name: 'Sao Tome and Principe', code: 'ST'}, 
  {name: 'Saudi Arabia', code: 'SA'}, 
  {name: 'Senegal', code: 'SN'}, 
  {name: 'Serbia and Montenegro', code: 'CS'}, 
  {name: 'Seychelles', code: 'SC'}, 
  {name: 'Sierra Leone', code: 'SL'}, 
  {name: 'Singapore', code: 'SG'}, 
  {name: 'Slovakia', code: 'SK'}, 
  {name: 'Slovenia', code: 'SI'}, 
  {name: 'Solomon Islands', code: 'SB'}, 
  {name: 'Somalia', code: 'SO'}, 
  {name: 'South Africa', code: 'ZA'}, 
  {name: 'South Georgia and the South Sandwich Islands', code: 'GS'}, 
  {name: 'Spain', code: 'ES'}, 
  {name: 'Sri Lanka', code: 'LK'}, 
  {name: 'Sudan', code: 'SD'}, 
  {name: 'Suriname', code: 'SR'}, 
  {name: 'Svalbard and Jan Mayen', code: 'SJ'}, 
  {name: 'Swaziland', code: 'SZ'}, 
  {name: 'Sweden', code: 'SE'}, 
  {name: 'Switzerland', code: 'CH'}, 
  {name: 'Syrian Arab Republic', code: 'SY'}, 
  {name: 'Taiwan, Province of China', code: 'TW'}, 
  {name: 'Tajikistan', code: 'TJ'}, 
  {name: 'Tanzania, United Republic of', code: 'TZ'}, 
  {name: 'Thailand', code: 'TH'}, 
  {name: 'Timor-Leste', code: 'TL'}, 
  {name: 'Togo', code: 'TG'}, 
  {name: 'Tokelau', code: 'TK'}, 
  {name: 'Tonga', code: 'TO'}, 
  {name: 'Trinidad and Tobago', code: 'TT'}, 
  {name: 'Tunisia', code: 'TN'}, 
  {name: 'Turkey', code: 'TR'}, 
  {name: 'Turkmenistan', code: 'TM'}, 
  {name: 'Turks and Caicos Islands', code: 'TC'}, 
  {name: 'Tuvalu', code: 'TV'}, 
  {name: 'Uganda', code: 'UG'}, 
  {name: 'Ukraine', code: 'UA'}, 
  {name: 'United Arab Emirates', code: 'AE'}, 
  {name: 'United Kingdom', code: 'GB'}, 
  {name: 'United States', code: 'US'}, 
  {name: 'United States Minor Outlying Islands', code: 'UM'}, 
  {name: 'Uruguay', code: 'UY'}, 
  {name: 'Uzbekistan', code: 'UZ'}, 
  {name: 'Vanuatu', code: 'VU'}, 
  {name: 'Venezuela', code: 'VE'}, 
  {name: 'Viet Nam', code: 'VN'}, 
  {name: 'Virgin Islands, British', code: 'VG'}, 
  {name: 'Virgin Islands, U.S.', code: 'VI'}, 
  {name: 'Wallis and Futuna', code: 'WF'}, 
  {name: 'Western Sahara', code: 'EH'}, 
  {name: 'Yemen', code: 'YE'}, 
  {name: 'Zambia', code: 'ZM'}, 
  {name: 'Zimbabwe', code: 'ZW'} 
]
selectedcountry = [] #Getting the selected country 
os_list = [' ','Linux Ubuntu x64 x86','Linux Debian x64 x86','Linux Ubuntu arm 32','Linux Debian arm 32','Linux Ubuntu arm 64','Linux Debian arm 64'] #The list of the operaring system on the system 
osmem = []
#Password = "Rkj3548123" #Find the way to popup and get the password using this part as login into the system 
os.system("echo Hello"+"\t"+str(username)) #Getting the host name 
parent_dir = "/Users/"+username+"/AppData/Local/Programs/" # Getting the robot node directory created inside the document as default directory  
directory = ["Wifi_devices_connects","Robotics_nodes_json"]
mode = 0o777
for dric in range(0,len(directory)):
   try:
      print("Now creating.....",str(directory[dric])) #Getting the directory created for the wifi config and robotics nodes json  
      path = os.path.join(parent_dir, directory[dric]) 
      os.mkdir(path,mode) #Make the path file for the wifi device connection data for choosing on the firmware devices generator
   except:
       print(directory[dric]+" directory  was created")
nodelist = os.listdir(os.path.join(parent_dir,directory[1]))  #getting the list of the robotics node json 
nodelist.append(" ")
storage_path = drives     
try:
 for re in range(0,len(storage_path)):
    generic_storage = os.listdir(storage_path[re]) #Getting the list of the storate path  
    generic_mem = []
    generic_mem.append(" ")
    generic_mem.append("Generic storage"+str(generic_storage[re]))
except:
  print("Storage devices not found") 
#>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>
#Getting the device name of the host 
devices = subprocess.check_output("arp -a",shell=True)
extract_devices = devices.decode('utf-8')
#print(extract_devices.split("wlo1"))
devices_list = extract_devices.split("wlo1")
hostname_mem = [] #Getting the list of the devices host name 
hostip_mem = [] #Getting the list of the devices host ip 
automateip_add = {}
hoste_selected =[]
host_password =[]
host_remote = [] #getting the remote host 
robothostname = []
#>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>
    #Getting the wifi of the host 
wifi_mem = []
wifi_password = []
#>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>
#UDP socket message receiver sensor connection between the robot systems 
Sensors_data = [] # getting the data from the sensor node numpy array 
global sensor_data_info, datasize
#>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>
    #Targetting command including firmware installation start and stop services and generate the config of the start at boot function 
command_exec = ["roboreactorfirmware.sh","./roboreactorfirmware.sh","sudo service supervisorctl start","sudo service supervisor stop","sudo supervisorctl reread","sudo service supervisor restart"]   #Command to activate the service automaticly and accessing the data inside the singleboard computer via ssh  
r = requests.get('https://raw.githubusercontent.com/KornbotDevUltimatorKraton/Firmwareoflaptop/main/FirmwareNongpuserver.sh')
firmware = requests.get('https://raw.githubusercontent.com/KornbotDevUltimatorKraton/Firmwareoflaptop/main/FirmwareNongpuserver.sh')
try:
  Create_file_storage = os.mkdir(storage_path+"/"+"Roboreactor",mode) #Current storage data # Creating the file inside the directory  
  Current_wifi_path = os.mkdir(storage_path+"/"+"Roboreactor"+"/"+"Wifi_scan",mode) #
except:
    print("File created inside the directory")
client_username = []
port_mem = []  # Getting the mem port to mem the data of the port that the computer going to connect  
host = 'local host'
port = 5000 # Getting the port  for the udp connection
#>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>
   # Getting the host name ip 
def get_Host_name_IP():  # Getting the host ip before scan inside the machine data 
    try: 
        host_name = socket.gethostname() 
        host_ip = socket.gethostbyname(host_name) 
        print("Hostname :  ",host_name) 
        print("IP : ",host_ip)
        print(str(host_ip)) 
        ip.append(str(host_ip)) # Getting the host ipv4 address 
        print("Host part ip "+str(host_ip).split(".")[2])
        Memhostpartip.append(str(host_ip).split(".")[2]) # Getting the host ip address of the system 
        if Memhostpartip != [] and ip != []:
            if len(Memhostpartip) and len(ip) >=2: 
               ip.remove(ip[0])  # remove the first ip scan data and getting the new one inside the list 
               Memhostpartip.remove(Memhostpartip[0]) #remove the host part ip from the list 
    except: 
        print("Unable to get Hostname and IP") 
#>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>
# Node advance function recall function by json from the webservices api 

class MainWindow2(QtWidgets.QMainWindow):
    def __init__(self):
        super(MainWindow2, self).__init__()
        self.setFixedSize(1028, 670)

        #Load the UI Page
        uic.loadUi('Roboticfirmwaregenerator.ui', self)
        self.setWindowTitle('Roboreactor firmware generator  User:'+"\t"+client_username[0]) #Getting the the client username from the new array
        p = self.palette()
        p.setColor(self.backgroundRole(), QtCore.Qt.darkGray)
        self.setPalette(p)
        #Adding the roboreactor firmware generator function right here 
        self.setPalette(p)
        oImage = QImage("bg2_new.jpeg")
        oImage.scaled(300,200)
        #sImage = oImage.scaled(QSize(300,200))                   # resize Image to widgets size
        palette = QPalette()
        palette.setBrush(QPalette.Window, QBrush(oImage))
        self.setPalette(palette)
        
        #>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>
        #Label pixmap camera 
        self.camera = self.findChild(QLabel,"label_5") # Getting this label to display the pixmap data 
        self.camera.setFixedSize(751,551) # Setting the size of the display image 
        #self.camera.setFixedSize(340,350) 
        #>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>
        self.pushButton.clicked.connect(self.Writeimage)
        self.pushButton_2.clicked.connect(self.Remoteconfig) #Autore mote config 
        self.pushButton_3.clicked.connect(self.Start_remote_robot) #Start remote robot  
        self.pushButton_4.clicked.connect(self.Stop_remote_robot)  #Stop remote robot 
        self.pushButton_5.clicked.connect(self.Scan_host_machine) #Scan robot host
        self.pushButton_6.clicked.connect(self.Scan_wifi) #Scan wifi 
        self.pushButton_7.clicked.connect(self.Logout) #Logout function to setting the new login 
        self.pushButton_8.clicked.connect(self.Visual1) # Getting the camera 1 connect to open visual data on udp 
        self.pushButton_9.clicked.connect(self.Restart_services) 
        self.pushButton_10.clicked.connect(self.Analyze_sensors) #Analyse the recorded sensor from the testing data on the hardware 
        #>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>
        # Adding layout for the nodes display to configure the robot code 
        #Nodes view will display the data of the nodes from the json file input from the json downloaded from the website roboreactor online with the account data connected via the api 
        #1 Making the node flow chart plot from the flowchart 
        self.gridLayout = self.findChild(QGridLayout,"gridLayout") # Setting the grid layout for flowchart control 
        #>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>
        #self.labelcam = self.findChild(QLabel,'label_5')
              #Set of commbobox selection function 

        self.combo1 = self.findChild(QComboBox, "comboBox")
        self.combo2 = self.findChild(QComboBox,"comboBox_2")
        self.combo3 = self.findChild(QComboBox,"comboBox_3")
        self.combo4 = self.findChild(QComboBox, "comboBox_4")
        self.combo5 = self.findChild(QComboBox,"comboBox_5")
        self.combo7 = self.findChild(QComboBox,"comboBox_7")

              #Text combonent 
        self.text6= self.findChild(QTextEdit,"textEdit_6")  #using the text edit 1 input the ssh text input  
        self.text3 = self.findChild(QLineEdit,"lineEdit_2")  #using the text edit 3 input the password of the host target 
        self.text3.setEchoMode(QLineEdit.Password) # Setting the qline edit for password mode 
        self.text4 = self.findChild(QLineEdit,"lineEdit")  #using the text edit 4 input the wifi password 
        self.text4.setEchoMode(QLineEdit.Password) # Setting the qline edit for password mode 
        self.text5 = self.findChild(QTextEdit,"textEdit_5")  #using the text edit 5 input the robot host hame 
             #Tab widget 
        self.tabwidget = self.findChild(QTabWidget,'tabWidget')  #using the TabWidget for the tab change the function
        self.cameras = self.findChild(QWidget,'Camera') #Getting the camera input mode 
        self.nodes_robot = self.findChild(QWidget,'nodes') #Getting the nodes input mode for nodes view data 
        
        #self.labelcam.setText("This is the first tab")
        #self.cameras.layout.addLayout(self.labelcam)
        #self.cameras.setLayout(self.cameras.layout)
        #self.tabWidget.addTab(,"Camera")
              #progressbard function   
        #self.progress = self.findChild(QProgressBar,'progressBar') #using progress bar 
        #self.progress.setMinimum(0)
        #Getting the maximum value input in dyanmics variant from the process feedback from the socket api communicate with the robotics host 
        #self.progress.setMaximum(100) #Getting the number of the maximum value
        #self.progress.setValue(0) #Move this progressbar into the function of the rest api feedback 
        #>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>
            #Action combolist function 
        self.combo1.activated.connect(self.Operatingsystem)
        self.combo1.addItems(os_list)
        self.combo2.activated.connect(self.Storage_generic)
        try:
           print("Access external storage devices")
           self.combo2.addItems(generic_mem)
        except:
           print("")
        self.combo3.activated.connect(self.robotnodes)
        self.combo3.addItems([" "])
        self.combo3.addItems(nodelist) #Getting the robotics node json file 
        self.combo5.activated.connect(self.countrychoose)  #Getting the data from the list dictionary countr to display on the combobox 
        
       
        print(host_password,wifi_password,robothostname)
        for countries in range(0,len(country)):
                       print(country[countries])
                       dict_cc[country[countries].get('name')] = country[countries].get('code')
        print(dict_cc)
        self.combo5.addItems(list(dict_cc))  #Adding the country into the list item of the combobox
        self.combo4.activated.connect(self.hostname_data)
        """
        print("Start scanning the host machine") #
        lst = map_network()
        print(lst)
        try:
              #automateip_add.clear()
              for r in range(0,len(lst)):
                   host = socket.gethostbyaddr(lst[r])
                   print(host[0],host[2])
                   automateip_add[host[0]] = host[2] #create the new list of the host scanner  
                   #Fixed the unscannable issue now able to scanning at instance scanning mode 
        except:
               print("Unknown host")
        for ri in range(0,len(devices_list)-1):
            print(devices_list[ri].split(" "))
            origin_list = devices_list[ri].split(" ")[0]
            getdatahost = devices_list[ri].split(" ")[1]
            gethostip = getdatahost.split("(")[1].split(")")[0]
            print(origin_list,getdatahost.split("(")[1].split(")")[0])
            hostname_mem.append(origin_list) #Get the hostname of the devices 
            automateip_add[origin_list] = gethostip #Getting the autolist of the ip address  #Create the automate list update 
        """
        #>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>
          # Window mode host ip scanner
        get_Host_name_IP() # Getting the host name ip data and collect the hostpartip 
        #>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>
        # Getting the IP range 
        for i in range(0,256): 
                 #os.system("nslookup 192.168."+str(Memhostpartip[0])+"."+str(i)) # Running loop ip address from the data of the local ip first scan         
                 checkip_data = subprocess.check_output("nslookup 192.168."+str(Memhostpartip[0])+"."+str(i),shell=True) # Getting the ouput from the command to processing in the data host ip scan 
                 print(checkip_data.decode().split(" ")) 
                 gettingdata  = checkip_data.decode().split(" ") 
                 if len(gettingdata) > 6:
                    print("Detect the devices connected to the network")
                    print(gettingdata[0],gettingdata[2].split("\r\n"),gettingdata[4].split("\r\n"),gettingdata[8].split("\r\n"),gettingdata[10].split("\r\n")) # Getting the gateway router name        
                    print("Host detected: ",gettingdata[8].split("\r\n"),gettingdata[10].split("\r\n"))
                    hostip_mem.append(gettingdata[8].split("\r\n")[0])
                    automateip_add[gettingdata[8].split("\r\n")[0]] = gettingdata[10].split("\r\n")[0] #Getting the host name and ip address ipv4 adress of devices 
                    time.sleep(0.05) # Getting the time sleep to protect DNS time out

    


        self.combo4.addItems(automateip_add.keys())#Getting the host mem data into the combo box  
        #self.combo6.addItems(hostip_mem) #Getting the ip address of the host target selected
        print(automateip_add)
        self.combo7.activated.connect(self.wifissid)
        #Change this part of the code to support window operating system 
        """
        for wifi_R in range(0,1):
                     getwifi = subprocess.check_output("nmcli dev wifi",shell=True) 
                     dataframe = getwifi.decode('utf-8')
                     #print(type(dataframe))
                     #print(dataframe)
                     file = open("currentwifi.csv",'w')
                     file.write(dataframe)
                     file.close()
                     #df = pandas.DataFrame(dataframe, columns=['SSID', 'SIGNAL'])
                     df = pd.read_csv('currentwifi.csv')
                     #print("Reading the saving current available wifi")
                     print(df)
                     index = df.index
                     print(index)
                     listdata = list(df.columns.values)
                     print(listdata)
                     print(listdata[0].split(" ")) #recreate the columns separate from one big column
                     print(df[listdata[0]].values[0])
                     print(len(index))
                     for wifi in range(0,len(index)-1):
                             getting_str =  df[listdata[0]].values[wifi].split(" ") #split the wifi data to get the wifi name and signal strength to choosing the best connection 
                             print(getting_str[10])
                             if len(wifi_mem) < len(index):
                                           wifi_mem.append(getting_str[10]) #getting the mem wifi name 
                             if len(wifi_mem) > len(index):
                                   terminal = len(wifi_mem)-len(index)
                                   for wifilist in range(len(index),terminal):
                                             wifi_mem.remove(wifi_mem[wifilist]) #remove the len of the index if the length is over 
        """
       
        wifi = pywifi.PyWiFi()
        iface = wifi.interfaces()[0]
        iface.scan()
        time.sleep(0.5)
        results = iface.scan_results()
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
                     self.combo7.addItems([" "]) #Getting the blank list on the top to be able to choosing the data in the combobox later 
                     self.combo7.addItems(list(wifidict)) #getting the list of wifi memory
                     print(list(wifidict))
        
       

    def Visual1(self): 
           # Camerafunction for the UDP receiver communication       
           #UDP socket client
           print("Connecting the ip camera")
           self.Worker1 = Worker1() 
           self.Worker1.start()
           self.Worker1.ImageUpdate.connect(self.ImageUpdateSlot)
    def ImageUpdateSlot(self, Image):
            self.pixmap = QPixmap.fromImage(Image)
            self.camera.setPixmap(self.pixmap) 
    def wifissid(self,wifi_index):
             print(list(wifidict)[wifi_index])
             if len(network_name) < len(list(wifidict)):
                   network_name.append(list(wifidict)[wifi_index-1])  #Getting the wifi mem on the list of the network name to generate the wifi configuretion on sd card 
             if len(network_name) >1:
                   network_name.remove(network_name[0]) #remove the network name from the list if out of range 
             print(network_name)      
    def hostip_data(self,hostip_index):
         try: 
             print(automateip_add.keys()[hostip_index-1])
         except: 
             print("Host scan ip cannot be using on the window operating system")    
    def hostname_data(self,host_index):
             print(host_index)
             #print(automateip_add.values()[host_index]) #Getting the host index
             print(automateip_add.get(list(automateip_add)[host_index])) 
             
             if str(automateip_add.get(list(automateip_add)[host_index])) not in list(automateip_add):
                       hostip_mem.append(automateip_add.get(list(automateip_add)[host_index]))
                       print(hostip_mem)
             if len(automateip_add.keys()) > 1:
                       hostip_mem.remove(hostip_mem[0])
             
    def Storage_generic(self,index_storage):
                print(generic_mem[index_storage])
    def robotnodes(self,nodes_list):
        print(nodelist[nodes_list]) 
        print("Start generate node components data")
        # Connect the node using the data structures algorithm 
        #assert os.path.isfile(parent_dir+"Robotics_nodes_json"+"/"+nodelist[nodes_list])
        f = open(parent_dir+"Robotics_nodes_json"+"/"+nodelist[nodes_list])
        # returns JSON object as
        # a dictionary
        data_components = json.load(f) # Getting the component list from the json file on the website    
        
        fc = Flowchart(terminals={
            'GPIO_2': {'io': 'in'},
            'Sensor1': {'io': 'out'}    
        })
        
        w = fc.widget() 
        self.gridLayout.addWidget(fc.widget(), 0, 0, 2, 1)


    def Operatingsystem(self,osp):
             print(os_list[osp])
             if osmem !=[]:
                   osmem.append(os_list[osp])
             if len(osmem) > 1:
                  osmem.remove(osmem[len(osmem)-1]) 
             print(osmem)    
    def countrychoose(self,countries_cc):
                 #Getting the breviation from key
              try:
                 print(list(dict_cc)[countries_cc])
                 get_extracted = list(dict_cc)[countries_cc]
                 selected_cc = dict_cc.get(get_extracted)
                 print(selected_cc)
                 selectedcountry.append(selected_cc) #Getting the country breviation for the memory function              
                 print("Store country breviation successfully....")
              except: 
                   print("Store country breviation error")
    def Remoteconfig(self):
       print("Operating remote config on the robot......") #Operating the remote config of the robot
       if len(robothostname) <=0:
                    robothostname.append(self.text5.toPlainText()) #Robot hostname for the remote operating robot auto configuretion and setting service 
       if len(robothostname) >1:
                    robothostname.remove(robothostname[0])
       if len(host_password) <=0:
                 host_password.append(self.text3.text()) #Host password for the ssh remote 
       if len(host_password) >1:
                 host_password.remove(host_password[0])
       try:     
           print(robothostname[0],hostip_mem[0],host_password[0])          
           with SSHClient() as client:
                     client.set_missing_host_key_policy(AutoAddPolicy())
                     print(robothostname)
                     print(hostip_mem[0],robothostname[0],host_password[0])
                     client.connect(hostname=str(hostip_mem[0]),username=str(robothostname[0]),password=str(host_password[0]),look_for_keys=False) #Getting all the data from the host ip,host_name and the other hostmachine to connect 
                     command = ["ls","python3 wifiscanner.py","lsusb"]
                     #Access remote command with sodo combine password generated working 
                     #Fix your host password into the remote machine password
                     try:
                         print("Remote chmod permission")
                         stdin, stdout, stderr = client.exec_command("sudo -S <<< " +str(host_password[0])+" chmod +x "+command_exec[0],get_pty=True)
                         lines = stdout.readlines()
                         print(lines)
                         #Messagebox here to display the progress bar 
                        
                         msgbox = QtWidgets.QMessageBox()
                         msgbox.setText('Finish robogenerator firmware generated')
                         msgbox.setTextInteractionFlags(QtCore.Qt.NoTextInteraction) # (QtCore.Qt.TextSelectableByMouse)
                         stdin, stdout, stderr = client.exec_command(command[0],get_pty=True)
                         lines = stdout.readlines()
                         for dataremote in range(0,len(lines)):   
                              msgbox.setDetailedText(lines[dataremote]+"\n")
                         msgbox.exec() 
                         #From the lines output list array seeking the cannot access as the trigger word for git installation on the system to prepare the remote firmware installation process 
                         #Reding the bash script in the list array to modify the firmware percentage report firmware installation progress 
                         
                     except:
                         print("Remote chmod permission fail")
                     
       except: 
            print("You haven't upload firmware and config to the SD card")
    def Analyze_sensors(self): 
      try:
        
        print("Start generate node components data")
        Classification_components_func(username) # Getting the classification mode to working on the code uploader writer on the ssh 
        # Connect the node using the data structures algorithm 
        #f = open('data.json')
        # returns JSON object as
        # a dictionary
        #data_components = json.load(f) # Getting the component list from the json file on the website    
        k = 4         
        
        fc = Flowchart(terminals={      
            'dataIn':{'io':'in'},
            'dataOut':{'io':'out'}
        })
        win = QtGui.QMainWindow() 
        win.setWindowTitle('Robot nodes flowchart')
        w = fc.widget() 
        self.gridLayout.addWidget(fc.widget(), 0, 0, 2, 1)
        #v1 = pg.ImageView() 
        #v2 = pg.ImageView()
        datacomponents = Classification_components_func(username)
        if Classified_list_components !=[]: 
                Classified_list_components.clear()
        for rt in range(0,len(list(datacomponents))):
                 if list(datacomponents)[rt].split(',')[0] in components: 
                            print("Found components: ",list(datacomponents)[rt].split(',')[0]) # Getting the topic of the component list                             
                            Matching_component_list[list(datacomponents)[rt].split(",")[0]+"_"+str(rt)] = list(datacomponents)[rt] # Getting the dictionary data  
                            Classified_list_components.append(list(datacomponents)[rt].split(',')[0])
        
        print("Components found: ",len(Classified_list_components)) #Getting the list of the classified component 
       
        for re in range(0,len(Classified_list_components)):  # Getting the len from the code to running in the case of the function here 
           # Running to get list function of visualization base on the name of the devices search in side the list of the for loop 
           #ImageView = pg.plotWidget
           #print(Matching_component_list)# Getting the dictionary list if the components 
           #print(list(Matching_component_list)) # Getting the name of the component and get the list info of the component name to classify data of the components gpio efficientcy and functionality
           #print(list(Matching_component_list.values()))
           #Get_components  = Matching_component_list.get(list(Matching_component_list)[re])
           print("Components name and amount: ", datacomponents.get(list(Matching_component_list.values())[re]))  #Getting the component name and list data of the component 
           
           exec("v"+str(re)+"="+"pg."+"ImageView"+"()")  # pg. and follow by the function of the components display of specification 
           if re%2 == 0:
               exec("self.gridLayout.addWidget(v"+str(re)+","+str(re)+", "+str(re%2+1)+")")
           if re%2 == 1: 
               exec("self.gridLayout.addWidget(v"+str(re)+","+str(re-1)+", "+str(re%2+1)+")")
        
        #Modification node type area 
        library = fclib.LIBRARY.copy() # start with the default node set
        library.addNodeType(Computeronboard,[('Display',)]) 
        library.addNodeType(Board,[('Display,')])
        library.addNodeType(CellularLTEmod,[('Display',)])
        library.addNodeType(ActuatorDriverIC,[('Display',)])
        library.addNodeType(Imagesensor,[('Display',)])
        library.addNodeType(BMSmodule,[('Display',)])
        library.addNodeType(Battery,[('Display',)])
        library.addNodeType(SensorArray,[('Display',)])
        library.addNodeType(Materials,[('Display',)])
        library.addNodeType(Acousticamplifier,[('Display',)])
        library.addNodeType(Navigationsensor,[('Display',)])

        fc.setLibrary(library)
       
        #v1Node = fc.createNode('Computernode', pos=(100, -150)) 
        #v1Node.setView(v1)
        #v2Node = fc.createNode('Boarddata', pos=(150, -150)) 
        #v2Node.setView(v2)      
        #v3Node = fc.createNode('Cellularmodule', pos=(50,-150))
        
        #v4Node = fc.createNode(listcommatch.get(Classified_list_components[15]), pos=(70,-120))

        #v5Node = fc.createNode(listcommatch.get(Classified_list_components[0]),pos=(100,-150))
        posparameter = k*len(Classified_list_components)
        if len(Classified_list_components) == 1: 
            for rww in range(0,len(Classified_list_components)):

                     print(Classified_list_components[rww],listcommatch.get(Classified_list_components[rww]))
                     #if rww  == len(Classified_list_components)-1:
                     number_list = random.sample(range(-150-posparameter,150+posparameter),len(Classified_list_components))
                     #if rww%2 == 1: 
                     #if rww <= len(Classified_list_components):  
                     vNode = fc.createNode(listcommatch.get(Classified_list_components[rww]),pos=(number_list[0],number_list[1]))  
        
        if len(Classified_list_components) > 1:
           for rww in range(0,len(Classified_list_components)):
                     print(Classified_list_components[rww],listcommatch.get(Classified_list_components[rww]))
                     #if rww  == len(Classified_list_components)-1:
                     number_list = random.sample(range(-150-posparameter,150+posparameter),len(Classified_list_components))
                     #if rww%2 == 1: 
                     #if rww <= len(Classified_list_components):  
                     vNode = fc.createNode(listcommatch.get(Classified_list_components[rww]),pos=(number_list[0],number_list[1]))
           # Generate the flow chart connector function 
           # Getting the function of the flow chart connection to running the programming loop and generate code for client software 
           # Setting the complete prototyping code to be ready for launch        
                      
                     #vNode2 = fc.createNode(listcommatch.get(Classified_list_components[rww+1]),pos=(number_list[2],number_list[3])) 
                     #print("v5Node = fc.createNode("+"'"+listcommatch.get(Classified_list_components[rww])+"'"+",pos=(100,-150)")   
                     #print(list(listcommatch)[rww],listcommatch.get(Classified_list_components[rww])) # Getting the data of nodes 
        #print(len(list(Classification_components_func(username))))

        #Using python exec to running the whole function for generate node here 
        
        #pw1 = pg.PlotWidget()
        #pw2 = pg.PlotWidget()
        #self.gridLayout.addWidget(pw1, 0, 1)
        #self.gridLayout.addWidget(pw2, 1, 1)
        # Inthe real function using the data recoded in array to using with the function of the system 
        #Request api data from the existing host machine selected from the gui to get the sesor hardware detected and value information 
        
        #datasize = 100
        #data = np.random.normal(size=datasize) # Getting the data input from the sensor api list input and magnage pattern like pyqtgraphflowchart example 
        #>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>
        #UDP socket programming function to get the message from the sensor
        #s = socket.socket(socket.AF_INET,socket.SOCK_STREAM) # udp socket 
        #s.connect((hostip_mem[0],port)) # Connect to certain machine ip and the port 
        #msg = s.recv(1024) # Receive byte of data 
        
        #>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>
        """
        for i  in range(1,101):
            data = requests.get("http://"+hostip_mem[0]+':5000') # Getting the data requests from the http api 
            print(data.text) 
            print(type(data.text))
            jsondata = json.loads(data.text)
            print(jsondata,len(jsondata.get('sensorinfo')))   # Getting the topic for specific sensor from the json key 
            #print(jsondata.get('components').get('sensorinfo').get('sensordata')) # Getting the sensor info nefore getting the sensor value 
            sensor_data_info = np.array(jsondata.get('sensorinfo'))
            datasize = len(jsondata.get('sensorinfo'))
            if datasize == len(sensor_data_info):
                print("Datasize matched!")
            sensor_data_info[200:300] += 1
            #data += np.sin(np.linspace(0, 100, 100))
            print(sensor_data_info)
            #plotList = {'Top Plot': pw1, 'Bottom Plot': pw2}
            sensor_data = metaarray.MetaArray(sensor_data_info, info=[{'name': 'Time', 'values': np.linspace(0, 0.1, len(sensor_data_info))}, {}])
        """    

        """
        ## Feed data into the input terminal of the flowchart
        #fc.setInput(dataIn=sensor_data)
        #plotList = {'Top Plot': pw1, 'Bottom Plot': pw2}
        #pw1Node = fc.createNode('PlotWidget', pos=(0, -150))
        #pw1Node.setPlotList(plotList)
        #pw1Node.setPlot(pw1)
        #pw2Node = fc.createNode('PlotWidget', pos=(150, -150))
        #pw2Node.setPlot(pw2)
        #pw2Node.setPlotList(plotList)
        #fNode = fc.createNode('GaussianFilter', pos=(0, 0))
        #fNode.ctrls['sigma'].setValue(5) # Spin box value increment control gaussian parameters
        #fc.connectTerminals(fc['dataIn'], fNode['In'])
        #fc.connectTerminals(fc['dataIn'], pw1Node['In'])
        #fc.connectTerminals(fNode['Out'], pw2Node['In'])
        #fc.connectTerminals(fNode['Out'], fc['dataOut'])
        #s.close() # Close the socket connection function 
        """
      except: 
          print("host machine ip "+hostip_mem[0]+':5000')
          print("Host mechine may not config firmware to report sensors data") # Getting the udp connection between the sensor data     
    
    def Scan_wifi(self): #Button input function for the wifi scanning 
           #Input the 1 loop wifi scanner here to operating at search mode 
        print('Mapping wifi") #Start mapping wifi')  
        wifi = pywifi.PyWiFi()
        iface = wifi.interfaces()[0]
        iface.scan()
        time.sleep(0.5)
        results = iface.scan_results()
        for er in range(0,3):
          for i in results:
             bssid = i.bssid
             ssid  = i.ssid
             #print(f"{bssid}: {ssid}")
             #print(ssid)
             wifidict[ssid] = bssid
             
        print(wifidict)
        
                    
        #self.progress.setValue((wifi/(len(wifi_mem)-1))*100) # Testing the progressbar using the scanning process of the wifi 
    def Start_remote_robot(self): 
           #Start the service robot to operating at boot 
        print("Start service robot to operating at boot services") # Start running the robot software 
        print("Sending the activate ip port")
        """
        axis = gl.GLAxisItem()
        g = gl.GLGridItem()
        g.scale(10, 10, 0.5) # Change the scale of the grid 
        self.openGLWidget.addItem(g)  # Adding the grid size 
        self.openGLWidget.addItem(axis) # Adding the axis 
        data = np.fromfunction(psi, (100,100,200))
        positive = np.log(np.clip(data, 0, data.max())**2)
        negative = np.log(np.clip(-data, 0, -data.min())**2)
        d2 = np.empty(data.shape + (4,), dtype=np.ubyte)
        d2[..., 0] = positive * (255./positive.max())
        d2[..., 1] = negative * (255./negative.max())
        d2[..., 2] = d2[...,1]
        d2[..., 3] = d2[..., 0]*0.3 + d2[..., 1]*0.3
        d2[..., 3] = (d2[..., 3].astype(float) / 255.) **2 * 255
        d2[:, 0, 0] = [255,0,0,100]
        d2[0, :, 0] = [0,255,0,100]
        d2[0, 0, :] = [0,0,255,100]
        v = gl.GLVolumeItem(d2)
        v.translate(-50,-50,-100)
        self.openGLWidget.addItem(v)
        ax = gl.GLAxisItem()
        self.openGLWidget.addItem(ax)
        """
    def Restart_services(self): 
           print("Restart service robot operating at boot services") # Restart the robot software 
    def Stop_remote_robot(self):
           #Stop the service robot to operating at boot 
           print("Stop service robot to operating at boot services") # Stop running the robot software 
    def Scan_host_machine(self):
           #Scan the hostmachine 
        print("Start scanning the host machine") #
        '''
        lst = map_network()
        print(lst)
        try:
              #automateip_add.clear()
              for r in range(0,len(lst)):
                   host = socket.gethostbyaddr(lst[r])
                   print(host[0],host[2])
                   automateip_add[host[0]] = host[2] #create the new list of the host scanner  
                   #Fixed the unscannable issue now able to scanning at instance scanning mode 
        except:
               print("Unknown host")
        '''
        #get_Host_name_IP() # Getting the host name ip data and collect the hostpartip 
        #>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>
        # Getting the IP range 
        for i in range(0,256): 
                 #dataout = subprocess.check_output("nslookup 192.168."+str(Memhostpartip[0])+"."+str(i)) # Running loop ip address from the data of the local ip first scan         
                 checkip_data = subprocess.check_output("nslookup 192.168."+str(Memhostpartip[0])+"."+str(i),shell=True) # Getting the ouput from the command to processing in the data host ip scan 
                 print(checkip_data.decode().split(" ")) 
                 gettingdata  = checkip_data.decode().split(" ") 
                 if len(gettingdata) > 6:
                    print("Detect the devices connected to the network")
                    print(gettingdata[0],gettingdata[2].split("\r\n"),gettingdata[4].split("\r\n"),gettingdata[8].split("\r\n"),gettingdata[10].split("\r\n")) # Getting the gateway router name        
                    print("Host detected: ",gettingdata[8].split("\r\n"),gettingdata[10].split("\r\n"))
                    hostip_mem.append(gettingdata[8].split("\r\n")[0])
                    automateip_add[gettingdata[8].split("\r\n")[0]] = gettingdata[10].split("\r\n")[0] #Getting the host name and ip address ipv4 adress of devices 
                    time.sleep(0.02) # Getting the time sleep to protect DNS time out
                    print(automateip_add)
    def Logout(self):
          print("Logging out from the system")
          self.w = MainWindow()
          self.w.show() 
          self.hide() 
    def Writeimage(self):
           
            if len(wifi_password) <=0:
                     wifi_password.append(self.text4.toPlainText()) #Network password for the wifi config session
            if len(wifi_password) >1:
                     wifi_password.remove(wifi_password[0]) #remove the first password from the list

            print(host_password,wifi_password)
            if memwrite ==[]:
                    memwrite.append("Write") #Getting the status write 
            if len(memwrite) >1:
                   memwrite.remove(memwrite[len(memwrite)]) #remove the memwrite with over lenght status writing on the array 
            print("Start writing the firmware on boot........") #Display the status on the logo 
            #>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>
                 #Start writing the firmware
                 #Selecte case of the operating system to upload the firmware into the 
            #This will be using the list combobox to select the SBC type tp choosing the image writer selection capability 
            #Accessing the boot directory of the raspberrypi_boot directory   
            target_rpi = ["boot","rootfs","/home/pi","system-boot","writable"]   #Getting the into the directory of the inner file 
            #Checking there is boot  
            list_seek_boot = os.listdir(PATH_SD_CARD) #Seeking the target file 
            print("Seek dir",list_seek_boot) #Getting the list seek boot 
            print(network_name[0])
            print(wifi_password[0])
            for re in range(0,len(list_seek_boot)):
                                      #Single Board computer will be choosing from the existing nodes json data to choosing the data from the websize api connecting with the back end    
                                      #Raspberrypi 
                                      # Write on the rpi debian function  condition                       
                                      if list_seek_boot[re] == str(target_rpi[1]):
                                                  print("Found "+str(list_seek_boot[re])+" Now operating firmware injection.......")
                                                  bashwriter = open(PATH_SD_CARD+"/"+list_seek_boot[re]+target_rpi[2]+"/"+"roboreactorfirmware.sh",'w') #Write the firmware directly into the SD card host
                                                  bashwriter.write(r.text) #Getting data inject into the sd card write directly into the user directory and create the file 
                                                  bashwriter.close() 
                                                  #os.system("sudo -S <<< "+str(host_password[0]) +" chmod +x "+PATH_SD_CARD+"/"+list_seek_boot[re]+target_rpi[2]+"/"+"roboreactorfirmware.sh")
                                      if list_seek_boot[re] == str(target_rpi[0]):
                                                  print("Found "+str(list_seek_boot[re])+" Now operating setting SSH and WiFi.......")
                                                  #Writing the file into the path
                                                  filessh = open(PATH_SD_CARD+"/"+list_seek_boot[re]+"/"+"ssh","w")  #Write the ssh file into the boot directory
                                                  #>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>
                                                  filessh.write(" ")
                                                  filessh.close() #Close the file writer after finish writing the file ssh for enable ssh command 

                                                  #>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>
                                                  filewpa_supplicant = open(PATH_SD_CARD+"/"+list_seek_boot[re]+"/"+"wpa_supplicant.conf",'w')
                                                  #>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>> 
                                                  print(selectedcountry)
                                                  filewpa_supplicant.write("country="+selectedcountry[0]+"\n") #Getting the country
                                                  filewpa_supplicant.write("ctrl_interface=DIR=/var/run/wpa_supplicant GROUP=netdev"+"\n")
                                                  filewpa_supplicant.write("update_config=1"+"\n")
                                                  filewpa_supplicant.write("network={"+"\n")
                                                  SSIDs = '"' + network_name[0] +'"'
                                                  SIDpass = '"' + wifi_password[0] + '"'
                                                  filewpa_supplicant.write("ssid="+SSIDs+"\n")  #Getting the name of the network from the combobox list SSID password
                                                  filewpa_supplicant.write("psk="+SIDpass+"\n") #Getting the password from the text input 
                                                  filewpa_supplicant.write("key_mgmt=WPA-PSK"+"\n") #Getting key wpa 
                                                  filewpa_supplicant.write("}"+"\n")  
                                                  filewpa_supplicant.close()
                                                  #>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>
                                                  #Fix the cmd code 
                                                  cmdfileconfig = open(PATH_SD_CARD+"/"+list_seek_boot[re]+"/"+"cmdline.txt",'w') 
                                                  cmdfileconfig.write("root=PARTUUID=f4481065-02 rootfstype=ext4 elevator=deadline fsck.repair=yes rootwait quiet init=/usr/lib/raspi-config/init_resize.sh splash plymouth.ignore-serial-consoles") 
                                                  cmdfileconfig.close() #Close file after finished writing the configuretion 
                                                  #>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>
                                                  #Fix the config boot 
                                                  configfile = open(PATH_SD_CARD+"/"+list_seek_boot[re]+"/"+"config.txt",'w') 
                                                  configfile.write("#Uncomment some or all of these to enable the optional hardware interfaces")
                                                  configfile.write("dtparam=i2c_arm=on"+"\n")
                                                  configfile.write("#dtparam=i2s=on"+"\n")
                                                  configfile.write("dtparam=spi=on"+"\n")
                                                  configfile.write("dtparam=audio=on"+"\n")
                                                  configfile.write("[pi4]"+"\n")
                                                  configfile.write("#Enable DRM VC4 V3D driver on top of the dispmanx display stack"+"\n")
                                                  configfile.write("dtoverlay=vc4-fkms-v3d"+"\n")
                                                  configfile.write("max_framebuffers=2"+"\n")
                                                  configfile.write("[all]"+"\n")
                                                  configfile.write("#dtoverlay=vc4-fkms-v3d"+"\n")
                                                  configfile.write("start_x=1"+"\n")
                                                  configfile.write("gpu_mem=128"+"\n")
                                                  configfile.write("enable_uart=1"+"\n")
                                                  configfile.close() #Close the file writer after finish writing 

                                                  #>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>
                                    
                                      #Write on the rpi ubuntu function condition 
                                      if list_seek_boot[re] == str(target_rpi[3]):                                
                                                   print("system-boot",list_seek_boot[re]) #getting the system boot 
                                                   

                                      if list_seek_boot[re] == str(target_rpi[4]):
                                                   print("writable",list_seek_boot[re]) #getting the system writable directory to inject the firmware on the system to run 
                                      

def Classification_components_func(username): 
    f = open("C:/Users/"+username+"/AppData/Local/Programs/Robotics_nodes_json/codeconfiggen.json") # Getting the code config gen json to running on the code system 
    
    datacom = json.load(f)
    print(datacom)
    Check_found_components = [] # Get the found components data inside the list
    Concatinate_components = [] # Getting the data of component in list together 
    # list of buyable part components data 
    # *Board = microcontroller spec and specification data these data will be extracted from the pins output from the pdf file 
    components = ['Imagesensor','Board','Computeronboard','ActuatorDriverIC','CellularLTEmodule','SensorArray','Navigationsensor','AmplifiermoduleIC','Battery','BMSmodule'] # Getting the components  
    # list of the function on the software data 
    Software_data = ['Objectdetection','Objectrecognition','Facerecognition','Posedetection','Poserecognition'] # Getting the data of software camera detection components 
    #list of the communication type data
    communication_component = ['Serial-baudrate','CANBUS-baudrate']
    for ire in range(0,len(datacom)): 
        print(datacom[ire]) # Getting the ire 
        if len(datacom[ire]) == 2: 
                dict_components[datacom[ire][0]] = datacom[ire][1] 
        if len(datacom[ire]) >2: 
                 getsplit_com = datacom[ire].split(":")
                 top_dat = datacom[ire][0]
                 dict_components[getsplit_com[0]] = getsplit_com[1] 
    print(dict_components) 
    print(list(dict_components)) # Getting the list key for the topic classification 
    for ir in list(dict_components): 
         #print("Components",ir) # Getting the string header function to running inside the conditioning status control 
         if ir.split(",")[0] in components: 
                    print("Found the components",ir.split(",")[0])
    for rex in list(dict_components): 
         #print("Components",dict_components.get(rex))
         Concatinate_components.append(rex+","+dict_components.get(rex)) # Getting the complete list 
    print(Concatinate_components)
    for listdata in range(0,len(Concatinate_components)): 
           print(Concatinate_components[listdata])

    #List of the communication system  
    for commu in list(dict_components): 
        if commu in communication_component: 
                  print("Found communication protocol",commu,dict_components.get(commu))
    print(dict_components) 
    return dict_components
#>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>
    # Write the output file into the usable function output 
    #json_dumpcom = json.dumps(dict_components)
    #writejson_Com = open("Components_node_robotics.json","w")
    #writejson_Com.write(json_dumpcom) #Write the json component 
    #writejson_Com.close()            
class Board(Node):
    """Node that displays image data in an ImageView widget"""
    nodeName = 'Boarddata'
    
    def __init__(self, name):
        self.view = None
        ## Initialize node with only a single input terminal
        Node.__init__(self, name, terminals={'data': {'io':'in'}})
        
    def setView(self, view):  ## setView must be called by the program
        self.view = view
        
    def process(self, data, display=True):
        ## if process is called with display=False, then the flowchart is being operated
        ## in batch processing mode, so we should skip displaying to improve performance.
        
        if display and self.view is not None:
            ## the 'data' argument is the value given to the 'data' terminal
            if data is None:
                self.view.setImage(np.zeros((1,1))) # give a blank array to clear the view
            else:
                self.view.setImage(data)
    
class Computeronboard(Node):
    """Node that displays image data in an ImageView widget"""
    nodeName = 'Computernode'
    
    def __init__(self, name):
        self.view = None
        ## Initialize node with only a single input terminal
        Node.__init__(self, name, terminals={'data': {'io':'in'}})
        
    def setView(self, view):  ## setView must be called by the program
        self.view = view
        
    def process(self, data, display=True):
        ## if process is called with display=False, then the flowchart is being operated
        ## in batch processing mode, so we should skip displaying to improve performance.
        
        if display and self.view is not None:
            ## the 'data' argument is the value given to the 'data' terminal
            if data is None:
                self.view.setImage(np.zeros((1,1))) # give a blank array to clear the view
            else:
                self.view.setImage(data)

class Imagesensor(Node):
    """Node that displays image data in an ImageView widget"""
    nodeName = 'Imagecameramodule'
    
    def __init__(self, name):
        self.view = None
        ## Initialize node with only a single input terminal
        Node.__init__(self, name, terminals={'data': {'io':'in'}})
        
    def setView(self, view):  ## setView must be called by the program
        self.view = view
        
    def process(self, data, display=True):
        ## if process is called with display=False, then the flowchart is being operated
        ## in batch processing mode, so we should skip displaying to improve performance.
        
        if display and self.view is not None:
            ## the 'data' argument is the value given to the 'data' terminal
            if data is None:
                self.view.setImage(np.zeros((1,1))) # give a blank array to clear the view
            else:
                self.view.setImage(data)

class Sensors(Node):
    """Node that displays image data in an ImageView widget"""
    nodeName = 'Sensormodule'
    
    def __init__(self, name):
        self.view = None
        ## Initialize node with only a single input terminal
        Node.__init__(self, name, terminals={'data': {'io':'in'}})
        
    def setView(self, view):  ## setView must be called by the program
        self.view = view
        
    def process(self, data, display=True):
        ## if process is called with display=False, then the flowchart is being operated
        ## in batch processing mode, so we should skip displaying to improve performance.
        
        if display and self.view is not None:
            ## the 'data' argument is the value given to the 'data' terminal
            if data is None:
                self.view.setImage(np.zeros((1,1))) # give a blank array to clear the view
            else:
                self.view.setImage(data)

class Acousticamplifier(Node):
    """Node that displays image data in an ImageView widget"""
    nodeName = 'Acoustticampmodule'
    
    def __init__(self, name):
        self.view = None
        ## Initialize node with only a single input terminal
        Node.__init__(self, name, terminals={'data': {'io':'in'}})
        
    def setView(self, view):  ## setView must be called by the program
        self.view = view
        
    def process(self, data, display=True):
        ## if process is called with display=False, then the flowchart is being operated
        ## in batch processing mode, so we should skip displaying to improve performance.
        
        if display and self.view is not None:
            ## the 'data' argument is the value given to the 'data' terminal
            if data is None:
                self.view.setImage(np.zeros((1,1))) # give a blank array to clear the view
            else:
                self.view.setImage(data)
class Navigationsensor(Node):
    """Node that displays image data in an ImageView widget"""
    nodeName = 'Navigationmodule'
    
    def __init__(self, name):
        self.view = None
        ## Initialize node with only a single input terminal
        Node.__init__(self, name, terminals={'data': {'io':'in'}})
        
    def setView(self, view):  ## setView must be called by the program
        self.view = view
        
    def process(self, data, display=True):
        ## if process is called with display=False, then the flowchart is being operated
        ## in batch processing mode, so we should skip displaying to improve performance.
        
        if display and self.view is not None:
            ## the 'data' argument is the value given to the 'data' terminal
            if data is None:
                self.view.setImage(np.zeros((1,1))) # give a blank array to clear the view
            else:
                self.view.setImage(data)

class CellularLTEmod(Node):
    """Node that displays image data in an ImageView widget"""
    nodeName = 'Cellularmodule'
    
    def __init__(self, name):
        self.view = None
        ## Initialize node with only a single input terminal
        Node.__init__(self, name, terminals={'data': {'io':'in'}})
        
    def setView(self, view):  ## setView must be called by the program
        self.view = view
        
    def process(self, data, display=True):
        ## if process is called with display=False, then the flowchart is being operated
        ## in batch processing mode, so we should skip displaying to improve performance.
        
        if display and self.view is not None:
            ## the 'data' argument is the value given to the 'data' terminal
            if data is None:
                self.view.setImage(np.zeros((1,1))) # give a blank array to clear the view
            else:
                self.view.setImage(data)
class Battery(Node):
    """Node that displays image data in an ImageView widget"""
    nodeName = 'Batterymodule'
    
    def __init__(self, name):
        self.view = None
        ## Initialize node with only a single input terminal
        Node.__init__(self, name, terminals={'data': {'io':'in'}})
        
    def setView(self, view):  ## setView must be called by the program
        self.view = view
        
    def process(self, data, display=True):
        ## if process is called with display=False, then the flowchart is being operated
        ## in batch processing mode, so we should skip displaying to improve performance.
        
        if display and self.view is not None:
            ## the 'data' argument is the value given to the 'data' terminal
            if data is None:
                self.view.setImage(np.zeros((1,1))) # give a blank array to clear the view
            else:
                self.view.setImage(data)
class BMSmodule(Node):
    """Node that displays image data in an ImageView widget"""
    nodeName = 'BMSmoduledata'
    
    def __init__(self, name):
        self.view = None
        ## Initialize node with only a single input terminal
        Node.__init__(self, name, terminals={'data': {'io':'in'}})
        
    def setView(self, view):  ## setView must be called by the program
        self.view = view
        
    def process(self, data, display=True):
        ## if process is called with display=False, then the flowchart is being operated
        ## in batch processing mode, so we should skip displaying to improve performance.
        
        if display and self.view is not None:
            ## the 'data' argument is the value given to the 'data' terminal
            if data is None:
                self.view.setImage(np.zeros((1,1))) # give a blank array to clear the view
            else:
                self.view.setImage(data)
class ActuatorDriverIC(Node):
    """Node that displays image data in an ImageView widget"""
    nodeName = 'Actuatormodule'
    
    def __init__(self, name):
        self.view = None
        ## Initialize node with only a single input terminal
        Node.__init__(self, name, terminals={'data': {'io':'in'}})
        
    def setView(self, view):  ## setView must be called by the program
        self.view = view
        
    def process(self, data, display=True):
        ## if process is called with display=False, then the flowchart is being operated
        ## in batch processing mode, so we should skip displaying to improve performance.
        
        if display and self.view is not None:
            ## the 'data' argument is the value given to the 'data' terminal
            if data is None:
                self.view.setImage(np.zeros((1,1))) # give a blank array to clear the view
            else:
                self.view.setImage(data)
class SensorArray(Node):
    
    """Node that displays image data in an ImageView widget"""
    nodeName = 'Sensorarraymodule'
    
    def __init__(self, name):
        self.view = None
        ## Initialize node with only a single input terminal
        Node.__init__(self, name, terminals={'data': {'io':'in'}})
        
    def setView(self, view):  ## setView must be called by the program
        self.view = view
        
    def process(self, data, display=True):
        ## if process is called with display=False, then the flowchart is being operated
        ## in batch processing mode, so we should skip displaying to improve performance.
        
        if display and self.view is not None:
            ## the 'data' argument is the value given to the 'data' terminal
            if data is None:
                self.view.setImage(np.zeros((1,1))) # give a blank array to clear the view
            else:
                self.view.setImage(data)
class Materials(CtrlNode):
    """Node that displays image data in an ImageView widget"""
    nodeName = 'MaterialsSkin'
    
    def __init__(self, name):
        self.view = None
        ## Initialize node with only a single input terminal
        Node.__init__(self, name, terminals={'data': {'io':'in'}})
        
    def setView(self, view):  ## setView must be called by the program
        self.view = view
        
    def process(self, data, display=True):
        ## if process is called with display=False, then the flowchart is being operated
        ## in batch processing mode, so we should skip displaying to improve performance.
        
        if display and self.view is not None:
            ## the 'data' argument is the value given to the 'data' terminal
            if data is None:
                self.view.setImage(np.zeros((1,1))) # give a blank array to clear the view
            else:
                self.view.setImage(data)


class MainWindow(QtWidgets.QMainWindow):
   
    def __init__(self, *args, **kwargs):
        super(MainWindow, self).__init__(*args, **kwargs)
        self.setFixedSize(496, 310)
        #Load the UI Page
        uic.loadUi('Loginpage.ui', self)
        self.setWindowTitle('Welcome to roboreactor User:'+"\t"+username)
        p = self.palette()
        p.setColor(self.backgroundRole(), QtCore.Qt.darkGray)
        self.setPalette(p)
        oImage = QImage("kobuki_new.jpg")
        oImage.scaled(300,200)
        #sImage = oImage.scaled(QSize(300,200))                   # resize Image to widgets size
        palette = QPalette()
        palette.setBrush(QPalette.Window, QBrush(oImage))
        self.setPalette(palette)
        self.pushButton.clicked.connect(self.Login) #button login 
        self.text = self.findChild(QTextEdit,"textEdit") #Getting the text edit input the username on the system
        self.text2 = self.findChild(QLineEdit,"lineEdit") #Getting the password input
        self.text2.setEchoMode(QLineEdit.Password) #QLine edit for hiding the password 
        self.label.setStyleSheet("color:white") 
        self.label_2.setStyleSheet("color:white")
        self.label_3.setStyleSheet("color:white")
        query()   #Query data database 
        #update()  #Update data rethrieve the data 
    def Login(self):
            print("Logging into the database......")
            usernamedata = self.text.toPlainText()
            passworddata = self.text2.text() # This is the QLineEdit for the text hiding password data 
            #self.text2.setEchoMode(QLineEdit.Password)
            print(usernamedata,passworddata) #Getting the username and password
            #reading the cloud database and activate the new window 
            #DATABASE_URL = os.environ['DATABASE_URL']
            #conn = psycopg2.connect(DATABASE_URL, sslmode='require') 
            conn = psycopg2.connect(
               DATABASE_URL,
               sslmode='require',
            )
            c = conn.cursor()
            c.execute('''CREATE TABLE IF NOT EXISTS customers
            (index Text,
            first_name Text,
            last_name Text,
            e_mail Text,
            password Text,
            address Text,
            payment_status Text,
            cardholder Text,
            schedule Text,
            recharge Text);''')
            # Create a cursor
            c = conn.cursor()
            #Grab stuff from online database 
            c.execute("SELECT*FROM customers")
            records = c.fetchall() 
            print(records[0])
            print("Amount of customers:",len(records)) #Find the amout of the customer
            am_customers = len(records)
            for rec in range(0,len(records)):
                   #print(records[rec][3],records[rec][4])
                   if usernamedata == records[rec][3]:
                       print("Username correct!")
                       if passworddata == records[rec][4]:
                               print("Password correct!")
                               #Create the title username data 
                               if client_username != []: 
                                  client_username.clear() 
                               if client_username == []:
                                  print("Getting the name record into the client username array to get the new title name")
                                  client_username.append(str(records[rec][1]) +"\t"+str(records[rec][2])) #Working user title created on the gui 
                               self.w = MainWindow2()
                               self.w.show() 
                               self.hide() 
                               break
                   
            conn.close()
def psi(i, j, k, offset=(50,50,100)):
    x = i-offset[0]
    y = j-offset[1]
    z = k-offset[2]
    th = np.arctan2(z, (x**2+y**2)**0.5)
    phi = np.arctan2(y, x)
    r = (x**2 + y**2 + z **2)**0.5
    a0 = 2
    #ps = (1./81.) * (2./np.pi)**0.5 * (1./a0)**(3/2) * (6 - r/a0) * (r/a0) * np.exp(-r/(3*a0)) * np.cos(th)
    ps = (1./81.) * 1./(6.*np.pi)**0.5 * (1./a0)**(3/2) * (r/a0)**2 * np.exp(-r/(3*a0)) * (3 * np.cos(th)**2 - 1)
    return ps
           
#Scan host devices name in the local network 
def pinger(job_q, results_q):
    """
    Do Ping
    :param job_q:
    :param results_q:
    :return:
    """
    DEVNULL = open(os.devnull, 'w')
    while True:

        ip = job_q.get()

        if ip is None:
            break

        try:
            subprocess.check_call(['ping', '-c1', ip],
                                  stdout=DEVNULL)
            results_q.put(ip)
        except:
            pass


def get_my_ip():
    """
    Find my IP address
    :return:
    """
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    s.connect(("8.8.8.8", 80))
    ip = s.getsockname()[0]
    s.close()
    return ip


def map_network(pool_size=255):
    """
    Maps the network
    :param pool_size: amount of parallel ping processes
    :return: list of valid ip addresses
    """

    ip_list = list()

    # get my IP and compose a base like 192.168.1.xxx
    ip_parts = get_my_ip().split('.')
    base_ip = ip_parts[0] + '.' + ip_parts[1] + '.' + ip_parts[2] + '.'

    # prepare the jobs queue
    jobs = multiprocessing.Queue()
    results = multiprocessing.Queue()

    pool = [multiprocessing.Process(target=pinger, args=(jobs, results)) for i in range(pool_size)]

    for p in pool:
        p.start()

    # cue hte ping processes
    for i in range(1, 255):
        jobs.put(base_ip + '{0}'.format(i))

    for p in pool:
        jobs.put(None)

    for p in pool:
        p.join()

    # collect he results
    while not results.empty():
        ip = results.get()
        ip_list.append(ip)

    return ip_list
class Worker1(QThread):
    ImageUpdate = pyqtSignal(QImage)
    def run(self):
        
        #UDP socket client 
        BUFF_SIZE = 65536
        client_socket = socket.socket(socket.AF_INET,socket.SOCK_DGRAM)
        client_socket.setsockopt(socket.SOL_SOCKET,socket.SO_RCVBUF,BUFF_SIZE)
        host_name = socket.gethostname()
        message = b'Hello'
        port = 9800 #hostip_mem[0]
        client_socket.sendto(message,(hostip_mem[0],port))
        fps,st,frames_to_count,cnt = (0,0,20,0) 
        self.ThreadActive = True
        while self.ThreadActive:
        
            packet,_ = client_socket.recvfrom(BUFF_SIZE)
            data = base64.b64decode(packet,' /')
            npdata = np.fromstring(data,dtype=np.uint8)
            Image = cv2.imdecode(npdata,1)
            Image = cv2.cvtColor(Image, cv2.COLOR_BGR2RGB)
            Image = cv2.putText(Image,'FPS: '+str(fps),(10,40),cv2.FONT_HERSHEY_SIMPLEX,0.7,(0,0,255),1)
            FlippedImage = cv2.flip(Image, 1)
            ConvertToQtFormat = QImage(FlippedImage.data, FlippedImage.shape[1], FlippedImage.shape[0], QImage.Format_RGB888)
            Pic = ConvertToQtFormat.scaled(751, 551, Qt.KeepAspectRatio) 
            self.ImageUpdate.emit(Pic)
            #cv2.imshow("Receiving video",Image)
            key = cv2.waitKey(1) & 0xFF 
            if key == ord('q'):
                client_socket.close() 
                break 
            
            if cnt == frames_to_count:
                     try:
                         fps = round(frames_to_count/time.time()-st) 
                         st=time.time() 
                         cnt=0
                     except:
                         pass 
            cnt+=1              
                
    def stop(self):
        self.ThreadActive = False
        self.quit()
def query():
      #Getting the host url https://dashboard.heroku.com/apps 
      #DATABASE_URL = os.environ['DATABASE_URL']
      #conn = psycopg2.connect(DATABASE_URL, sslmode='require') 
      conn = psycopg2.connect(
               DATABASE_URL,
               sslmode='require',
      )
      c = conn.cursor()
      c.execute('''CREATE TABLE IF NOT EXISTS customers
      (index Text,
      first_name Text,
      last_name Text,
      e_mail Text,
      password Text,
      address Text,
      payment_status Text,
      Cardholder Text,
      schedule Text,
      Recharge Text);
      ''')
      conn.commit()
      conn.close()
      

def main():
    app = QtWidgets.QApplication(sys.argv)
     
    main = MainWindow()
    main.show()
    
    sys.exit(app.exec_())
    
    
if __name__ == '__main__':
     main()
     