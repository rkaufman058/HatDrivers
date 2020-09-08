# -*- coding: utf-8 -*-
"""
Created on Thu Jul 30 14:20:10 2020

@author: Ryan Kaufman

Description - 
A metainstrument for a mode on a device. facilitates acquisition, sweeping, and fitting
"""
import types
import logging
import numpy as np
import time
from qcodes import (Instrument, VisaInstrument,
                    ManualParameter, MultiParameter,
                    validators as vals)
import instrumentserver.serialize as ser
import easygui 

class mode(Instrument): 
    
    def __init__(self, name, **kwargs) -> None: 
        super().__init__(name, **kwargs)
        
        self.add_parameter('fcenter', 
                           set_cmd = None, 
                           # initial_value = par_dict["frequency"],
                           vals = vals.Numbers(0),
                           unit = 'Hz'
                           )
        self.add_parameter('bandwidth', 
                           set_cmd = None, 
                           # initial_value = par_dict["bandwidth"],
                           vals = vals.Numbers(0),
                           unit = 'Hz'
                           )
        self.add_parameter('span', 
                           set_cmd = None, 
                           # initial_value = par_dict["span"],
                           vals = vals.Numbers(0),
                           unit = 'Hz'
                           )
        self.add_parameter('power',
                           set_cmd = None, 
                           # initial_value = par_dict['power'], 
                           vals = vals.Numbers(), 
                           unit = 'dBm'
                           )
        self.add_parameter('electrical_delay', 
                           set_cmd = None, 
                           # initial_value = par_dict["electrical_delay"],
                           vals = vals.Numbers(0),
                           unit = 's'
                           )
        self.add_parameter('mode_dict', 
                           set_cmd = None, 
                           # initial_value = par_dict["mode_dict"],
                           vals = vals.Strings()
                           )
        self.add_parameter('phase_offset', 
                           set_cmd = None, 
                           # initial_value = par_dict["phase_offset"], 
                            vals = vals.Numbers(),
                           unit = 'Deg'
                           )
        self.add_parameter('bias_current', 
                           vals = vals.Numbers(),
                           set_cmd = None,
                           unit = 'A')
        self.add_parameter('ifbw', 
                           vals = vals.Numbers(),
                           set_cmd = None,
                           unit = 'Hz')
        self.add_parameter('avgnum', 
                           vals = vals.Numbers(),
                           set_cmd = None,
                           unit = 'Hz')
        
    def pull_from_VNA(self, VNA): #this needs to be the whole damn instrument
        self.fcenter(VNA.fcenter())
        self.span(VNA.fspan())
        self.electrical_delay(VNA.electrical_delay())
        self.power(VNA.power())
        self.phase_offset(VNA.phase_offset())
        self.ifbw(VNA.ifbw())
        self.avgnum(VNA.avgnum())
    
    def pull(self, VNA = None, CS = None, Gen1 = None, Gen2 = None): #TODO: make general way of recording all instruments into here
        return None
    
    def push_to_VNA(self, VNA, SWT = None):
        if self.fcenter() != None: 
            VNA.fcenter(self.fcenter())
        if self.span() != None:
            VNA.fspan(self.span())
        if self.electrical_delay() != None: 
            VNA.electrical_delay(self.electrical_delay())
        if self.power() != None: 
            VNA.power(self.power())
        if self.mode_dict() != None and SWT != None: 
            SWT.set_mode_dict(self.mode_dict())
        if self.phase_offset() != None:
            VNA.phase_offset(self.phase_offset())
        if self.ifbw() != None: 
            VNA.ifbw(self.ifbw())
        if self.avgnum() != None: 
            VNA.avgnum(self.avgnum())
            VNA.averaging(1)
        
    def print(self):
        return ser.toParamDict([self])
    
    def save(self, cwd = None):
        if cwd == None: 
            cwd = easygui.diropenbox()
        ser.saveParamsToFile([self], cwd+'\\'+self.name+'.txt')
        
    def load(self, filepath = None): 
        if filepath == None: 
            filepath = easygui.fileopenbox()
        ser.loadParamsFromFile()
    def savetrace(self, VNA, cwd = None, avgnum = 1):
        self.push_to_VNA(VNA)
        self.pull_from_VNA(VNA)
        if cwd == None: 
            cwd = easygui.diropenbox()
        ser.saveParamsToFile([self], cwd+'\\'+self.name+'.txt')
        VNA.savetrace(avgnum = avgnum, savedir = cwd+'\\'+self.name+'_trace.h5')
        