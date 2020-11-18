# -*- coding: utf-8 -*-
"""
Created on Thu Jul 30 14:20:10 2020

@author: Ryan Kaufman

Description - 
A metainstrument for a mode on a device. facilitates acquisition
"""
import types
import logging
import numpy as np
import time
from qcodes import (Instrument, VisaInstrument,
                    ManualParameter, MultiParameter,
                    validators as vals, Station)
import instrumentserver.serialize as ser
import easygui 
import os

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
                           set_cmd = None)
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
        self.add_parameter('gen_power', 
                           set_cmd = None, 
                           # initial_value = par_dict['power'], 
                           vals = vals.Numbers(), 
                           unit = 'dBm'
                           )
        self.add_parameter('gen_frequency', 
                           set_cmd = None, 
                           # initial_value = par_dict["frequency"],
                           vals = vals.Numbers(0),
                           unit = 'Hz'
                           )
        self.add_parameter('trace', 
                           set_cmd = None)
        
                           
        
    def pull(self, VNA = None, SWT = None, CS = None, Gen = None): #this needs to be the whole damn instrument
        if VNA != None: 
            print(f"pulling from: {VNA}")
            self.fcenter(VNA.fcenter())
            self.span(VNA.fspan())
            self.electrical_delay(VNA.electrical_delay())
            self.power(VNA.power())
            self.phase_offset(VNA.phase_offset())
            self.ifbw(VNA.ifbw())
            self.avgnum(VNA.avgnum())
        if SWT != None:
            print("pulling from: "+str(SWT))
            self.mode_dict(list(SWT.portvalue()))
        if CS != None:
            print(f"pulling from: {CS}")
            self.bias_current(CS.current())
        if Gen != None: 
            print(f"pulling from: {Gen}")
            self.gen_frequency(Gen.frequency())
            self.gen_power(Gen.power())
    
    def push(self, VNA = None, SWT = None, Gen = None, CS = None):
        if VNA != None: 
            if self.fcenter() != None: 
                VNA.fcenter(self.fcenter())
            if self.span() != None:
                VNA.fspan(self.span())
            if self.electrical_delay() != None: 
                VNA.electrical_delay(self.electrical_delay())
            if self.power() != None: 
                VNA.power(self.power())
            if self.phase_offset() != None:
                VNA.phase_offset(self.phase_offset())
            if self.ifbw() != None: 
                VNA.ifbw(self.ifbw())
            if self.avgnum() != None: 
                VNA.avgnum(self.avgnum())
                VNA.averaging(1)
        if SWT != None and self.mode_dict()!= None: 
            SWT.modes[self.name] = self.mode_dict()
            SWT.set_mode_dict(self.name)
        if Gen != None and self.gen_power() != None and self.gen_frequency() != None: 
            Gen.power(self.gen_power())
            Gen.frequency(self.gen_frequency())
        if CS != None and self.bias_current() != None: 
            CS.change_current(self.bias_current())
        
    def print(self):
        return ser.toParamDict([self])
    
    def save(self, cwd = None):
        if cwd == None: 
            cwd = easygui.diropenbox()
        ser.saveParamsToFile([self], cwd+'\\'+self.name+'.txt')
        
    def load(self, filepath = None): 
        if filepath == None: 
            filepath = easygui.fileopenbox()
        ser.loadParamsFromFile(filepath, [self])
        
    def savetrace(self, VNA, cwd = None, avgnum = 1):
        self.push_to_VNA(VNA)
        self.pull_from_VNA(VNA)
        if cwd == None: 
            cwd = easygui.diropenbox()
        ser.saveParamsToFile([self], cwd+'\\'+self.name+'.txt')
        VNA.savetrace(avgnum = avgnum, savedir = cwd+'\\'+self.name+'_trace.h5')

def load_from_folder(namespace, path = None):
    if path == None: 
            path = easygui.diropenbox()
    assert path != None
    for modefile in os.listdir(path):
        name = modefile.split(".")[0]
        mode_init = mode(name)
        mode_init.load(filepath = path+"\\"+modefile)
        namespace[name] = mode_init
        
        print(modefile)
        
    
    