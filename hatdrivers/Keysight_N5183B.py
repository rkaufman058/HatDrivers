# -*- coding: utf-8 -*-
"""
Created on Wed Jun 24 14:03:04 2020

A driver to control the Keysight MXG Analog Signal Generator N5183B using QCodes

#original driver by Erick Brindock for Qtlab

@author: Hatlab - Ryan Kaufman - rewritten for QCodes

"""
import types
import logging
import numpy as np
import time
from qcodes import (Instrument, VisaInstrument,
                    ManualParameter, MultiParameter,
                    validators as vals)

class Keysight_N5183B(VisaInstrument):
    #startup, setting all of the parameters, confirming connection
    def __init__(self, name, address = None, **kwargs): 
        
        if address == None:
            raise Exception('TCPIP Address needed')
            
        logging.info(__name__ + ' : Initializing instrument Agilent_E5071C')
        
        super().__init__(name, address, terminator = '\n', **kwargs)
        
        #add all parameters from old driver
        self.add_parameter('output_status', 
                           get_cmd = 'OUTP?', 
                           set_cmd = 'OUTP {}', 
                           vals = vals.Ints(0,1), 
                           get_parser = int
                           )
        self.add_parameter('frequency', 
                           get_cmd = 'FREQ:CW?', 
                           set_cmd = 'FREQ:CW {}', 
                           vals = vals.Numbers(1, 20e9), 
                           get_parser = float,
                           unit = 'Hz'
                           )
        self.add_parameter('reference_source', 
                           get_cmd = 'ROSC:SOUR?', 
                           set_cmd = 'ROSC:SOUR {}', 
                           vals = vals.Enum('INT','EXT'), 
                           get_parser = str
                           )
        self.add_parameter('alc_auto', 
                           get_cmd = 'POW:ATT:AUTO?', 
                           set_cmd = 'POW:ATT:AUTO {}', 
                           vals = vals.Ints(0,1), 
                           get_parser = int
                           )
        self.add_parameter('phase_adjust', 
                           get_cmd = 'PHAS:ADJ?', 
                           set_cmd = 'PHAS:ADJ {}', 
                           vals = vals.Numbers(), 
                           get_parser =float, 
                           unit = 'Hz'
                           )
        self.add_parameter('power', 
                           get_cmd = 'POW?', 
                           set_cmd = 'POW {}DB', 
                           vals = vals.Numbers(-20, 20), 
                           get_parser = float, 
                           unit = 'dBm'
                           )
        self.add_parameter('power_mode', 
                           get_cmd = 'POW:MODE?', 
                           set_cmd = 'POW:MODE {}', 
                           vals = vals.Enum('CW', 'FIX', 'LIST'), 
                           get_parser = str
                           )
        self.add_parameter('power_start', 
                           get_cmd = 'POW:STAR?', 
                           set_cmd = 'POW:STAR {}DB', 
                           vals = vals.Numbers(-20,20), 
                           get_parser = float, 
                           unit = 'dBm'
                           )
        self.add_parameter('power_stop',
                           get_cmd = 'POW:STOP?', 
                           set_cmd = 'POW:STOP {}DB', 
                           vals = vals.Numbers(-20,20), 
                           get_parser = float, 
                           unit = 'dBm'
                           )
        self.add_parameter('mod_status',
                           get_cmd = 'OUTP_MOD?', 
                           set_cmd = 'OUTP:MOD {}', 
                           vals = vals.Ints(0,1), 
                           get_parser = int
                           )
        self.add_parameter('frequency_mode',
                           get_cmd = 'FREQ:MODE?', 
                           set_cmd = 'FREQ:MODE {}',
                           vals = vals.Enum('CW', 'FIX', 'LIST'), 
                           get_parser = str
                           )
        self.add_parameter('sweep_generation_type',
                           get_cmd = 'SWE:GEN?', 
                           set_cmd = 'SWE:GEN {}', 
                           vals = vals.Enum('ANAL', 'STEP'), 
                           #Analog and stepped, respectively...
                           #theres no way the engineers weren't 
                           #chuckling to themselves when they programmed this 
                           get_parser = str
                           )
        self.add_parameter('frequency_start',
                           get_cmd = 'FREQ:STAR?', 
                           set_cmd = 'FREQ:STAR {}', 
                           vals = vals.Numbers(1, 20e9), 
                           get_parser = float,
                           unit = 'Hz'
                           )
        self.add_parameter('frequency_stop',
                           get_cmd = 'FREQ:STOP?', 
                           set_cmd = 'FREQ:STOP {}', 
                           vals = vals.Numbers(1, 20e9), 
                           get_parser = float,
                           unit = 'Hz'
                           )
        self.add_parameter('dwell_time',
                           get_cmd = 'SWE:DWEL?', 
                           set_cmd = 'SWE:DWEL {}', 
                           vals = vals.Numbers(), 
                           get_parser = float,
                           unit = 's'
                           )
        self.add_parameter('sweep_spacing',
                           get_cmd = 'SWE:SPAC?', 
                           set_cmd = 'SWE:SPAC {}', 
                           vals = vals.Enum('LIN','LOG'), 
                           get_parser = str
                           )
        self.add_parameter('sweep_points',
                           get_cmd = 'SWE:POIN?', 
                           set_cmd = 'SWE:POIN {}', 
                           vals = vals.Ints(1), 
                           get_parser = int
                           )
        self.add_parameter('sweep_direction',
                           get_cmd = 'LIST:DIR?', 
                           set_cmd = 'LIST:DIR {}', 
                           vals = vals.Enum('UP','DOWN'), 
                           get_parser = str
                           )
        self.add_parameter('sweep_type',
                           get_cmd = 'LIST:TYPE?', 
                           set_cmd = 'LIST:TYPE {}', 
                           vals = vals.Enum('LIST', 'STEP'), 
                           get_parser = str
                           )
        self.add_parameter('sweep_step',
                           get_cmd = 'SWE:STEP?', 
                           set_cmd = 'SWE:STEP {}Hz', 
                           vals = vals.Numbers(0), 
                           get_parser = float, 
                           unit = 'Hz'
                            )
        self.add_parameter('trigger_source',
                           get_cmd = 'LIST:TRIG:SOUR?', 
                           set_cmd = 'LIST:TRIG:SOUR {}', 
                           vals = vals.Enum('BUS', 'IMM', 'EXT', 'INT', 'KEY', 'TIM'),
                           # Sets the trigger source for a list or step sweep event
                           # source (str) : BUS | IMMediate | EXTernal | INTernal | KEY | TIMer
                           get_parser = str
                           )
        self.add_parameter('trigger_wait_time',
                           get_cmd = 'TRIG:TIM?', 
                           set_cmd = 'TRIG:TIM {}s', 
                           vals = vals.Numbers(0), 
                           get_parser = float, 
                           unit = 's'
                           )
        self.add_parameter('retrace', 
                           get_cmd = 'LIST:RETR?', 
                           set_cmd = 'LIST:RETR {}', 
                           vals = vals.Ints(0,1), 
                           get_parser = int
                          )
        self.connect_message()

#Begin the custom functions, these are pretty much copied from Erick's code:
    def send_instruction(self, instruction):
        '''
        Sends a command to the instrument
            Input:
                command (string) : command to be sent (see manual for commands)
        '''
        self._visainstrument.write(instruction)
    def retrieve_data(self, query):
        '''
        Reads data from the instrument
            Input:
                query (string) : command to be sent (see manual for commands)
            Output:
                varies depending on command sent
        '''
        return self._visainstrument.ask(query)
    def reset(self):
        '''
        Reset to default state
        '''
        self._visainstrument.write('*RST')
        
    def get_all(self):

        self.output_status()
        self.frequency()
        self.reference_source()
        self.alc_auto()
        self.phase_adjust()
        self.power()
        self.power_mode()
        self.power_start()
        self.power_stop()
        self.mod_status()
        self.frequency_mode()
        self.sweep_type()
        self.frequency_start()
        self.frequency_stop()
        self.dwell_time()
        self.sweep_spacing()
        self.sweep_points()
        self.sweep_direction()
        self.sweep_type()
        self.sweep_step()