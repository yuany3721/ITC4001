from VISAInstrument import VISAInstrument
from datetime import datetime


class ITC4001(VISAInstrument):

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
