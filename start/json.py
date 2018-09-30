#!/usr/bin/python3
#Copyright 2018 Michael Kirsch

#Permission is hereby granted, free of charge, to any person obtaining a copy of this software and associated documentation files (the "Software"),
#to deal in the Software without restriction, including without limitation the rights to use, copy, modify, merge, publish, distribute, sublicense,
# and/or sell copies of the Software, and to permit persons to whom the Software is furnished to do so, subject to the following conditions:
#The above copyright notice and this permission notice shall be included in all copies or substantial portions of the Software.

import configparser
import sys, getopt

def change_value(value, set_to):  # change one of the values in the config file
    parser = configparser.ConfigParser()
    parser.read("/opt/kintaro/start/kintaro.config")
    parser.set('Boot', value, set_to)
    with open("/opt/kintaro/start/kintaro.config", "w+") as configfile:
        parser.write(configfile)


def main(argv):
    try:
        opts, args = getopt.getopt(argv, "v:s:")
    except getopt.GetoptError:
        pass
    val1=""
    val2=""
    for opt, arg in opts:
        if opt in ("-v"):
            val1 = arg
            print (val1)
        if opt in ("-s"):
            print (arg)
            val2 = arg

    change_value(val1, val2)

if __name__ == "__main__":
    main(sys.argv[1:])


