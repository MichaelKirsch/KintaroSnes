#!/usr/bin/python -u
#Copyright 2017 Michael Kirsch

#Permission is hereby granted, free of charge, to any person obtaining a copy of this software and associated documentation files (the "Software"),
#to deal in the Software without restriction, including without limitation the rights to use, copy, modify, merge, publish, distribute, sublicense,
# and/or sell copies of the Software, and to permit persons to whom the Software is furnished to do so, subject to the following conditions:
#The above copyright notice and this permission notice shall be included in all copies or substantial portions of the Software.
import ConfigParser
import time
import os
import RPi.GPIO as GPIO
import commands
from ConfigParser import SafeConfigParser
GPIO.setmode(GPIO.BOARD) #Use the same layout as the pins
LED=7
FAN=8
RESET=3
POWER=5
CHECK_PCB=10
GPIO.setup(LED, GPIO.OUT) #LED Output
GPIO.setup(FAN, GPIO.OUT) #FAN Output
GPIO.setup(POWER, GPIO.IN)  #set pin as input
GPIO.setup(RESET, GPIO.IN, pull_up_down=GPIO.PUD_UP) #set pin as input and switch on internal pull up resistor
GPIO.setup(CHECK_PCB, GPIO.IN, pull_up_down=GPIO.PUD_UP)
Config = ConfigParser.ConfigParser()
file = "/opt/kintaro/start/kintaro.config"
Config.read(file)

def temp(): #returns the gpu temoperature
    p = commands.getstatusoutput('vcgencmd measure_temp')
    s = str(p[1])
    s = s.replace("temp=", "")
    s = float(s.replace("'C", ""))
    return s

class led:  #class to control the led
    def toggle(self,status):  #toggle the led on of off
        if status == 0:       #the led is inverted
            GPIO.output(LED, GPIO.LOW)
        if status == 1:
            GPIO.output(LED, GPIO.HIGH)

    def blink(self,amount,interval): #blink the led
        for x in range(amount):
            toggle(1)
            time.sleep(interval)
            toggle(0)
            time.sleep(interval)


def fan(status):  #switch the fan on or off
    if status == 1:
        GPIO.output(FAN, GPIO.HIGH)
    if status == 0:
        GPIO.output(FAN, GPIO.LOW)

def fancontrol(hysteresis,starttemp):  #read the temp and have a buildin hysteresis
    if temp() > starttemp:
        fan(1)
    if temp() < starttemp-hysteresis:
        fan(0)


def toggle(toggle_this):  #change one of the values in the config file
    parser = SafeConfigParser()
    parser.read(file)
    if (Config.getboolean("Boot", toggle_this) == True):
        parser.set('Boot', toggle_this, "False")
        fan(0)
    if (Config.getboolean("Boot", toggle_this) == False):
        parser.set('Boot', toggle_this, "True")
    with open(file, "w+") as configfile:
        parser.write(configfile)
if (Config.getboolean("Boot", "video")==True):
    os.system("omxplayer /opt/kintaro/start/intro.mp4 &") #start the bootvideo on start

while True:
    Config.read(file)       #read the configfile
    if Config.getboolean("Boot", "pcb")==True and GPIO.input(CHECK_PCB)==GPIO.LOW: #check if there is an pcb and if there is
        led.toggle(1)
        if (Config.getboolean("Boot", "Fan")==True): #check if the fan is activated in the config
            fancontrol(5,60) # fan starts at 60 degrees and has a 5 degree hysteresis
        if (GPIO.input(POWER) == GPIO.HIGH) and GPIO.input(CHECK_PCB)==GPIO.LOW: #shutdown funktion if the powerswitch is toggled
            os.system("killall emulationstation")
            led.toggle(0)
            fan(0)
            os.system("sudo shutdown -h now")
        if (GPIO.input(RESET) == GPIO.LOW): #reset function
            counter = 0 #counter for the time funktion
            time.sleep(0.01) #debounce time
            while (GPIO.input(RESET) == GPIO.LOW): #while the button is hold the counter counts up
                counter = counter +1
                time.sleep(0.01)
            if counter >100:  #check if its hold more that one second
                if counter<=500: #if you hold it less than 5 sec it will toggle the fan
                    toggle("fan")
                    led.blink(3,0.5)
                if counter >500: #if you hold it more than 5 seconds if will toggle the bootupvideo
                    toggle("video")
                    led.blink(10,0.5)
            elif(counter<=100): #if you dont hold it it will toggle a software reboot
                os.system("killall emulationstation")
                os.system("sudo reboot")
