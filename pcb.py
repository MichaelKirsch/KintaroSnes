#!/usr/bin/python3
#Copyright 2017 Michael Kirsch

#Permission is hereby granted, free of charge, to any person obtaining a copy of this software and associated documentation files (the "Software"),
#to deal in the Software without restriction, including without limitation the rights to use, copy, modify, merge, publish, distribute, sublicense,
# and/or sell copies of the Software, and to permit persons to whom the Software is furnished to do so, subject to the following conditions:
#The above copyright notice and this permission notice shall be included in all copies or substantial portions of the Software.

try:
    import http.server
    import configparser
    import time
    import os
    import RPi.GPIO as GPIO
    import subprocess
    from configparser import SafeConfigParser
    from enum import Enum
except ImportError:
    raise ImportError('spidev or gpio not installed')

class SNES:

    def __init__(self):

        #GPIOs

        self.led_pin=7
        self.fan_pin=8
        self.reset_pin=3
        self.power_pin=5
        self.check_pin=10

        #vars

        self.fan_hysteresis = 5
        self.fan_starttemp = 60
        self.fan_hysteresis_pwm = 20
        self.fan_starttemp_pwm = 60
        self.reset_hold_short = 100
        self.reset_hold_long = 500
        self.debounce_time = 0.1
        self.counter_time = 0.01
        self.delay_until_reset = 2
        self.is_pwm = False

        #path

        self.kintaro_folder = "/opt/kintaro/"
        self.start_folder = "start/"
        self.intro_video = self.kintaro_folder + self.start_folder + "intro.mp4"
        self.config_file = self.kintaro_folder + self.start_folder + "kintaro.config"
        self.temp_command = 'vcgencmd measure_temp'

        #Set the GPIOs

        GPIO.setmode(GPIO.BOARD)  # Use the same layout as the pins
        GPIO.setwarnings(False)
        GPIO.setup(self.led_pin, GPIO.OUT)  # LED Output
        GPIO.setup(self.fan_pin, GPIO.OUT)  # Fan normal Output
        GPIO.setup(self.power_pin, GPIO.IN)  # set pin as input
        GPIO.setup(self.reset_pin, GPIO.IN,
                   pull_up_down=GPIO.PUD_UP)  # set pin as input and switch on internal pull up resistor
        GPIO.setup(self.check_pin, GPIO.IN, pull_up_down=GPIO.PUD_UP)
        if self.return_config_bool("PWM_FAN"):
            self.is_pwm = True
            self.pwm=GPIO.PWM(self.fan_pin,50)
            self.pwm.start(0)


    def power_interrupt(self, channel):
        time.sleep(self.debounce_time)  # debounce
        if GPIO.input(self.power_pin) == GPIO.HIGH and GPIO.input(
                self.check_pin) == GPIO.LOW:  # shutdown function if the powerswitch is toggled
            self.led(0)  # led and fan off
            os.system("killall emulationstation")
            self.blink(20, 0.1) #wait for the metadata to be safed
            self.fan(0)
            os.system("sudo shutdown -h now")

    def reset_interrupt(self, channel):
        if GPIO.input(self.reset_pin) == GPIO.LOW:  # reset function
            reset_counter = 0  # counter for the time funktion
            time.sleep(self.debounce_time)  # debounce time
            while GPIO.input(self.reset_pin) == GPIO.LOW:  # while the button is hold the counter counts up
                reset_counter = reset_counter + 1
                time.sleep(self.counter_time)
            if reset_counter > self.reset_hold_short:  # check if its hold more that one second
                if reset_counter <= self.reset_hold_long:  # if you hold it less than 5 sec it will toggle the fan
                    self.change_config_value("fan")
                    self.blink(3, 0.5)
                    self.led(1)
                if reset_counter > self.reset_hold_long:  # if you hold it more than 5 seconds if will toggle the bootupvideo
                    self.change_config_value("video")
                    self.blink(10, 0.5)
                    self.led(1)
            else:
                os.system("killall emulationstation")
                self.blink(15, 0.1)
                os.system("sudo reboot")

    def pcb_interrupt(self, channel):
        GPIO.cleanup()  # when the pcb is pulled clean all the used GPIO pins

    def temp(self):     #returns the gpu temoperature
        res = os.popen(self.temp_command).readline()
        return float((res.replace("temp=", "").replace("'C\n", "")))

    def led(self,status):  #toggle the led on of off
        if status == 0:       #the led is inverted
            GPIO.output(self.led_pin, GPIO.LOW)
        if status == 1:
            GPIO.output(self.led_pin, GPIO.HIGH)

    def blink(self,amount,interval): #blink the led
        for x in range(amount):
            self.led(1)
            time.sleep(interval)
            self.led(0)
            time.sleep(interval)

    def return_config_bool(self,searchterm):
        Config = configparser.ConfigParser()
        Config.read(self.config_file)  # read the configfile
        return Config.getboolean("Boot", searchterm)

    def fan(self,status):  #switch the fan on or off
        if status == 1:
            GPIO.output(self.fan_pin, GPIO.HIGH)
        if status == 0:
            GPIO.output(self.fan_pin, GPIO.LOW)

    def fancontrol_normal(self,hysteresis,starttemp):  #read the temp and have a buildin hysteresis
        if self.temp() > starttemp:
            self.fan(1)
        if self.temp() < starttemp-hysteresis:
            self.fan(0)

    def pwm_fancontrol(self,hysteresis, starttemp, temp):
        perc = 100.0 * ((temp - (starttemp - hysteresis)) / (starttemp - (starttemp - hysteresis)))
        perc=min(max(perc, 0.0), 100.0)
        self.pwm.ChangeDutyCycle(float(perc))

    def change_config_value(self,toggle_this):  #change one of the values in the config file
        parser = configparser.ConfigParser()
        parser.read(self.config_file)
        if self.return_config_bool(toggle_this):
            parser.set('Boot', toggle_this, "False")
            self.fan(0)
        else:
            parser.set('Boot', toggle_this, "True")
        with open(self.config_file, "w+") as configfile:
            parser.write(configfile)

    def check_video(self):
        if self.return_config_bool("video"):
            os.system("omxplayer " + self.intro_video + " &")  # start the bootvideo on start

    def check_fan(self):
        if self.return_config_bool("fan"):  # check if the fan is activated in the config
            if self.is_pwm:
                self.pwm_fancontrol(self.fan_hysteresis_pwm,self.fan_starttemp_pwm,self.temp())
            else:
                self.fancontrol_normal(self.fan_hysteresis,self.fan_starttemp)  # fan starts at 60 degrees and has a 5 degree hysteresis

    def attach_interrupts(self):
        if self.return_config_bool("pcb") and GPIO.input(self.check_pin) == GPIO.LOW:  # check if there is an pcb and if so attach the interrupts
            GPIO.add_event_detect(self.check_pin, GPIO.RISING,callback=self.pcb_interrupt)  # if not the interrupt gets attached
            if GPIO.input(self.power_pin) == GPIO.HIGH: #when the system gets startet in the on position it gets shutdown
                os.system("sudo shutdown -h now")
            else:
                self.led(1)
                GPIO.add_event_detect(self.reset_pin, GPIO.FALLING, callback=self.reset_interrupt)
                GPIO.add_event_detect(self.power_pin, GPIO.RISING, callback=self.power_interrupt)
        else:       #no pcb attached so lets exit
            GPIO.cleanup()
            exit()

snes = SNES()

snes.attach_interrupts()
snes.check_video()

while True:
    time.sleep(5)
    snes.led(1)
    snes.check_fan()
