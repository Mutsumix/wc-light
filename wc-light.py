# -*- cofing: utf-8 -*-

import subprocess
import datetime
import RPi.GPIO as GPIO
from time import sleep
import threading
import requests
import settings
import json
import random

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
    HUE_API_INSIDE=settings.HUE_API_INSIDE
    
    LIGHT_DURATION=15
    MUSIC_DURATION=45

    light_count_down=0
    music_count_down=0
    #count=0
    #count_no=0
        
    
    try:
        
        while True:
            status=GPIO.input(HUMAN_PIN)
            if status == 1:
                
                now = datetime.datetime.now()
                print(now)
                #count+=1
                print('someone is there !!')
                
                #RED light on
                result = requests.put(HUE_API_OUTSIDE, json = {"on":True, "bri":60, "xy":[0.7, 0.26]})
                #INSERT light on
                result = requests.put(HUE_API_INSIDE, json = {"on":True, "bri":200})
                #sound on
                sound_on(music_count_down)
                light_count_down=LIGHT_DURATION
                music_count_down=MUSIC_DURATION
  
            else:
                light_count_down-=1
                music_count_down-=1
                print('Light:' + str(light_count_down) + ', Music' + str(music_count_down))
                    
                if light_count_down == 0:
                    #count_no+=1
                    print('light turns off')
                          
                    #light off
                    result = requests.put(HUE_API_OUTSIDE, json = {"on":False})
                
                if music_count_down == 5:
                    result = requests.put(HUE_API_INSIDE, json = {"on":True, "bri":100})
                    
                if music_count_down == 0:
                    print('music turns off')
                    
                    
                    #INSIDE light off
                    result = requests.put(HUE_API_INSIDE, json = {"on":True, "bri":30})
                    #music off
                    sound_off()
            
                #count_no+=1
                #print('there is no one: ' + str(count_no))
            
            sleep(SENSOR_INTERVAL)
    
    except KeyboardInterrupt:
        pass
    
    GPIO.cleanup()

def callHueApi(color=0):
    pass

def sound_on(count_down):
    if count_down < 0:
        songs = json.load(open('music/songlist.json', 'r'))
        song_no = random.randint(1, len(songs))
        se = ''
        
        for song in songs:
            if song_no == songs[song]['no']:
                se = songs[song]['title']
        
        print(se)
        subprocess.Popen(['mpg321', '-g', '3', '-q', 'music/' + se + '.mp3'], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
#    else:
#        print('process ongoing')
    
def sound_off():
    subprocess.Popen(['killall', 'mpg321'])

if __name__=='__main__':        
        sense()
