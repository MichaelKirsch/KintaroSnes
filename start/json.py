import configparser
import sys, getopt


def main(argv):
    try:
        opts, args = getopt.getopt(argv, "v:s:", ["value=", "set="])
    except getopt.GetoptError:
        pass
    val1=""
    val2=""
    for opt, arg in opts:
        if opt in ("-v", "--value"):
            val1 = arg
        if opt in ("-s", "--set"):
            val2 = arg
    change_value(val1, val2)

if __name__ == "__main__":
    main(sys.argv[1:])


def change_value(value, set_to):  # change one of the values in the config file
    parser = configparser.ConfigParser()
    parser.read("/opt/kintaro/start/kintaro.config")
    parser.set('Boot', value, set_to)
    with open("/opt/kintaro/start/kintaro.config", "w+") as configfile:
        parser.write(configfile)
