from datetime import datetime
import pyvisa as visa


class VISAInstrument:
    manufacturer = 'USTC'
    model = 'VISAInstrument'

    def __init__(self, resourceID, timeout=5000, channel=1):
        self.resourceID = resourceID
        self.channelCount = channel
        # connect
        try:
            self.resource = visa.ResourceManager().open_resource(resourceID)
            self.resource.timeout = timeout
        except BaseException as e:
            print('Error in open device ID: {}'.format(id), e)
        # reset
        self.resource.write("*RST")
        # instrument infomation
        print(datetime.now(), self.query("*IDN?").strip().replace(",", " "), "connected.")

    def write(self, command):
        return self.resource.write(command)

    def query(self, command):
        return self.resource.query(command)

    def print_info(self):
        # print instrument info
        info = self.query("*IDN?").strip().split(",")[:4]
        print(datetime.now(), info[0], info[1])
        print(datetime.now(), "serial number:", info[2])
        revision = info[3].split("/")
        print(datetime.now(), "instrument firmware revision:", revision[0])
        print(datetime.now(), "front panel board firmware revision:", revision[1])
        print(datetime.now(), "temperature controller board firmware revision:", revision[2])
