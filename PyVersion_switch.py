import os
import argparse

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--v', help='the python version you want to use')
    args = parser.parse_args()
    command_0 = "sudo rm /usr/bin/python"
    if args.v == "3":
        command_1 = "sudo ln -s /usr/bin/python3.5  /usr/bin/python"
    if args.v == "2":
        command_1 = "sudo ln -s /usr/bin/python2.7 /usr/bin/python"
    os.system(command_0)
    os.system(command_1)
