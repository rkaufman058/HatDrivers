
# MJH 2015_10_15.. Maybe this will work??
#Additions by Alex
#average method by Erick Brindock  7/15/16
#driver rewritten by Ryan Kaufman 06/11/20 for Qcodes
#YR: also, here is keysights manual,http://ena.support.keysight.com/e5071c/manuals/webhelp/eng/
#you want the programming -> remote control part for VISA commands

import visa
import types
import logging
import numpy as np
import time
from qcodes import (Instrument, VisaInstrument,
                    ManualParameter, MultiParameter,
                    validators as vals)
#from pyvisa.visa_exceptions import VisaIOError
#triggered=[False]*159 

class Agilent_ENA_5071C(VisaInstrument):
    '''
    This is the driver for the Agilent E5071C Vector Netowrk Analyzer

    Usage:
    Initialize with
    <name> = instruments.create('<name>', 'Agilent_E5071C', 
    address='<GBIP address>, reset=<bool>')
    '''
    
    def __init__(self, name, address = None, **kwargs):
        '''
        Initializes the Agilent_E5071C, and communicates with the wrapper.

        Input:
          name (string)    : name of the instrument
          address (string) : GPIB address
          reset (bool)     : resets to default values, default=False
        '''
        if address == None: 
            raise Exception('TCP IP address needed')
        logging.info(__name__ + ' : Initializing instrument Agilent_E5071C')
        super().__init__(name, address, terminator = '\n', **kwargs)

        # Add in parameters
        self.add_parameter('fstart', 
                          get_cmd = ':SENS1:FREQ:STAR?', 
                          set_cmd = ':SENS1:FREQ:STAR {}', 
                          vals = vals.Numbers(), 
                          get_parser = float, 
                          unit = 'Hz'
                          )
        self.add_parameter('fstop', 
                          get_cmd = ':SENS1:FREQ:STOP?', 
                          set_cmd = ':SENS1:FREQ:STOP {}', 
                          vals = vals.Numbers(), 
                          get_parser = float, 
                          unit = 'Hz'
                          )
        self.add_parameter('fcenter', 
                          get_cmd = ':SENS1:FREQ:CENT?', 
                          set_cmd = ':SENS1:FREQ:CENT {}', 
                          vals = vals.Numbers(), 
                          get_parser = float, 
                          unit = 'Hz'
                          )
        self.add_parameter('fspan', 
                          get_cmd = ':SENS1:FREQ:SPAN?', 
                          set_cmd = ':SENS1:FREQ:SPAN {}', 
                          vals = vals.Numbers(), 
                          get_parser = float, 
                          unit = 'Hz'
                          )
        
        self.add_parameter('rfout', 
                           get_cmd = ':OUTP?',
                           set_cmd = ':OUTP {}',
                           vals = vals.Ints(0,1), 
                           get_parser = int
                           )
        
        self.add_parameter('nfpts', 
                           get_cmd = ':SENS1:SWE:POIN?', 
                           set_cmd = ':SENS1:SWE:POIN {}', 
                           vals = vals.Ints(1,1601), 
                           get_parser = int
                           )
        self.add_parameter('ifbw', 
                           get_cmd = ':SENS1:BWID?', 
                           set_cmd = ':SENS1:BWID {}', 
                           vals = vals.Numbers(), #TODO: get range
                           get_parser = float)
        self.add_parameter('power', 
                           get_cmd = ":SOUR1:POW?", 
                           set_cmd = ":SOUR1:POW {}", 
                           unit = 'dBm', 
                           get_parser = float,
                           vals = vals.Numbers(-85, 10)
                           )
        self.add_parameter('power_start',
                           get_cmd = ':SOUR1:POW:STAR?',
                           set_cmd = ':SOUR1:POW:STAR {}',
                           unit = 'dBm',
                           get_parser = float, 
                           vals = vals.Numbers(-85, 10)
                           )
        self.add_parameter('power_stop', 
                           get_cmd = ':SOUR:POW:STOP?', 
                           set_cmd = ':SOUR1:POW:STOP {}', 
                           unit = 'dBm', 
                           get_parser = float, 
                           vals = vals.Numbers(-85, 10)), 
        self.add_parameter('averaging', 
                           get_cmd = ':SENS1:AVER?',
                           set_cmd = ':SENS1:AVER {}', 
                           get_parser = int, 
                           vals = vals.Ints(0,1)
                           )
        self.add_parameter('average_trigger', 
                           get_cmd = ':TRIG:AVER?',
                           set_cmd = ':TRIG:AVER {}', 
                           get_parser = int, 
                           vals = vals.Ints(0,1)
                           )
        self.add_parameter('avgnum', 
                           get_cmd = ':SENS1:AVER:COUN?', 
                           set_cmd = ':SENS1:AVER:COUN {}', 
                           vals = vals.Ints(1), 
                           get_parser = int
                           )
        self.add_parameter('phase_offset', 
                           get_cmd = ':CALC1:CORR:OFFS:PHAS?', 
                           set_cmd = ':CALC1:CORR:OFFS:PHAS {}', 
                           get_parser = float, 
                           vals = vals.Numbers())
        self.add_parameter('electrical_delay', 
                           get_cmd = 'CALC1:CORR:EDEL:TIME?', 
                           set_cmd = 'CALC1:CORR:EDEL:TIME {}', 
                           unit = 's',
                           get_parser = float,
                           vals = vals.Numbers()
                           )
        self.add_parameter('trigger_source', 
                            get_cmd = 'TRIG:SOUR?', 
                            set_cmd = 'TRIG:SOUR {}', 
                            vals = vals.Enum('INT', 'EXT', 'MAN', 'BUS')
                            )
        self.add_parameter('trform', 
                            get_cmd = ':CALC1:FORM?', 
                            set_cmd = ':CALC1:FORM {}', 
                            vals = vals.Enum('PLOG', 'MLOG', 'PHAS', 
                                             'GDEL', 'SLIN', 'SLOG', 
                                             'SCOM', 'SMIT', 'SADM', 
                                             'PLIN', 'POL', 'MLIN', 
                                             'SWR', 'REAL', 'IMAG', 
                                             'UPH', 'PPH')
                            )
                            # '''
                            # Set trace format. MLOGarithmic|PHASe|GDELay| SLINear|
                            # SLOGarithmic|SCOMplex|SMITh|SADMittance|PLINear|PLOGarithmic|
                            # POLar|MLINear|SWR|REAL| IMAGinary|UPHase|PPHase
                            # '''
                            
        self.add_parameter('math', 
                           get_cmd = ':CALC1:MATH:FUNC?', 
                           set_cmd = ':CALC1:MATH:FUNC {}', 
                           vals = vals.Enum('ADD', 'SUBT', 'DIV', 'MULT', 'NORM')
                           )
        self.add_parameter('sweep_type',
                           get_cmd = ':SENS1:SWE:TYPE?', 
                           set_cmd = ':SENS1:SWE:TYPE {}', 
                           vals = vals.Enum('LIN', 'LOG', 'SEGM', 'POW')
                           )
        self.add_parameter('correction', 
                           get_cmd = ':SENS1:CORR:STAT?', 
                           set_cmd = ':SENS1:CORR:STAT {}', 
                           get_parser = int)
        self.add_parameter('smoothing', 
                           get_cmd = ':CALC1:SMO:STAT?', 
                           set_cmd = ':CALC1:SMO:STAT {}', 
                           get_parser = float 
                           )
        self.add_parameter('trace', 
                           set_cmd = None, 
                           get_cmd = self.gettrace)
        self.add_parameter('fdata', 
                           set_cmd = None, 
                           get_cmd = self.getfdata)
        self.add_parameter('pdata', 
                           set_cmd = None, 
                           get_cmd = self.getpdata)
        self.connect_message()
        
        
####################### Custom Functions 
    def average_restart(self):
        self.write('SENS1:AVER:CLE')    
    def gettrace(self):
        '''
        Gets amp/phase stimulus data, returns 2 arrays
        
        Input:
            None
        Output:
            mags (dB) phases (rad)
        '''
        logging.info(__name__ + ' : get amp, phase stim data')
        strdata= str(self.ask(':CALC:DATA:FDATa?'))
        data= np.array(list(map(float,strdata.split(','))))
        data=data.reshape((int(np.size(data)/2)),2)
        return data.transpose()
        
    def getfdata(self):
        '''
        Gets freq stimulus data, returns array
        
        Input:
            None
        Output:
            freqvalues array (Hz)
        '''
        logging.info(__name__ + ' : get f stim data')
        strdata= str(self.ask(':SENS1:FREQ:DATA?'))
        return np.array(map(float,strdata.split(',')))
    def getpdata(self):
        '''
        Get the probe power sweep range
        
        Input: 
            None
        Output:
            probe power range (numpy array)
        '''
        logging.debug(__name__ + ' : get the probe power sweep range')
        return np.linspace(self.power_start(), self.power_stop(), 1601)
        
    def set_bundle(self, bundle):
        '''
        This lets you set values for the VNA all at once in a dictionary by using a key
        '''
        for key in bundle:
            try: 
                if type(bundle[key]) == str: 
                    eval("self."+key+"(str('"+bundle[key]+"'))") 
                else:
                    eval("self."+key+"(str("+str(bundle[key])+"))") 
            except AttributeError:
                raise Exception("Key '" + str(key)+"' not a valid VNA setting, check your dictionary for typos compared to VNA settings in driver using VNA.get_all()")

        
    def get_bundle(self,bundle):
        ''' 
        This retrieves the current elements in the bundle dictionary, but JUST the keys that you give it. It also calls BS if you give it a garbage key.
        '''
        for key in bundle:
            try: 
                if type(bundle[key]) == str: 
                    bundle[key] = eval("self."+key+"(str('"+bundle[key]+"'))") 
                else:
                    bundle[key] = eval("self."+key+"(str("+str(bundle[key])+"))") 
            except AttributeError:
                raise Exception("Key '" + str(key)+"' not a valid VNA setting, check your dictionary for typos compared to VNA settings in driver using VNA.get_all()")
                
        return bundle.copy() #the copy is because you want them to be seperate from the original dictionary. If it were C they would have different pointers
      
    def data_to_mem(self):        
        '''
        Calls for data to be stored in memory
        '''
        logging.debug(__name__+": data to mem called")
        self.write(":CALC1:MATH:MEM")
    def average(self, number): 
        #setting averaging timeout, it takes 52.02s for 100 traces to average with 1601 points and 2kHz IFBW, so 
        '''
        Sets the number of averages taken, waits until the averaging is done, then gets the trace
        '''
        s_per_trace = 54/100
        #turn on the average trigger
        prev_timeout = self.timeout()
        self.timeout(number*s_per_trace)
        self.average_trigger(1)
        self.avgnum(number)
        self.trigger_source('BUS')
        self.write(':TRIG:SING')
        #the next command will hang the kernel until the averaging is done
        self.ask('*OPC?')
        
        #reset the timeout
        self.timeout(prev_timeout)

        return self.gettrace()
        
        
        
        