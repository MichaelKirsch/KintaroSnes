# Kintaro Installer

Easy Package to provide drivers for the Kintaro Cases 

### Installing:

## Installation for experts:

sudo wget -O - https://www.dropbox.com/s/gmziwqpipzpe38l/kintaroinstaller.sh | bash

## Installation for beginners:

To get to working system you need a running debian based operating system such as RetroPie or Raspbian.
You can download RetroPie here: https://retropie.org.uk/download/
You can download Raspbian here: https://www.raspberrypi.org/downloads/raspbian/

To install them follow the guides on their sites.

After you have the Operating system running then we can start to install our script:


For installing all of this you need to open the so called terminal. When you use RetroPie then you can access it (after EmulationStation has started) by clicking F4. If you use other Debian based operating systems like Raspbian please have a look at the official docs on how to open the terminal.
Before we start please make sure that your raspberry is connected to the internet.

From now on we will work in the terminal. I will tell you some commands and you just have to write them into the commandline and hit enter. You will see a line that looks something like this **pi@retropie:~ $**  and a blinking cursor. This means that the system is ready and you can give it commands. When you will install something please wait until you see that line again. Sometimes the system will ask you if you really want to install something, when this happens then click the y-Button and hit enter. 


Okay now lets start to install the kintaro package.

Type in the command **sudo wget -O - https://www.goo.gl/22RsN3 | bash** and hit enter. This will start the installation.

After that restart the raspberry

The whole kintaro team hopes you have a lot of fun with our product.


### Deinstalling

If you need to unistall the script please type: "sudo dpkg -r pcb"


### How to change the options

The package is controlled by the kintaro.config file in the folder /opt/kintaro/start

if you want to change it type: sudo nano /opt/kintaro/start/kintaro.config

then change the options you need and save your changes with ctrl+o and hit enter

after that type: sudo reboot to restart the console with the new settings


### How the package works and how to hack around with it: 

The intro movie and picture are store in the folder /opt/kintaro/start. If you want to have your own just change the files kintaro.png or intro.mp4 to your files.

If you want to change the basic functionality (for example the fan controll) then have a look at the pcb.py script in the folder /opt/kintaro/

If you want to stop the script type: systemctl stop kintaro.service

If you dont want the script to run on bootup then type: systemctl disable kintaro.service

## Contributing

If you have a cool new option for our package feel free to open a pull request.


## Authors

* **Michael Kirsch** - *Initial work*

See also the list of [contributors](https://github.com/michaelkirsch/contributors) who participated in this project.

## License

This project is licensed under the MIT License - see the [LICENSE.md](LICENSE.md) file for details

