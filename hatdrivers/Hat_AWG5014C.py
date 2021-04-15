# -*- coding: utf-8 -*-
"""
Created on Thu Apr 15 10:47:49 2021

@author: Ryan Kaufman

Thsi dirver is mostly going to be the qcodes driver, with parameters added in for channel skew, amplitude, and offset 
that allow us to rapidly tune the mixer leakage and such. 

"""
from qcodes import (Instrument, VisaInstrument,
                    ManualParameter, MultiParameter,
                    validators as vals)
from qcodes.instrument_drivers.tektronix.AWG5014 import Tektronix_AWG5014
class Hat_AWG5014C(Tektronix_AWG5014): 
    
    def __init__(self,name: str, address: str = None, terminator: str = "\n", **kwargs):
        if address == None:
            raise Exception('TCPIP Address needed')
        super().__init__(name, address, terminator = terminator, **kwargs)
        
        self.add_parameter('ch1offset', 
                           get_cmd = 'SOURCE1:VOLTAGE:LEVEL:IMMEDIATE:OFFSET?', 
                           set_cmd = 'SOURCE1:VOLTAGE:LEVEL:IMMEDIATE:OFFSET {}', 
                           vals = vals.Numbers(), 
                           get_parser = float
                           )
        
        self.add_parameter('ch2offset', 
                           get_cmd = 'SOURCE2:VOLTAGE:LEVEL:IMMEDIATE:OFFSET?', 
                           set_cmd = 'SOURCE2:VOLTAGE:LEVEL:IMMEDIATE:OFFSET {}', 
                           get_parser = float, 
                           vals = vals.Numbers()
                           )
        self.add_parameter('ch3offset', 
                           get_cmd = 'SOURCE3:VOLTAGE:LEVEL:IMMEDIATE:OFFSET?', 
                           set_cmd = 'SOURCE3:VOLTAGE:LEVEL:IMMEDIATE:OFFSET {}', 
                           get_parser = float, 
                           vals = vals.Numbers()
                           )
        self.add_parameter('ch4offset', 
                           get_cmd = 'SOURCE4:VOLTAGE:LEVEL:IMMEDIATE:OFFSET?', 
                           set_cmd = 'SOURCE4:VOLTAGE:LEVEL:IMMEDIATE:OFFSET {}', 
                           get_parser = float, 
                           vals = vals.Numbers()
                           )
        
        self.add_parameter('ch1skew', 
                           get_cmd = 'SOURCE1:SKEW?', 
                           set_cmd = 'SOURCE1:SKEW {} NS', 
                           get_parser = float, 
                           vals = vals.Numbers()
                           )
        self.add_parameter('ch2skew', 
                           get_cmd = 'SOURCE2:SKEW?', 
                           set_cmd = 'SOURCE2:SKEW {} NS', 
                           get_parser = float, 
                           vals = vals.Numbers()
                           )
        self.add_parameter('ch3skew', 
                           get_cmd = 'SOURCE3:SKEW?', 
                           set_cmd = 'SOURCE3:SKEW {} NS', 
                           get_parser = float, 
                           vals = vals.Numbers()
                           )
        self.add_parameter('ch4skew', 
                           get_cmd = 'SOURCE4:SKEW?', 
                           set_cmd = 'SOURCE4:SKEW {} NS', 
                           get_parser = float, 
                           vals = vals.Numbers()
                           )
        self.add_parameter('ch1amp', 
                           get_cmd = 'SOURCE1:VOLTAGE:AMPLITUDE?', 
                           set_cmd = 'SOURCE1:VOLTAGE:AMPLITUDE {}', 
                           vals = vals.Numbers(), 
                           get_parser = float
                           )
        
        self.add_parameter('ch2amp', 
                           get_cmd = 'SOURCE2:VOLTAGE:AMPLITUDE?', 
                           set_cmd = 'SOURCE2:VOLTAGE:AMPLITUDE {}', 
                           vals = vals.Numbers(), 
                           get_parser = float
                           )
        self.add_parameter('ch3amp', 
                           get_cmd = 'SOURCE3:VOLTAGE:AMPLITUDE?', 
                           set_cmd = 'SOURCE3:VOLTAGE:AMPLITUDE {}', 
                           vals = vals.Numbers(), 
                           get_parser = float
                           )
        self.add_parameter('ch4amp', 
                           get_cmd = 'SOURCE4:VOLTAGE:AMPLITUDE?', 
                           set_cmd = 'SOURCE4:VOLTAGE:AMPLITUDE {}', 
                           vals = vals.Numbers(), 
                           get_parser = float
                           )