# -*- coding: utf-8 -*-

import pyvisa as visa
from ITC4001 import ITC4001
from Logger import Logger
import sys
import time
import getopt
import csv
import numpy as np
from Timer import Timer
from datetime import datetime

# communication timeout with ITC4001 (ms)
TIMEOUT = 5000
# retry times when tec temperature set failed
RETRY_TIMES = 5
# waiting time for TEC start status (s)
WAITING_TIME = 20
# interval of tunning file data (ms)
INTERVAL = 100
# whether save tunning log
TUNNING_LOG = True
# whether reset the instrument while initialization
RESET = False
# whether reset the instrument after tunning
RESET_END = False
# 中心波长1550.12nm
# 15.375℃ ~ 1550.08346nm
# 22.030℃ ~ 1550.15647nm
# 20.146℃ ~ 1550.15647nm


def parse_file(filename: str):
    data = np.loadtxt(filename, dtype=np.float32, delimiter=",").tolist()
    for i in range(len(data)):
        data[i] = round(data[i], 5)
    return data


def tunning(data: list, instrument: ITC4001):

    def get_temp():
        if len(data) < 1:
            timer.stop()
            return -1
        t = data[0]
        data.pop(0)
        return t

    def set_temp():
        t = get_temp()
        if t == -1:
            timer.stop()
            # TEC OFF
            print(datetime.now(), "tunning finished")
            if RESET_END:
                print(datetime.now(), "set TEC OFF")
                instrument.write("OUTP2 OFF")
            return
        for __ in range(RETRY_TIMES):
            if instrument.set_temp(t):
                if TUNNING_LOG:
                    with open(str(datetime.now()).split(" ")[0] + ".csv", "a", encoding="utf-8-sig", newline="") as f:
                        writer = csv.writer(f)
                        writer.writerow([str(datetime.now()), t])
                return

    # set start status
    print(datetime.now(), "initialize TEC temperature", data[0])
    instrument.set_temp(data[0])
    # TEC ON
    print(datetime.now(), "set TEC ON")
    instrument.write("OUTP2 ON")
    time.sleep(WAITING_TIME)

    # start tunning
    timer = Timer(set_temp, INTERVAL)
    timer.start()


if __name__ == "__main__":

    sys.stdout = Logger()

    try:
        opts, args = getopt.getopt(sys.argv[1:], "hlr:f:c:", ["help", "list", "resource=", "file=", "command="])
    except getopt.GetoptError:
        print("wrong args")
        print("Please running with -h, --help for using guidance")
        exit(2)

    if len(opts) < 1:
        print("Please running with -h, --help for using guidance")
        exit(0)

    visaResource = None
    tunningFile = None
    command = None
    for opt, arg in opts:
        if opt in ("-h", "--help"):
            print("-l, --list\n\tlist all visa resources")
            print("-r A::B::C, --resource A::B::C\n\tconnect ITC4001 at A::B::C")
            print("-f FILE, --file FILE\n\ttunning ITC4001 with FILE")
            exit(0)
        elif opt in ("-l", "--list"):
            print(visa.ResourceManager().list_resources())
            exit(0)
        elif opt in ("-r", "--resource"):
            visaResource = arg
        elif opt in ("-f", "--file"):
            tunningFile = arg
        elif opt in ("-c", "--command"):
            command = arg

    if visaResource == None or tunningFile == None:
        print("no resource or file input")
        print("Please running with -h, --help for using guidance")
        if command == None:
            exit(0)

    if command == None:
        print(datetime.now(), "Preparing for tunning", tunningFile, "with", INTERVAL, "ms interval at", visaResource)

    try:
        instrument = ITC4001(visaResource, TIMEOUT, RESET)
    except BaseException as e:
        print(e)
        exit(0)

    if not (command == None):
        print(datetime.now(), "excuting command:", command)
        print(instrument.command(command))
        exit(0)

    tunningData = parse_file(tunningFile)
    tunning(tunningData, instrument)
