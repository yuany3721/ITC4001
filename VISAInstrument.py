import pyvisa as visa
from datetime import datetime


class VISAInstrument(object):
    manufacturer = 'USTC'
    model = 'VISAInstrument'

    def __init__(self, resourceID: str, timeout: int, reset: bool):
        self.resourceID = resourceID
        # connect
        try:
            self.resource = visa.ResourceManager().open_resource(resourceID)
            self.resource.timeout = timeout
        except BaseException as e:
            print('Error in open device at: {}'.format(resourceID), e)
        # instrument infomation
        print(datetime.now(), self.query("*IDN?").strip().replace(",", " "), "connected.")
        # reset
        if reset:
            self.reset()

    def reset(self):
        self.resource.write("*RST")
        print(datetime.now(), "resource reset")

    def write(self, command: str):
        return self.resource.write(command)

    def query(self, command: str):
        return self.resource.query(command)

    def command(self, command: str):
        if command.endswith("?"):
            return self.query(command)
        else:
            return self.write(command)

    def print_info(self):
        # print instrument info
        info = self.query("*IDN?")
        print(datetime.now(), info)
