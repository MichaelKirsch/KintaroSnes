#! /usr/bin/python3
import os
import configparser
from configparser import SafeConfigParser
from dialog import Dialog
Config = configparser.ConfigParser()
file="/opt/kintaro/start/kintaro.config"
Config.read(file)
# You may want to use 'autowidgetsize=True' here (requires pythondialog >= 3.1)
d = Dialog(dialog="dialog")
# Dialog.set_background_title() requires pythondialog 2.13 or later
d.set_background_title("Kintaro-Setup")

parser = SafeConfigParser()
parser.read(file)
if d.yesno("Do you want to activate the LED and the Switches?") == d.OK:
    parser.set('Boot', 'pcb', "True")
else:
    parser.set('Boot', 'pcb', "False")
if d.yesno("Do you want to activate the fan output?") == d.OK:
    parser.set('Boot', 'fan', "True")
else:
    parser.set('Boot', 'fan', "False")
if d.yesno("Do you want to have our custom video on startup?") == d.OK:
    parser.set('Boot', 'video', "True")
else:
    parser.set('Boot', 'video', "False")
with open(file, "w+") as configfile:
    parser.write(configfile)
if d.yesno("Do you want to restart now?") == d.DIALOG_OK:
    os.system("sudo reboot")
else:
    quit()

