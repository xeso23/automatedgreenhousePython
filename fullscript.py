import serial
import time
import sys
import mysql.connector
import threading


greenDB = mysql.connector.connect(user='root', password='root',
                              host='192.188.131.181',
                              database='greenhousesysdb')
cursor = greenDB.cursor()
findmasterid = ("SELECT Distinct MasterID from config_mastercontrollers");
cursor.execute(findmasterid)
for MasterID, in cursor:
        masterid1 = MasterID

#for c in range(1,4):
 #   arduino[c] = "%s_UNIT%s" % (masterid1, c)
  #  print(arduino)
arduino1 = ("%s_UNIT1" % (masterid1))
arduino2 = ("%s_UNIT2" % (masterid1))
#arduino2 = "WJU_RPI1_UNIT2"
arduino3 = ("%s_UNIT3" % (masterid1))
arduino4 = ("%s_UNIT4" % (masterid1))


##Instantiating up to four Arduinos, checking availibility and catching timeout or inactive exceptions.##
#1
try:
    ard1 = serial.Serial('COM3', 115200, timeout = 60)
    time.sleep(5)
    activateard1 = ("Update config_units set isActive = 'Y' where MasterID = '%s' and UnitID ='%s';" % (masterid1, arduino1))
    cursor.execute(activateard1)
    greenDB.commit()
    
except serial.SerialException:
    inactiveard1 = ("Update config_units set isActive = 'N' where MasterID = '%s' and UnitID ='%s';" % (masterid1, arduino1))
    cursor.execute(inactiveard1)
    greenDB.commit()
   
#2
try:
    ard2 = serial.Serial('COM4', 115200, timeout = 60)
    time.sleep(5)
    activateard2 = ("UPDATE config_units SET isActive='Y' where MasterID='%s' AND UnitID='%s';" % (masterid1, arduino2))
    cursor.execute(activateard2)
    greenDB.commit()
    
except serial.SerialException:
    inactiveard2 = ("Update config_units set isActive = 'N' where MasterID='%s' and UnitID ='%s';" % (masterid1, arduino2))
    cursor.execute(inactiveard2)
    greenDB.commit()
    
#3
try:
    ard3 = serial.Serial('COM5', 115200, timeout = 60)
    time.sleep(5)
    activateard3 = ("Update config_units set isActive = 'Y' where MasterID = '%s' and UnitID ='%s';" % (masterid1, arduino3))
    cursor.execute(activateard3)
    greenDB.commit()
except serial.SerialException:
    inactiveard3 = ("Update config_units set isActive = 'N' where MasterID = '%s' and UnitID ='%s';" % (masterid1, arduino3))
    cursor.execute(inactiveard3)
    greenDB.commit()
    
#4
try:
    ard4 = serial.Serial('COM6', 115200, timeout = 60)
    time.sleep(5)
    activateard4 = ("Update config_units set isActive = 'Y' where MasterID = '%s' and UnitID ='%s';" % (masterid1, arduino4))
    cursor.execute(activateard4)
    greenDB.commit()
except serial.SerialException:
    inactiveard4 = ("Update config_units set isActive = 'N' where MasterID = '%s' and UnitID ='%s';" % (masterid1, arduino4))
    cursor.execute(inactiveard4)
    greenDB.commit()
    

def readArduino2Temp(ard):
    try:
        result = ard.read(12).strip()
        newresult = str(result.decode()) 
    except ard.SerialTimeoutException:
         print ('Data could not be read')
         time.sleep(1)
    switch = False
    humidity = ""
    temperature = ""
    for c in range(len(newresult)):
            #print(newresult[c])
            if newresult[c] == '|':
                switch = True
            if switch == False:
                humidity += newresult[c]
            
            else:
                if newresult[c] != '|':
                   temperature += newresult[c]
    return humidity, temperature

def mainfunc():
        #print(daystarthour)
        ard1active = ("SELECT isActive from config_units where MasterID = '%s' and UnitID ='%s'" % (masterid1, arduino1))
        cursor.execute(ard1active)
        for isActive, in cursor:
                ard1ON = isActive;
        ard2active = ("SELECT isActive from config_units where MasterID = '%s' and UnitID ='%s'" % (masterid1, arduino2))
        cursor.execute(ard2active)
        for isActive, in cursor:
                ard2ON = isActive;
        ard3active = ("SELECT isActive from config_units where MasterID = '%s' and UnitID ='%s'" % (masterid1, arduino3))
        cursor.execute(ard3active)
        for isActive, in cursor:
                ard3ON = isActive;
       # ard4active = ("SELECT isActive from config_units where MasterID = '%s' and UnitID ='%s'" % (masterid1, arduino4))
      #  cursor.execute(ard4active)
       # for isActive, in cursor:
        #        ard4ON = isActive;
        ard4ON = 'N';
        
        if(ard1ON == 'Y'):
                try:
                        ard = ard1          
                        humid, temp = readArduino2Temp(ard);
                        
                except serial.SerialException:
                        activeButBrokenInput1 = ("CALL INSERT_statsunits_minutely(%s, %s, 0, 0, 'N', 'N', 0);" % (masterid1, arduino1))
                        cursor.execute(activeButBrokenInput1)
                        greenDB.commit()
        elif(ard2ON == 'Y'):
                try:
                        ard = ard2          
                        humid2, temp2 = readArduino2Temp(ard);
                        #Temperature/Fan
                        maxT = ("SELECT MaxTemp from config_units where MasterID = '%s' and UnitID ='%s'" % (masterid1, arduino2))
                        cursor.execute(maxT)
                        for MaxTemp, in cursor:
                                maxTemp = MaxTemp
                        if(float(temp2) >= MaxTemp):
                                fanOn = 'Y'
                                fanCode = 'fan21'
                        else:
                                fanOn = 'N'
                                fanCode = 'fan20'
                        #Lights
                        checklights = ("SELECT CASE WHEN CURRENT_TIMESTAMP BETWEEN DATE_ADD(DATE_FORMAT(CURRENT_TIMESTAMP, '%Y-%m-%d 00:00:00'), INTERVAL (SELECT StartOfDayTime FROM config_units WHERE UnitID = '" + arduino2 + "' LIMIT 1) HOUR) AND DATE_ADD(DATE_FORMAT(CURRENT_TIMESTAMP, '%Y-%m-%d 00:00:00'), INTERVAL (SELECT (StartOfDayTime + LightsOn_Hours) FROM config_units WHERE UnitID = '" + arduino2 + "' LIMIT 1) HOUR ) THEN 'Y' ELSE 'N' END as ActivateLights;")
                        cursor.execute(checklights)
                        for ActivateLights, in cursor:
                                LightOn = ActivateLights
                        if(LightOn == 'Y'):
                                lightCode = 'lgh21'
                        else:
                                lightCode = 'lgh20'
                        #Water
                        checkwater = ("select CASE WHEN CAST((DATE_FORMAT(CURRENT_TIMESTAMP, '%H') * 60 + DATE_FORMAT(CURRENT_TIMESTAMP, '%i')) % (60 *(24/(SELECT WaterUnits FROM config_units WHERE UnitID = '" + arduino2 + "' LIMIT 1))) as unsigned) = 0 THEN 1 ELSE 0 END as ActivateWater;")
                        cursor.execute(checkwater)
                        for ActivateWater, in cursor:
                                WaterUsed = ActivateWater
                        if(WaterUsed == 1):
                                waterCode = 'wtr21'
                        else:
                                waterCode = 'wtr20'
                        test = str.encode(("%s%s%s") % (lightCode, waterCode, fanCode))
                        ard2.write(test)
                        #time.sleep(10)
                        ardInput2 = ("CALL INSERT_statsunits_minutely('%s', '%s', %s, %s, '%s', '%s', %s);" % (masterid1, arduino2, temp2, humid2, LightOn, fanOn, WaterUsed))
                        cursor.execute(ardInput2)
                        greenDB.commit()
                        #time.sleep(10)
                except serial.SerialException:
                        activeButBrokenInput2 = ("CALL INSERT_statsunits_minutely(%s, %s, 0, 0, 'N', 'N', 0);" % (masterid1, arduino2))
                        cursor.execute(activeButBrokenInput2)
                        greenDB.commit()

        elif(ard3ON == 'Y'):
                try:
                        ard = ard3          
                        humid, temp = readArduino2Temp(ard);
                        print('yes');
                except serial.SerialException:
                        activeButBrokenInput3 = ("CALL INSERT_statsunits_minutely(%s, %s, 0, 0, 'N', 'N', 0);" % (masterid1, arduino3))
                        cursor.execute(activeButBrokenInput3)
                        greenDB.commit()
        elif(ard4ON == 'Y'):
                try:
                        ard = ard4          
                        humid, temp = readArduino2Temp(ard);
                        print('yes');
                except serial.SerialException:
                        activeButBrokenInput4 = ("CALL INSERT_statsunits_minutely(%s, %s, 0, 0, 'N', 'N', 0);" % (masterid1, arduino4))
                        cursor.execute(activeButBrokenInput4)
                        greenDB.commit()

        
#t = threading.Timer(60.0, mainfunc)
while(True):
      # gtk.timeout_add(60*1000, mainfunc())
        mainfunc()
       #time.sleep(60)
        #print("waiting...")
              
greenDB.close()  
     
