from datetime import datetime
import pyvisa as visa


class ITC4001:
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
            self.resource.write("*RST")

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
        info = self.query("*IDN?").strip().split(",")[:4]
        print(datetime.now(), info[0], info[1])
        print(datetime.now(), "serial number:", info[2])
        revision = info[3].split("/")
        print(datetime.now(), "instrument firmware revision:", revision[0])
        print(datetime.now(), "front panel board firmware revision:", revision[1])
        print(datetime.now(), "temperature controller board firmware revision:", revision[2])

    def set_temp(self, temp: float):
        # set TEC temperature
        self.write("SOUR2:TEMP " + str(temp) + "C")
        # query TEC temperature
        res = self.query("SOUR2:TEMP?")
        if abs(float(res) - temp) < 0.0005:
            # set succeed
            return True
        return False
