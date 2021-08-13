# -*- cofing: utf-8 -*-

import subprocess
import datetime
import RPi.GPIO as GPIO
from time import sleep
import threading
import requests
import settings

#OCCUPIED_COLOR
#VACANT_COLOR

def sense():
    SENSOR_INTERVAL=1
    HUMAN_PIN = 18

    # initialize GPIO
    GPIO.setwarnings(False)
    GPIO.setmode(GPIO.BCM)
    GPIO.setmode(GPIO.BCM)
    GPIO.setup(HUMAN_PIN, GPIO.IN)
    
    # Hue settings
    HUE_API_OUTSIDE=settings.HUE_API_OUTSIDE

    HUMAN_DURATION=45

    count_down=HUMAN_DURATION
    count=0
    count_no=0
    
    try:
        
        while True:
            status=GPIO.input(HUMAN_PIN)
            if status == 1:
                
                now = datetime.datetime.now()
                print(now)
                count+=1
                count_down=HUMAN_DURATION
                
                print('someone is there !!: ' + str(count))
                
                #RED light on
                result = requests.put(HUE_API_OUTSIDE, json = {"on":True, "bri":60, "xy":[0.7, 0.26]})
                                            
            else:
                count_down-=1
                print(count_down)
                    
                if count_down == 0:
                    count_no+=1
                    print('light turns off: ' + str(count_no))
                          
                    #light off
                    result = requests.put(HUE_API_OUTSIDE, json = {"on":False})
            
                #count_no+=1
                #print('there is no one: ' + str(count_no))
            
            sleep(SENSOR_INTERVAL)
    
    except KeyboardInterrupt:
        pass
    
    GPIO.cleanup()

def callHueApi(color=0):
    pass

if __name__=='__main__':        
        sense()
