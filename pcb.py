#!/usr/bin/python3 -u
#Copyright 2017 Michael Kirsch

#Permission is hereby granted, free of charge, to any person obtaining a copy of this software and associated documentation files (the "Software"),
#to deal in the Software without restriction, including without limitation the rights to use, copy, modify, merge, publish, distribute, sublicense,
# and/or sell copies of the Software, and to permit persons to whom the Software is furnished to do so, subject to the following conditions:
#The above copyright notice and this permission notice shall be included in all copies or substantial portions of the Software.
import configparser
import time
import os
import RPi.GPIO as GPIO
import subprocess
from configparser import SafeConfigParser
from enum import Enum

class pcb_components(Enum):
    LED = 7
    FAN = 8
    RESET = 3
    POWER = 5
    CHECK_PCB = 10

class path():
    kintaro_folder = "/opt/kintaro/"
    start_folder = kintaro_folder + "start/"
    intro_video = kintaro_folder + start_folder + "intro.mp4"
    config_file = kintaro_folder + start_folder + "kintaro.config"
    temp_command = 'vcgencmd measure_temp'

class vars():
    fan_hysteresis = 5
    fan_starttemp = 50
    reset_hold_short = 100
    reset_hold_long = 500
    debounce_time = 0.01
    counter_time = 0.01

GPIO.setmode(GPIO.BOARD) #Use the same layout as the pins
GPIO.setup(pcb_components.LED.value, GPIO.OUT) #LED Output
GPIO.setup(pcb_components.FAN.value, GPIO.OUT) #FAN Output
GPIO.setup(pcb_components.POWER.value, GPIO.IN)  #set pin as input
GPIO.setup(pcb_components.RESET.value, GPIO.IN, pull_up_down=GPIO.PUD_UP) #set pin as input and switch on internal pull up resistor
GPIO.setup(pcb_components.CHECK_PCB.value, GPIO.IN, pull_up_down=GPIO.PUD_UP)

def temp(): #returns the gpu temoperature
    res = os.popen(path.temp_command).readline()
    return (res.replace("temp=", "").replace("C\n", ""))

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

def return_config_bool(searchterm):
    Config = configparser.ConfigParser()
    Config.read(path.config_file)  # read the configfile
    return Config.getboolean("Boot", searchterm)

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

if return_config_bool("video"):
    os.system("omxplayer" + path.intro_video + "&") #start the bootvideo on start

def toggle(toggle_this):  #change one of the values in the config file
    parser = SafeConfigParser()
    parser.read(path.config_file)
    if return_config_bool(toggle_this):
        parser.set('Boot', toggle_this, "False")
        fan(0)
    else:
        parser.set('Boot', toggle_this, "True")
    with open(path.config_file, "w+") as configfile:
        parser.write(configfile)

def check_powerbutton():
    if (GPIO.input(POWER) == GPIO.HIGH) and GPIO.input(CHECK_PCB) == GPIO.LOW:  # shutdown funktion if the powerswitch is toggled
        os.system("killall emulationstation")
        led.toggle(0)
        fan(0)
        os.system("sudo shutdown -h now")

def check_resetbutton():
    if (GPIO.input(RESET) == GPIO.LOW):  # reset function
        reset_counter = 0  # counter for the time funktion
        time.sleep(vars.debounce_time)  # debounce time
        while (GPIO.input(RESET) == GPIO.LOW):  # while the button is hold the counter counts up
            reset_counter = reset_counter + 1
            time.sleep(vars.counter_time)
        if reset_counter > vars.reset_hold_short:  # check if its hold more that one second
            if counter <= vars.reset_hold_long:  # if you hold it less than 5 sec it will toggle the fan
                toggle("fan")
                led.blink(3, 0.5)
            if counter > vars.reset_hold_long:  # if you hold it more than 5 seconds if will toggle the bootupvideo
                toggle("video")
                led.blink(10, 0.5)
        elif (counter <= vars.reset_hold_short):  # if you dont hold it it will toggle a software reboot
            os.system("killall emulationstation")
            os.system("sudo reboot")

while True:
    if return_config_bool("pcb") and GPIO.input(CHECK_PCB)==GPIO.LOW: #check if there is an pcb and if there is
        led.toggle(1)
        if return_config_bool("fan"): #check if the fan is activated in the config
            fancontrol(vars.fan_hysteresis , vars.fan_starttemp) # fan starts at 60 degrees and has a 5 degree hysteresis
        check_powerbutton()
        check_resetbutton()

