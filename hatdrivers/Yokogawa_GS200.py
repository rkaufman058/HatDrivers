# -*- coding: utf-8 -*-
"""
Created on Wed Jun 24 15:39:29 2020

@author: Ryan Kaufman
"""


#The Qcodes driver does pretty much everything I need it to, 
#the problem is that it's not formatted like we used to have it
#So this driver will subclass the qcodes driver 
#(at: https://github.com/QCoDeS/Qcodes/blob/master/qcodes/instrument_drivers/yokogawa/GS200.py)
#and just add a few things that we used before

from qcodes.instrument_drivers.yokogawa.GS200 import GS200
import numpy as np

class YOKO(GS200): 
    
    def __init__(self,name: str, address: str = None, terminator: str = "\n", **kwargs):
        if address == None:
            raise Exception('TCPIP Address needed')
        super().__init__(name, address, terminator = terminator, **kwargs)
        #the driver assumes you just turned on the YOKO, and it's in voltage mode. This is almost never the case
        #for us so this sequence changes that assumption to currents instead of voltages
        self._cached_mode = "CURR"
        self.output_level = self.current # the whole parameter, not just one value
        
        self._cached_range_value = self.current_range()
        
        
    def change_current(self,new_curr):
        #if the difference is less than a milliamp, the steps will be 0.1uA, otherwise, 1uA
        #the net rate will be the same either way: but limited by the TCPIP transfer speed of the YOKO in the 0.1uA case
        old_curr = self.current()
        if np.abs(new_curr-old_curr) > 1e-3: 
            rate = 1e-4 #A/s
            step = 1e-6
            delay = step/rate
            self.ramp_current(new_curr, step, delay)
        else: 
            rate = 1e-4 #A/s
            step = 1e-7
            delay = step/rate #I suspect this is too fast for the TCP protocol to keep up
            self.ramp_current(new_curr, step, delay)
            
    def bump(self, bump): 
        old = self.current()
        new = old + bump
        self.change_current(new)