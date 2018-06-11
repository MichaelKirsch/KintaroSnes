## Version 2.7.2


## Packaging

for packaging use the fpm **https://github.com/jordansissel/fpm** and then run folling command to get a .deb package: 

 fpm --log error --after-install install.sh --after-remove  uninstall.sh --architecture armhf --name kintarosnes --version x.x.x -s dir -t deb --vendor Michael --description "Kintaro SNES PCB Driver"  -d python-rpi.gpio -d python3-dialog -d python3-rpi.gpio .

Our packages are hosted on packagecloud.
 
 
## Authors

* **Michael Kirsch** - *Initial work*

See also the list of [contributors](https://github.com/michaelkirsch/contributors) who participated in this project.

## License

This project is licensed under the MIT License - see the [LICENSE.md](LICENSE.md) file for details

