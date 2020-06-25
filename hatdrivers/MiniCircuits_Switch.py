# -*- coding: utf-8 -*-
"""
Created on Wed Jun 24 19:45:01 2020

@author: Ryan Kaufman, modifying work of Xi Cao for the original qtlab

"""

import ctypes
import types
import logging
import types
import logging
import numpy as np
import time
from qcodes import (Instrument, VisaInstrument,
                    ManualParameter, MultiParameter,
                    validators as vals)
import logging
import urllib2

#switch_address = 'http://169.254.47.255'
class MiniCircuits_Switch(Instrument):

    def __init__(self, name, address, reset=False):
        '''
        Initializes the Mini_Circuits switch, and communicates with the wrapper.

        Input:
          name (string)    : name of the instrument
          address (string) : http address
          reset (bool)     : resets to default values, default=False
        '''
        logging.info(__name__ + ' : Initializing instrument Mini_CircuitsSwitch')
        super().__init__(self, name)

        # Add some global constants
        self._address = address
        
        self.add_parameter('portvalue',
                           get_cmd = self.do_get_portvalue(), 
                           set_cmd = None, 
                           get_parser = str)

    def get_all(self):
        '''
        Reads all implemented parameters from the instrument,
        and updates the wrapper.
        SSWT
        Input:
            None

        Output:
            None
        '''
        logging.info(__name__ + ' : get all')
        #self.get_runningstate()
        
        self.get_portvalue()

    def set_switch(self,sw,state):
        '''
        sw: switch A through H or P if you want to control all the gates at same time
        state: 0 or 1 to choose output. 0=1 (green), 1=2 (red)        
        
        '''
        logging.info(__name__ + ' : Set switch%s' % sw +' to state %s' % state)
        if sw != 'P':
            ret = urllib2.urlopen(self._address + "/SET" + sw + "=" + state)
        else:
            if (len(state)) != 8:
                print len(state)
                raise Exception("Wrong input length!")
            newstate = 0
            for x in range(0,len(state)):
                if (int(state[x]) != 0) & (int(state[x]) != 1):
                    raise Exception("Wrong input value at %ith" % x + " switch!")
                else:
                    newstate += int(state[x])*(2**x)
            
  
            ret = urllib2.urlopen(self._address + "/SETP" + "=" + str(newstate))

        status = ret.readlines()[0]
        if status != '1':
            raise Exception("Switch didn't switch!")
        else:
            self.get('portvalue')

        
    def do_get_portvalue(self):
        logging.debug(__name__+' : get portvalue')
        ret = urllib2.urlopen(self._address + "/SWPORT?" )
        result = ret.readlines()[0]
        result = int(result)
        result = format(result,'08b')
        result = result[::-1]
        return result
