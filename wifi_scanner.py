import subprocess 
import csv
import pandas
mem_str = []
while True:
         getwifi = subprocess.check_output("nmcli dev wifi",shell=True) 
         dataframe = getwifi.decode('utf-8')
         #print(type(dataframe))
         #print(dataframe)
         file = open("currentwifi.csv",'w')
         file.write(dataframe)
         file.close()
         #df = pandas.DataFrame(dataframe, columns=['SSID', 'SIGNAL'])
         df = pandas.read_csv('currentwifi.csv')
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
                      if len(mem_str) < len(index):
                               mem_str.append(getting_str[10]) #getting the mem wifi name 
                      if len(mem_str) > len(index):
                              terminal = len(mem_str)-len(index)
                              for wifilist in range(len(index),terminal):
                                             mem_str.remove(mem_str[wifilist]) #remove the len of the index if the length is out of range
         print(mem_str)                   