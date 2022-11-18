# -*- coding: utf-8 -*-

from Instrument import VISAInstrument
from Logger import Logger
import sys

if __name__ == "__main__":
    sys.stdout = Logger()

    # mgr = visa.ResourceManager()
    # print(mgr.list_resources())
    visaResource = 'USB0::0x1313::0x804A::M00482881::INSTR'
    dev = VISAInstrument(visaResource)
