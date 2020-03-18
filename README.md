## Version 4.0.0

Im not working for Kintaro. This software is maintained in my freetime. So please help me out when you find problems and open pull requests

## Installing on Raspbian/Retropie

BOTH COMMANDS ARE NEEDED! ERRORS AFTER THE FIRST ONE REGARDING MISSING PACKAGES ARE OKAY! Second command will fix that

**sudo dpkg -i kintarosnes.deb**

**sudo apt-get install -f**

## Packaging

for packaging use the fpm **https://github.com/jordansissel/fpm** and then run folling command to get a .deb package: 

 fpm --log error --after-install install.sh --after-remove  uninstall.sh --architecture armhf --name kintarosnes --version x.x.x -s dir -t deb --vendor Michael --description "Kintaro SNES PCB Driver"  -d python-rpi.gpio -d python3-dialog -d python3-rpi.gpio .
 
## Authors

* **Michael Kirsch** - *Initial work*

See also the list of [contributors](https://github.com/michaelkirsch/contributors) who participated in this project.

## License

This project is licensed under the MIT License - see the [LICENSE.md](LICENSE.md) file for details

