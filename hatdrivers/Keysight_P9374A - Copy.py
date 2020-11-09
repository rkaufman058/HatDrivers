<<<<<<< HEAD

# MJH 2015_10_15.. Maybe this will work??
#Additions by Alex
#average method by Erick Brindock  7/15/16
#driver rewritten by Ryan Kaufman 06/11/20 for Qcodes
#YR: also, here is keysights manual,http://ena.support.keysight.com/e5071c/manuals/webhelp/eng/
#you want the programming -> remote control part for VISA commands

=======
# -*- coding: utf-8 -*-
"""
A driver to control the Keysight VNA P9374A using VISA

@author: Hatlab: Pinlei Lu
@email: PIL9@pitt.edu

PS: This driver is not very mature, feel free contacting author.
"""

from instrument import Instrument
>>>>>>> a7e8429a186eeaeec2d1790a73c8fe4879d23db2
import visa
import types
import logging
import numpy as np
import time
<<<<<<< HEAD
from qcodes import (Instrument, VisaInstrument,
                    ManualParameter, MultiParameter,
                    validators as vals)
#from pyvisa.visa_exceptions import VisaIOError
#triggered=[False]*159 

class Keysight_P9374A(VisaInstrument):
    '''
    This is the driver for the Agilent E5071C Vector Netowrk Analyzer

    Usage:
    Initialize with
    <name> = instruments.create('<name>', 'Agilent_E5071C', 
    address='<GBIP address>, reset=<bool>')
    '''
    
    def __init__(self, name, address = None, **kwargs):
=======
# from pyvisa.visa_exceptions import VisaIOError

class Keysight_P9374A(Instrument):

    def __init__(self, name, address, reset=False):
>>>>>>> a7e8429a186eeaeec2d1790a73c8fe4879d23db2
        '''
        Initializes the Agilent_E5071C, and communicates with the wrapper.

        Input:
          name (string)    : name of the instrument
          address (string) : GPIB address
          reset (bool)     : resets to default values, default=False
        '''
<<<<<<< HEAD
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
        
        self.add_parameter('num_points', 
                           get_cmd = ':SENS1:SWE:POIN?', 
                           set_cmd = ':SENS1:SWE:POIN {}', 
                           vals = vals.Ints(1,1601), 
                           get_parser = int
                           )
        self.add_parameter('ifbw', 
                           get_cmd = ':SENS1:BWID?', 
                           set_cmd = ':SENS1:BWID {}', 
                           vals = vals.Numbers(10,1.5e6),
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
        #TODO: Set trg sources
        self.add_parameter('trigger_source', 
                            get_cmd = 'TRIG:SOUR?', 
                            set_cmd = 'TRIG:SOUR {}', 
                            vals = vals.Enum('INT', 'EXT', 'MAN', 'BUS')
                            )
        self.add_parameter('trform', 
                            get_cmd = ':CALC1:FORM?', 
                            set_cmd = ':CALC1:FORM {}', 
                            vals = vals.Enum('MLOG', 'PHAS', 
                                             'GDEL',  
                                             'SCOM', 'SMIT', 'SADM', 
                                             'POL', 'MLIN', 
                                             'SWR', 'REAL', 'IMAG', 
                                             'UPH', 'PPH')
                            )
                            # '''
                            # Set trace format. MLOGarithmic|PHASe|GDELay| SLINear|
                            # SLOGarithmic|SCOMplex|SMITh|SADMittance|PLINear|PLOGarithmic|
                            # POLar|MLINear|SWR|REAL| IMAGinary|UPHase|PPHase
                            # '''
                            
        self.add_parameter('math', 'SLIN', 'SLOG',
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
        self.add_parameter('sweep_time', 
                           get_cmd = ':SENS1:SWE:TIME?', 
                           set_cmd = None, #generally just adjust ifbw and number of pts to change it,
                           get_parser = float,
                           unit = 's'
                           )
        self.connect_message()
        
        
####################### Custom Functions 
    def average_restart(self):
        self.write('SENS1:AVER:CLE')
=======
        logging.info(__name__ + ' : Initializing instrument Agilent_E5071C')
        Instrument.__init__(self, name, tags=['physical'])
        print 'portable VNA init...'
        # Add some global constants
        self._address = address
        self._visainstrument = visa.instrument(self._address)
        print self._visainstrument
        print address

        self.add_parameter('power',flags=Instrument.FLAG_GETSET, units='dBm',
                           minval=-80, maxval=10, type=types.FloatType)
        
        self.add_parameter('rfout',flags=Instrument.FLAG_GETSET, minval=0,
                           maxval=1, type=types.IntType)
        
        self.add_parameter('nfpts', flags=Instrument.FLAG_GETSET,minval=2,
                           maxval=100001, type=types.IntType)
        
        self.add_parameter('sparam',flags=Instrument.FLAG_GETSET,
                           type=types.StringType)
        
        self.add_parameter('fstart', flags=Instrument.FLAG_GETSET, units='Hz',
                           minval=300E3, maxval=20E9, type=types.FloatType)
        
        self.add_parameter('fstop', flags=Instrument.FLAG_GETSET, units='Hz',
                           minval=300E3, maxval=20E9, type=types.FloatType)
        
        self.add_parameter('ifbw', flags=Instrument.FLAG_GETSET, units='Hz',
                           minval=10, maxval=1500000, type=types.FloatType)
        
        self.add_parameter('avgstat', flags=Instrument.FLAG_GETSET, minval=0,
                           maxval=1, type=types.IntType)
        
        self.add_parameter('avgnum', flags=Instrument.FLAG_GETSET, minval=1,
                           maxval=999, type=types.IntType)
        
        self.add_parameter('trform',flags=Instrument.FLAG_GETSET,
                           type=types.StringType)       
        
#        self.add_parameter('continuous_trigger',flags=Instrument.FLAG_GETSET,
#                           type=types.BooleanType)

        self.add_parameter('trigger_scope',flags=Instrument.FLAG_GETSET, 
                           type=types.StringType)

        self.add_parameter('trigger_source',flags=Instrument.FLAG_GETSET, 
                           type=types.StringType)    

#        self.add_parameter('point_trigger',flags=Instrument.FLAG_GETSET, 
#                           type=types.BooleanType)

#        self.add_parameter('avg_trigger',flags=Instrument.FLAG_GETSET, 
#                           type=types.BooleanType)

        self.add_parameter('averaging', type=types.IntType)
        
        self.add_parameter('time_sweep', flags=Instrument.FLAG_GETSET,
                           type=types.FloatType)

        self.add_parameter('auto_sweep', flags=Instrument.FLAG_GETSET,
                           type=types.StringType)
        
        self.add_parameter('smoothing', flags=Instrument.FLAG_GETSET,
                           type=types.IntType, minVal=0, maxVal=1)
        
        self.add_parameter('correction', flags=Instrument.FLAG_GETSET,
                           type=types.IntType, minVal=0, maxVal=1)                   
        
        self.add_parameter('fcenter', flags=Instrument.FLAG_GETSET,
                           type=types.FloatType, units='Hz')
        
        self.add_parameter('fspan', flags=Instrument.FLAG_GETSET,
                           type=types.FloatType, units='Hz')        
        
        self.add_parameter('cwfreq', flags=Instrument.FLAG_GETSET,
                           type=types.FloatType, units='Hz')        
                           
        self.add_parameter('power_start', flags=Instrument.FLAG_GETSET,
                           type=types.FloatType, units='dB')
        self.add_parameter('power_stop', flags=Instrument.FLAG_GETSET,
                           type=types.FloatType, units='dB')

                           
        self.add_parameter('math', flags=Instrument.FLAG_GETSET,
                           type=types.StringType)        
        
        self.add_parameter('sweep_type', flags=Instrument.FLAG_GETSET,
                           type=types.StringType)
        
        self.add_parameter('electrical_delay', flags=Instrument.FLAG_GETSET,
                           type=types.FloatType)
        
        self.add_parameter('phase_offset', flags = Instrument.FLAG_GETSET,
                           type=types.FloatType)
        self.add_function('send')
        self.add_function('receive')
        self.add_function('reset')
        self.add_function('get_all')
        self.add_function('getfdata')
        self.add_function('gettrace')
        self.add_function('trigger')
        self.add_function('continuous_trigger_toggle')
        self.add_function('average')
        self.add_function('wait')
        self.add_function('data_to_mem')
        self.add_function('getpdata')
        self.add_function('restart_trigger')
        self.add_function('average_restart')
        
       # self._visainstrument.write('CALC1:PAR:DEF meas1, S11')
        self._visainstrument.write('CALC1:PAR:MNUM 1')        
        
        
        
        if (reset):
            self.reset()
        else:
            self.get_all()

    def set_avg_trigger(self,*kwarg):
        pass
    def get_avg_trigger(self,*kwarg):
        pass
    def average_restart(self):
        self._visainstrument.write('SENS1:AVER:CLE')
    def send(self, command):
        self._visainstrument.write(command)
    def receive(self, command):
        return self._visainstrument.ask(command)
    def average(self, number, PVNA=1):
        '''
        Sets the number of averages taken and waits until the averaging is done
        (Note: Trigger source must be set to bus)
        '''
        # disable warning beep for the unterminated Query waring if the 
        #exception is raised
        if PVNA:
            self.average_restart()
            time.sleep(int(number*0.8))
        else:
            self._visainstrument.write(':SYST:BEEP:WARN:STAT off')
            self.set_avgnum(number)
            self._visainstrument.write(':TRIG:SING')
            testing = 0
            while testing == 0:
                try:
                    testing = int(self._visainstrument.ask('*OPC?'))
                except Error:#VisaIOError:
                    # testing = 0
                    pass
            self._visainstrument.write('SYST:BEEP:WARN:STAT on')
            print 'Averaging completed'
    def reset(self):
        '''
        Resets the instrument to default values

        Input:
            None

        Output:
            None
        '''
        logging.info(__name__ + ' : resetting instrument')
        self._visainstrument.write('*RST')
        self.get_all()

    def get_all(self):
        '''
        Reads all implemented parameters from the instrument,
        and updates the wrapper.

        Input:
            None

        Output:
            None
        '''
        logging.info(__name__ + ' : get all')
        self.get_power()
        self.get_rfout()
        self.get_nfpts()
        self.get_fstart()
        self.get_fstop()
        self.get_fcenter()
        self.get_fspan()
        self.get_ifbw()
        self.get_avgstat()
        self.get_avgnum()
        self.get_trigger_scope()
        self.get_trigger_source()
        self.get_correction()
        self.get_cwfreq()
        self.get_auto_sweep()
        self.get_time_sweep()
#        self.get_point_trigger()
#        self.get_avg_trigger()
#        self.get_continuous_trigger()
        self.get_math()
        self.get_sweep_type()
        self.get_electrical_delay()
        self.get_averaging()
        self.get_power_start()
        self.get_power_stop()
        
    def wait(self, wait_time):
        '''
        
        '''
        start = time.time()
        while (time.time()-start<wait_time):
            pass
            
#        print("I should be waiting")
#        cont=True
#        while(cont):
#            try:
#                self.get_fdata()
#                cont=False
#            except:
#                cont=True
#        return
            
    def restart_trigger(self):
        logging.info(__name__ + " restarting trigger")
        self._visainstrument.write(":ABORt")
    def do_set_power_start(self, power):
        logging.info(__name__ + " setting start power to %s" %power)
        self._visainstrument.write(':SOUR1:POW:STAR %s' %power)
        
    def do_get_power_start(self):
        logging.info(__name__ + " getting the start power")
        return self._visainstrument.ask(':SOUR1:POW:STAR?')
        
    def do_set_power_stop(self, power):
        logging.info(__name__ + " setting the stop power to %s" %power)
        self._visainstrument.write(':SOUR1:POW:STOP %s' %power)
        
    def do_get_power_stop(self):
        logging.info(__name__ + " getting the start power")
        return self._visainstrument.ask(':SOUR:POW:STOP?')
                
    def do_get_averaging(self):
        return self._visainstrument.ask(':SENS1:AVER?')
        
    def do_set_averaging(self, enable):
        self._visainstrument.write(':SENS1:AVER %s' %enable)
        
    def do_get_phase_offset(self):
        '''
        Reads the phase offset
        
            Output:
                offset (float) : the phase offset in degrees
        '''
        return self._visainstrument.ask(':CALC1:CORR:OFFS:PHAS?')
        
    def do_set_phase_offset(self, offset):
        '''
        Sets the phase offset
            Input:
                offset (float) : the phase offset in degrees
        '''
        self._visainstrument.write(':CALC1:CORR:OFFS:PHAS %s' % offset)
        
    def continuous_trigger_toggle(self, ch=1):
        '''
        Creates a continues trigger if one is not already present,
        if a continuous trigger is already in place, this function
        ends it.
        
        Input:
            ch: The number corresponding to the Channel, defaults to 1
        '''
        global triggered
        triggered[ch-1]=(not triggered[ch-1])
        logging.info(__name__+"triggered: "+str(triggered[ch-1]))
        self._visainstrument.write(":INIT{}:CONT {}".format(ch,
                                   int(triggered[ch-1])))
        return triggered[ch-1]
        
    def trigger(self,ch=1):
        '''
        Creates a single trigger and returns to the normal state unless\
        already in a continuous trigger.
        
        Input:
            ch: The number corresponding to the Channel, defaults to 1
        
        Output:
            None
        '''
        if triggered[ch-1]:
            return
        logging.info(__name__ + ' : trigger')
        self._visainstrument.write(":INIT %s" % ch)

    def do_get_electrical_delay(self):
        '''
        Gets the length of the electrical delay in seconds
        
        Input:
            None
        
        Output:
            None
        '''
        logging.info(__name__ + "get the electrical delay length (seconds)")
        return self._visainstrument.ask(":CALC1:CORR:EDEL:TIME?")
        
    def do_set_electrical_delay(self, time):
        '''
        Sets the length of the electrical delay in seconds
        
        Input:
            time= Amount of time to simulate as a delay in seconds
            
        Output:
            None
        '''
        logging.info(__name__ + "set the electrical delay length (seconds)")
        self._visainstrument.write(":CALC1:CORR:EDEL:TIME "+str(time))    
    
    def do_get_trigger_scope(self):
        '''
        Returns the scope of the trigger
        
        Input:
            None
             
        Output:
            A string representation of the source.  Either "ALL" or "ACT"
            
        '''
        logging.debug(__name__+' : get trigger scope')
        return self._visainstrument.ask(":TRIG:SEQ:SCOP?")
    
    def do_set_trigger_scope(self, scope):
        '''
        Sets the scope trigger
        
        Input:
            scope: Either "ALL" or "ACT", which defines the scope
            of the trigger"
        '''
        assert scope.upper() in ['ACT','ALL']
        logging.debug(__name__+' : set the trigger scope to: '+scope)
        self._visainstrument.write(":TRIG:SEQ:SCOP "+scope.upper())
    
    def do_get_trigger_source(self):
        '''
        Gets the trigger source
        
        Input:
            None
            
        Output:
            trigger_source: It will be INT EXT MAN or BUS which represents\
            the trigger source
            
        '''
        logging.debug(__name__+" : get trigger source")
        return self._visainstrument.ask("TRIG:SOUR?")
        
    def do_set_trigger_source(self, source, PVNA=1):
        '''
        Sets the trigger source
        
        Input:
            trigger_source: It will be INT EXT MAN or BUS which represents\
            the trigger source
            
        Output:
            None
            
        '''
        if PVNA:
            pass
        else:
            assert source.upper() in ['INT','EXT','MAN','BUS']
            logging.debug(__name__+" : set trigger source to "+source)
            self._visainstrument.write("TRIG:SOUR "+source.upper())
    
    def do_get_correction(self):
        '''
        Gets the state of correction
        
        Input:
            None
        
        Output:
            The state of the correction
        '''
        logging.debug(__name__+" : get state of correction")
        return self._visainstrument.ask(":SENS1:CORR:STAT?")
    
    def do_set_correction(self, correction):
        '''
        Sets the state of correction
        
        Input:
            The state of the correction
            
        Output:
            None
        '''
        logging.debug(__name__+": set state of correction to "+str(correction))
        self._visainstrument.write(":SENS1:CORR:STAT "+str(correction))
    
    def do_get_smoothing(self):
        '''
        Gets the state of the smoothing
        
        Input:
            None
            
        Output:
            smoothing=the state of the smoothing operation
        '''
        logging.debug(__name__+": get the state of smoothing")
        return self._visainstrument.ask(":CALC1:SMO:STAT?")
        
    def do_set_smoothing(self, smoothing):
        '''
        Sets the state of the smoothing
        
        Input:
            smoothing=the state of the smoothing operation
            
        Output:
            None
        '''
        logging.debug(__name__+": set the smoothing "+ str(smoothing))
        self._visainstrument.write(":CALC1:SMO:STAT "+str(smoothing))        
        
    def do_get_power(self):
        '''
        Gets the current power (Amplitude) of the sweep
        
        Input:
            None
            
        Output:
            power=The power (Amplitude) of the sweep
        '''
        logging.debug(__name__+ ": get the power")
        return self._visainstrument.ask(":SOUR1:POW?")
    
    def do_set_power(self, power):
        '''
        Sets the current power (Amplitude) of the sweep
        
        Input:
            power=The power desired for the sweep (.05 dBm resolution)
       
       Output:
            None
        '''
        if(int(power)>5):
            power=5
        assert power<=5
        logging.debug(__name__+ ": set the power")
        self._visainstrument.write(":SOUR1:POW "+str(power))
    
    def do_get_cwfreq(self):
        '''
        Get the cw frequency
        
        Input:
            None
            
        Output:
            cw frequency (Hz)
        '''
    
        logging.debug(": Get the cw frequency")
        return self._visainstrument.ask(":SENS1:FREQ?")
        
    def do_set_cwfreq(self, cw):
        '''
        Set the cw frequency
        
        Input:
            CW frequency (Hz)
            
        Output:
            None
        '''
        logging.debug(": Set the cw frequency to "+str(cw))   
        self._visainstrument.write(":SENS1:FREQ "+str(cw))
        
    def do_get_auto_sweep(self):
        '''
        Gets whether or not auto sweep is set
        
        Input:
            None
            
        Output:
            auto=(1/0) representation of whether the auto sweep is on
            
        '''
        
        logging.debug(__name__+": get if auto sweep")
        return self._visainstrument.ask(":SENS1:SWE:TIME:AUTO?")
    
    def do_set_auto_sweep(self, on_off):
        '''
        Sets the auto sweep
        
        Input:
            on_off: (1/0) representation of boolean
        
        Output:
            None
        '''
        
        logging.debug(__name__ + ": set auto swep to "+str(on_off))
        self._visainstrument.write(":SENS1:SWE:TIME:AUTO "+str(on_off))
    
    def do_get_time_sweep(self):
        '''
        Gets the timing of the the sweep
        
        Input:
            None
            
        Output:
            time=the timing of the trigger (0 represents autotrigger)
        '''
        
        logging.debug(__name__+ ": get the time of the sweep")
        return self._visainstrument.ask(":SENS1:SWE:TIME?")
    
    def do_set_time_sweep(self, time):
        '''
        Sets the timing of the sweep
        
        Input:
            time=The time of the trigger (set 0 for auto trigger)
            
        Output:
            None
        '''
        if(self.get_auto_sweep()):
            self.set_auto_sweep(0)
        logging.debug(__name__ + ": set the time of the sweep to "+str(time))
        self._visainstrument.write(":SENS1:SWE:TIME "+ str(time))
    
#    def do_get_point_trigger(self):
#        '''
#        Gets the state of the point trigger (ON/OFF)
#        
#        Input:
#            None
#            
#        Output:
#            point_trigger: 1 if on, 0 if off
#        '''
#        
#        logging.debug(__name__+" : get trigger source")
#        return self._visainstrument.ask("TRIG:POIN?")        
#   
#    def do_set_point_trigger(self, trigger):
#        '''
#        Sets the state of the point trigger (ON/OFF)
#        
#        Input:
#            trigger: 1 if on, 0 if off
#            
#        Output:
#            None
#            
#        '''
#        logging.debug(__name__+" : set the state of the point trigger")
#        self._visainstrument.write(":TRIG:POIN "+str(int(trigger)))
#    
#    def do_get_avg_trigger(self):
#        '''
#        Gets the state of the averaging trigger
#        
#        Input:
#            None
#        
#        Output:
#            state: The state of the average trigger.
#        
#        '''
#        logging.debug(__name__+" : get the state of the averaging trigger")
#        return self._visainstrument.ask(":TRIG:AVER?")
#    
#    def do_set_avg_trigger(self, state):
#        '''
#        Gets the state of the averaging trigger
#        
#        Input:
#            None
#        
#        Output:
#            state: The state of the average trigger.
#        '''
#        logging.debug(__name__+" : set the state of the averaging trigger")
#        self._visainstrument.write(":TRIG:AVER "+str(int(state)))
    
    def getfdata(self):
        '''
        Gets freq stimulus data, returns array
        
        Input:
            None
        Output:
            freqvalues array (Hz)
        '''
        logging.info(__name__ + ' : get f stim data')
        strdata= str(self._visainstrument.ask(':SENS1:X:VAL?'))
        return np.array(map(float,strdata.split(',')))

    def get_fdata(self):
        '''
        Gets freq stimulus data, returns array
        
        Input:
            None
        Output:
            freqvalues array (Hz)
        '''
        logging.info(__name__ + ' : get f stim data')
        strdata= str(self._visainstrument.ask(':SENS1:X:VAL?'))
        return np.array(map(float,strdata.split(',')))
  
>>>>>>> a7e8429a186eeaeec2d1790a73c8fe4879d23db2
    def gettrace(self):
        '''
        Gets amp/phase stimulus data, returns 2 arrays
        
        Input:
            None
        Output:
            mags (dB) phases (rad)
        '''
        logging.info(__name__ + ' : get amp, phase stim data')
<<<<<<< HEAD
        strdata= str(self.ask('CALC1:DATA? FDATA'))
        data= np.array(strdata.split(',')).astype(float)
        print(len(data))
        if len(data)%2 == 0:
            data=data.reshape((int(len(data)/2),2))
=======
        strdata= str(self._visainstrument.ask('CALC1:DATA? FDATA'))
        data= np.array(map(float,strdata.split(',')))
        if len(data)%2 == 0:
            print 'change shape'
            data=data.reshape((len(data)/2,2))
>>>>>>> a7e8429a186eeaeec2d1790a73c8fe4879d23db2
            real=data[:, 0]
            imag=data[:, 1]
            mag=20*np.log10(np.sqrt(real**2+imag**2))
            phs=np.arctan2(imag,real)
            magAndPhase = np.zeros((2, len(real)))
            magAndPhase[0]=mag
            magAndPhase[1]=phs
            return magAndPhase
        else:
            return data#.transpose() # mags, phase
        
<<<<<<< HEAD
    def getfdata(self):
        '''
        Gets freq stimulus data, returns array
=======
    def getcomplextrace(self):
        '''
        Gets amp/phase stimulus data, returns 2 arrays
>>>>>>> a7e8429a186eeaeec2d1790a73c8fe4879d23db2
        
        Input:
            None
        Output:
<<<<<<< HEAD
            freqvalues array (Hz)
        '''
        logging.info(__name__ + ' : get f stim data')
        strdata= str(self.ask(':SENS1:FREQ:DATA?'))
        return np.array(list(map(float,strdata.split(','))))
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
      
=======
            mags (dB) phases (rad)
        '''
        logging.info(__name__ + ' : get amp, phase stim data')
        strdata= str(self._visainstrument.ask('CALC1:DATA? SDATA'))
        data= np.array(map(float,strdata.split(',')))
#        data=data.reshape((len(data)/2,2))
        return data#.transpose() # mags, phase
        
#    def do_get_continuous_trigger(self, ch=1):
#        '''
#        Reads the state of trigger on a channel
#        
#        Input:
#            ch: defaults to 1, represents the channel to be triggered
#            
#        Output:
#            The state of the channel's trigger
#        '''
#        global triggered
#        logging.debug(__name__+' : get state of continuous trigger in '+
#            'channel %s' % ch)
#        return triggered[ch-1]
#
#    def do_set_continuous_trigger(self, state,ch=1):
#        '''
#        Sets the state of the trigger on a channel
#        
#        Input:
#            state: state desired
#            ch: defaults to 1, the numeric representation of the channel
#        '''
#        global triggered
#        logging.debug(__name__+' : set the state of channel {} to {}'.format(
#                     ch, state))
#        self._visainstrument.write(':INIT{}:CONT {}'.format(int(ch),
#                                   int(state)))
#        triggered[ch-1]=bool(state)
#        return triggered[ch-1]
       
    
    def do_get_rfout(self):
        '''
        Reads the rf output status from instrument
        
        Input:
            None
            
        Output
            RF output status (On/1, Off/0)
        '''
        logging.debug(__name__ + ': get status')
        return int(self._visainstrument.ask(':OUTP?'))
    
    def do_set_rfout(self, newout):
        '''
        Set the rf output status to On/1 Off/0
        
        Input: 
            New Output stat (1,0)
            
        Output:
            None
        '''
        logging.debug(__name__ + ' : set output status to %s' % newout)
        self._visainstrument.write(':OUTP %s' % newout )
    
    def do_get_nfpts(self):
        '''
        Get number of pts. in freq sweetp (int)
        
        Input: 
            None
            
        Outpt:
            Int # of freq pts 
        '''
        logging.debug(__name__ + ': get nfpts')
        return int(self._visainstrument.ask(':SENS1:SWE:POIN?')) 
    
    def do_set_nfpts(self, nfpts):
        '''
        set number of pts. in freq sweetp (int)
        
        Input: 
            None
            
        Outpt:
            Int # of freq pts 
        '''
        logging.debug(__name__ + ': set nfpts to %s' % nfpts)
        self._visainstrument.write(':SENS1:SWE:POIN %s' % nfpts)
        
    def do_get_sparam(self):
        '''
        Get Sparam of current msmt 
        
        Input: 
            None
            
        Outpt:
            Sxx as string 
        '''
        logging.debug(__name__ + ': get sparam')
        return str(self._visainstrument.ask(':CALC1:PAR:CAT?')) 
    
    def do_set_sparam(self, sparam):
        '''
        Set Sparam of current msmt
        
        Input: 
            New Sparam in form Sxx (string)
            
        Outpt:
             None
        '''
        logging.debug(__name__ + ': set sparam to %s' % sparam)
        self._visainstrument.write(':CALC1:PAR:MOD %s' % sparam)
        
    def do_get_fstart(self):
        '''
        Get start freq
        
        Input: 
            None
            
        Outpt:
            start freq (Hz) 
        '''
        logging.debug(__name__ + ': get fstart')
        return float(self._visainstrument.ask(':SENS1:FREQ:STAR?')) 
    
    def do_set_fstart(self, fstart):
        '''
        Set start freq
        
        Input: 
            start freq (Hz)
            
        Outpt:
            None
        '''
        logging.debug(__name__ + ': set fstart to %s' % fstart)
        self._visainstrument.write(':SENS1:FREQ:STAR %s' % fstart)
    def do_get_fstop(self):
        '''
        Get stop freq
        
        Input: 
            None
            
        Outpt:
            stop freq (Hz) 
        '''
        logging.debug(__name__ + ': get fstop')
        return float(self._visainstrument.ask(':SENS1:FREQ:STOP?')) 
    
    def do_set_fstop(self, fstop):
        '''
        Set stop freq
        
        Input: 
            stop freq (Hz) 
            
        Outpt:
            None 
        '''
        logging.debug(__name__ + ': set fstop to %s' % fstop)
        self._visainstrument.write(':SENS1:FREQ:STOP %s' % fstop)
    
    def do_get_fcenter(self):
        '''
        Get the frequency center
        
        Input:
            None
            
        Output:
            center freq (Hz)
        '''
        logging.debug(__name__+": get fcenter")
        return self._visainstrument.ask(":SENS1:FREQ:CENT?")
    
    def do_set_fcenter(self, center):
        '''
        Set the frequency center
        
        Input:
            center=center frequency
        
        Output:
            None
        '''
        logging.debug(__name__+": set fcenter")
        self._visainstrument.write(":SENS1:FREQ:CENT "+str(center))
    
    def do_get_fspan(self):
        '''
        Get the frequency span
        
        Input:
            None
            
        Output:
            span freq (Hz)
        '''
        logging.debug(__name__+": get fspan")
        return self._visainstrument.ask(":SENS1:FREQ:SPAN?")
    
    def do_set_fspan(self, span):
        '''
        Set the frequency span
        
        Input:
            span=span frequency
        
        Output:
            None
        '''
        logging.debug(__name__+": set fcenter")
        self._visainstrument.write(":SENS1:FREQ:SPAN "+str(span))
    
    
    def do_get_ifbw(self):
        '''
        Get ifbw 
        
        Input: 
            None
            
        Outpt:
            ifbw (Hz) 
        '''
        logging.debug(__name__ + ': get ifbw')
        return float(self._visainstrument.ask(':SENS1:BWID?')) 
    
    def do_set_ifbw(self, ifbw):
        '''
        Set ifbw
        
        Input: 
            ifbw (Hz) 
            
        Outpt:
            None 
        '''
        logging.debug(__name__ + ': set ifbw to %s' % ifbw)
        self._visainstrument.write(':SENS1:BWID %s' % ifbw)
    def do_get_avgstat(self):
        '''
        Get avgstatus (1/On 0/off) 
        
        Input: 
            None
            
        Outpt:
            avgstatus (1/On 0/off) 
        '''
        logging.debug(__name__ + ': get avgstat')
        return int(self._visainstrument.ask(':SENS1:AVER?')) 
    
    def do_set_avgstat(self, avgstat):
        '''
        Set average status (1/On 0/off)
        
        Input: 
            new avgstat (1/0)
            
        Outpt:
            None 
        '''
        logging.debug(__name__ + ': set ifbw to %s' % avgstat)
        self._visainstrument.write(':SENS1:AVER %s' % avgstat)
    def do_get_avgnum(self):
        '''
        Get avg num
        
        Input: 
            None
            
        Outpt:
            avg num
        '''
        logging.debug(__name__ + ': get avgsnum')
        return int(self._visainstrument.ask(':SENS1:AVER:COUN?')) 
    
    def do_set_avgnum(self, avgnum):
        '''
        Set average number
        
        Input: 
            new avg number
            
        Outpt:
            None 
        '''
        logging.debug(__name__ + ': set avg # to %s' % avgnum*2)
        self._visainstrument.write(':SENS1:AVER:COUN %s' % avgnum*2)
    def do_get_trform(self):
        '''
        Get trace format.  MLOGarithmic|PHASe|GDELay| SLINear|
        SLOGarithmic|SCOMplex|SMITh|SADMittance|PLINear|PLOGarithmic|
        POLar|MLINear|SWR|REAL| IMAGinary|UPHase|PPHase
        
        Input: 
            None
            
        Outpt:
            trace format (string)
        '''
        logging.debug(__name__ + ': get format')
        return str(self._visainstrument.ask(':CALC1:FORM?')) 
    
    def do_set_trform(self, f):
        '''
        Set trace format. MLOGarithmic|PHASe|GDELay| SLINear|
        SLOGarithmic|SCOMplex|SMITh|SADMittance|PLINear|PLOGarithmic|
        POLar|MLINear|SWR|REAL| IMAGinary|UPHase|PPHase
        
        Input: 
            new format (string)
          
        Outpt:
            None 
        '''
        if f=='PLOG':
            f ="POLar"
        logging.debug(__name__ + ': set trace  format to %s' % f)
        self._visainstrument.write(':CALC1:FORM %s' % f)    
        
>>>>>>> a7e8429a186eeaeec2d1790a73c8fe4879d23db2
    def data_to_mem(self):        
        '''
        Calls for data to be stored in memory
        '''
        logging.debug(__name__+": data to mem called")
<<<<<<< HEAD
        self.write(":CALC1:MATH:MEM")
    def average(self, number): 
        #setting averaging timeout, it takes 52.02s for 100 traces to average with 1601 points and 2kHz IFBW, so 
        '''
        Sets the number of averages taken, waits until the averaging is done, then gets the trace
        '''
        assert number > 0
        
        prev_trform = self.trform()
        self.trform('PLOG')
        self.trigger_source('BUS')
        
        buffer_time = 1 #s
        if number == 1:
           
            self.averaging(0)
            self.average_trigger(0)
            s_per_trace = self.sweep_time()
            self.timeout(number*s_per_trace+buffer_time)
            self.trigger()
            return self.gettrace()
        else: 
            #wait just a little longer for safety #TODO: find a way to make this better than 8%
            #turn on the average trigger
            
            self.averaging(1)
            self.average_trigger(1)
            self.avgnum(number)
            prev_timeout = self.timeout()
            s_per_trace = self.sweep_time()
            self.timeout(number*s_per_trace+buffer_time)
            print("Waiting {:.3f} seconds for {} averages...".format(self.timeout(), number))
            self.write(':TRIG:SING')
            # print('triggered')
            #the next command will hang the kernel until the averaging is done
            print(self.ask('*OPC?'))
            # print('timeout check')
            return self.gettrace()
    
    def savetrace(self, avgnum = 200, savedir = None): 
        if savedir == None:
            import easygui 
            savedir = easygui.filesavebox("Choose file to save trace information: ")
            assert savedir != None
            
        elif savedir == "previous": 
            savedir = self.previous_save
            assert savedir != None
        fdata = self.getfdata()
        prev_trform = self.trform()
        self.trform('PLOG')
        tracedata = self.average(avgnum)
        self.trform(prev_trform)
        self.trigger_source('INT')
        self.previous_save = savedir
        import h5py
        file = h5py.File(savedir, 'w')
        file.create_dataset("VNA Frequency (Hz)", data = fdata)
        file.create_dataset("S21", data = tracedata)
        file.create_dataset("Phase (deg)", data = tracedata[1])
        file.create_dataset("Power (dB)", data = tracedata[0])
        file.close()
        
        
        
        
    def save_important_info(self, savedir = None):
        if savedir == None:
            import easygui 
            savedir = easygui.filesavebox("Choose where to save VNA info: ", default = savedir)
            assert savedir != None
        file = open(savedir+'.txt', 'w')
        file.write(self.name+'\n')
        file.write("Power: "+str(self.power())+'\n')
        file.write("Frequency: "+str(self.fcenter())+'\n')
        file.write("Span: "+str(self.fspan())+'\n')
        file.write("EDel: "+str(self.electrical_delay())+'\n')
        file.write("Num_Pts: "+str(self.num_points())+'\n')
        print("Power: "+str(self.power())+'\n'+"Frequency: "+str(self.fcenter())+'\n'+"Span: "+str(self.fspan())+'\n'+"EDel: "+str(self.electrical_delay())+'\n'+"Num_Pts: "+str(self.num_points())+'\n')
        file.close()
        return savedir
    
    def trigger(self): 
        self.write(':TRIG:SING')
        return None
    def set_to_manual(self): 
        self.rfout(1)
        self.averaging(1)
        self.avgnum(1)
        self.average_trigger(0)
        self.trform('PHAS')
        self.trigger_source('INT')
=======
        self._visainstrument.write(":CALC1:MATH:MEM")
    
    def do_get_math(self):
        '''
        Gets the state of the math
            'ADD'=Addition
            'SUBT'=Subtraction
            'DIV'=Division
            'MULT'=Multiplication
            'NORM'=Normal/None
        '''
        logging.debug(__name__+": math")
        return self._visainstrument.ask(":CALC1:MATH:FUNC?")
        
    def do_set_math(self, math):
        '''
        Sets the state of the math
            'ADD'=Addition
            'SUBT'=Subtraction
            'DIV'=Division
            'MULT'=Multiplication
            'NORM'=Normal/None
        '''
        logging.debug(__name__+": sets the state of math_mem")
        self._visainstrument.write(":CALC1:MATH:FUNC "+ math.upper())
    
    def do_get_sweep_type(self):
        '''
        Gets the type of sweep
            'LIN'=Linear
            'LOG'=Logarithmic
            'SEGM'=Segment
            'POW'=Power
        '''
        logging.debug(__name__+": gets the sweep type")
        return self._visainstrument.ask(":SENS1:SWE:TYPE?")
        
    def do_set_sweep_type(self, sweep):
        '''
        Gets the type of sweep
            'LIN'=Linear
            'LOG'=Logarithmic
            'SEGM'=Segment
            'POW'=Power
        '''
        logging.debug(__name__+": Set the sweep type to "+sweep)
        self._visainstrument.write(":SENS1:SWE:TYPE "+sweep.upper())
    # shortcuts
    def off(self):
        '''
        Set status to 'off'

        Input:
            None

        Output:
            None
        '''
        logging.debug(__name__ + ' : set output OFF')
        self._visainstrument.write(':OUTP:STAT OFF')

    def on(self):
        '''
        Set status to 'off'

        Input:
            None

        Output:
            None
        '''
        logging.debug(__name__ + ' : set output ON')
        self._visainstrument.write(':OUTP:STAT ON')
    
    def getpdata(self):
        '''
        Get the probe power sweep range
        
        Input: 
            None
        Output:
            probe power range (numpy array)
        '''
        logging.debug(__name__ + ' : get the probe power sweep range')
        return np.linspace(self.get_power_start(), self.get_power_stop(), 1601)    

        
#    def do_get_nfpts(self):
#        '''
#        Get number of pts. in freq sweetp (int)
#        
#        Input: 
#            None
#            
#        Outpt:
#            Int # of freq pts 
#        '''
#        return int(self._visainstrument.ask(':SENS1:SWE:POIN?')) 
#    
#    def do_set_nfpts(self, nfpts):
#        '''
#        set number of pts. in freq sweetp (int)
#        
#        Input: 
#            None
#            
#        Outpt:
#            Int # of freq pts 
#        '''
#        self._visainstrument.write(':SENS1:SWE:POIN %s' % nfpts)
#
#    def do_get_fstart(self):
#        '''
#        Get start freq
#        
#        Input: 
#            None
#            
#        Outpt:
#            start freq (Hz) 
#        '''
#        logging.debug(__name__ + ': get fstart')
#        return float(self._visainstrument.ask(':SENS1:FREQ:STAR?')) 
#    
#    def do_set_fstart(self, fstart):
#        '''
#        Set start freq
#        
#        Input: 
#            start freq (Hz)
#            
#        Outpt:
#            None
#        '''
#        logging.debug(__name__ + ': set fstart to %s' % fstart)
#        self._visainstrument.write(':SENS1:FREQ:STAR %s' % fstart)
#    def do_get_fstop(self):
#        '''
#        Get stop freq
#        
#        Input: 
#            None
#            
#        Outpt:
#            stop freq (Hz) 
#        '''
#        logging.debug(__name__ + ': get fstop')
#        return float(self._visainstrument.ask(':SENS1:FREQ:STOP?')) 
#    
#    def do_set_fstop(self, fstop):
#        '''
#        Set stop freq
#        
#        Input: 
#            stop freq (Hz) 
#            
#        Outpt:
#            None 
#        '''
#        logging.debug(__name__ + ': set fstop to %s' % fstop)
#        self._visainstrument.write(':SENS1:FREQ:STOP %s' % fstop)
#    
#    def do_get_fcenter(self):
#        '''
#        Get the frequency center
#        
#        Input:
#            None
#            
#        Output:
#            center freq (Hz)
#        '''
#        logging.debug(__name__+": get fcenter")
#        return self._visainstrument.ask(":SENS1:FREQ:CENT?")
#    
#    def do_set_fcenter(self, center):
#        '''
#        Set the frequency center
#        
#        Input:
#            center=center frequency
#        
#        Output:
#            None
#        '''
#        logging.debug(__name__+": set fcenter")
#        self._visainstrument.write(":SENS1:FREQ:CENT "+str(center))
#    
#    def do_get_fspan(self):
#        '''
#        Get the frequency span
#        
#        Input:
#            None
#            
#        Output:
#            span freq (Hz)
#        '''
#        logging.debug(__name__+": get fspan")
#        return self._visainstrument.ask(":SENS1:FREQ:SPAN?")
#    
#    def do_set_fspan(self, span):
#        '''
#        Set the frequency span
#        
#        Input:
#            span=span frequency
#        
#        Output:
#            None
#        '''
#        logging.debug(__name__+": set fcenter")
#        self._visainstrument.write(":SENS1:FREQ:SPAN "+str(span))
>>>>>>> a7e8429a186eeaeec2d1790a73c8fe4879d23db2
