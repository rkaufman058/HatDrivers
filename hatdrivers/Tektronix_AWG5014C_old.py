# -*- coding: utf-8 -*-
"""
Created on Tue Apr 13 13:55:30 2021

@author: Ryan Kaufman - based on the original code from Xi Cao
"""

import types
import logging
import numpy as np
import time
from qcodes import (Instrument, VisaInstrument,
                    ManualParameter, MultiParameter,
                    validators as vals)

class Tektronix_AWG5014C(VisaInstrument):
    
    def __init__(self, name, address, reset=False):
        '''
        Initializes the AWG5014C, and communicates with the wrapper.

        Input:
          name (string)    : name of the instrument
          address (string) : GPIB address
          reset (bool)     : resets to default values, default=False
        '''
        logging.info(__name__ + ' : Initializing instrument AWG5014C')
        
        super().__init__(name, address, terminator = '\n')

        # Add some global constants
        self._address = address        
        #self.add_parameter('runningstate',flags=Instrument.FLAG_GETSET, type=types.BooleanType)
        self.add_parameter('DC1output',
                           get_cmd = 'AWGControl:DC1:STATe?', 
                           set_cmd = 'AWGControl:DC1:STATe {}', 
                           vals = vals.Ints(), 
                           get_parser = int)
        
        
        #self.add_parameter('sequence',flags=Instrument.FLAG_GETSET, type=types.StringType)     
        self.add_parameter('AWGmode',
                           set_cmd = 'AWGCONTROL:RMODE {}', 
                           get_cmd = 'AWGCONTROL:RMODE?', 
                           get_parser = str)
        
        self.add_parameter('sequence_length', 
                           set_cmd = 'SEQUENCE:LENGTH {}', 
                           vals = vals.Ints(), 
                           get_parser = int, 
                           get_cmd = 'SEQUENCE:LENGTH?'
                           )
        
        self.add_parameter('internal_trigger_rate', 
                           get_cmd = 'TRIGGER:SEQUENCE:TIMER?', 
                           set_cmd = 'TRIGGER:SEQUENCE:TIMER {}', 
                           vals = vals.Numbers(), 
                           get_parser = float
                           )
        
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
        self.connect_message()
        if (reset):
            self.reset()
        else:
            self.get_all()
        
        #Custom functions
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
        #self.get_runningstate()
        
        self.DC1output()
        self.AWGmode()   
        self.ch1offset()
        self.ch2offset()
        self.ch3offset()
        self.ch4offset()
        self.ch1skew()
        self.ch2skew()
        self.ch3skew()
        self.ch4skew()
        self.ch1amp()
        self.ch2amp()
        self.ch3amp()
        self.ch4amp()
        self.internal_trigger_rate()
        self.sequence_length()
    def newwaveform(self,waveformname):
        '''
        create a new blank waveform in the waveform list.
        
        Input: a string with form '"waveformname",number of the point in the waveform, waveform type(integer or real)'
        e.g. '"TEST", 1024, INTEGER'
        '''
        logging.info(__name__ + ' : create a new wave form')
        self.write('WLIST:WAVEFORM:NEW %s' % waveformname)
        
    def setwaveform(self,wavestr):
        '''
        set value for a waveform that is in the waveform list (if waveform is not existed, use newwaveform to create one)
    
        '''
        logging.info(__name__ + ' : set value for a waveform')
        self.write('WLIST:WAVEFORM:DATA %s' % wavestr)
        
    def addwaveform(self,element,channel,wavename):
        '''
        Add waveform called "wavename" to the sequence and its position is given by channel and element
        '''
        logging.info(__name__ + ' : add a waveform to "channel"th channel of "element"th element')
        commandstr = 'SEQUENCE:ELEMENT%i:' % element + 'WAVEFORM%i' % channel + ' "%s"' % wavename
        self.write(commandstr)
        
    def addwaveform_nonseq(self,channel,wavename):
        '''
        Add waveform called "wavename" to the channel
        '''
        logging.info(__name__ + ' : add waveform %s' % wavename + ' to %i channel' % channel)
        self.write('SOURCE%i' % channel +':WAVEFORM "%s"' % wavename)
        
    def setmode(self,awgmode):
        '''
        Set AWG runmode 
        '''
        logging.info(__name__ + ' : select mode for AWG5014C')
        self.write('AWGCONTROL:RMODE %s' % awgmode)
    
    def waittrigger(self,element,command):
        '''
        Set or ask the wait trigger state of a certain element in the sequence
        Input: element number (int), command (0: no wait, 1: wait, 3: check the state)
        '''
        
        logging.info(__name__ + ': get wait trigger state')
        
        if (int(command) == 0):
            self.write('SEQUENCE:ELEMENT%i:TWAIT 0' % element)
  
        elif (int(command) == 1):
            self.write('SEQUENCE:ELEMENT%i:TWAIT 1' % element)
            
        #state = self._visainstrument.ask('SEQUENCE:ELEMENT%i:TWAIT?' % element)
        #print 'The wait trigger state for the desired element is:(0 for no wait, 1 for wait)'
        #print state
    def repeat(self, element, repeat_times = 1):
        '''
        Set the repeat number fot the element that needs to be repeated at the desired element, for 
        desired repeat times.
        '''
        logging.info(__name__ + ': set the repeat times')
        
        self.write('SEQUENCE:ELEMENT%i' % element +':LOOP:COUNT %i' % repeat_times)
        
    def run(self):
        '''
        Run AWG
        '''        
        logging.info(__name__ + ' : run the AWG')
        self.write('AWGCONTROL:RUN')     
        
    def stop(self):
        '''
        Stop AWG
        '''
        logging.info(__name__ + ' : stop the AWG')
        self.write('AWGCONTROL:STOP')
        
    def channel_on(self,channel_num):
        '''
        Turn on the chosen channel
        '''
        logging.info(__name__ + ' : turn on the %ith channel' % channel_num)
        self.write('OUTPUT%i:STATE ON' % channel_num)

    def channel_off(self,channel_num):
        '''
        Turn off the chosen channel
        '''
        logging.info(__name__ + ' : turn off the %ith channel' % channel_num)
        self.write('OUTPUT%i:STATE OFF' % channel_num)
        
        
    def force_trigger(self):
        '''
        Make a force trigger
        '''
        logging.info(__name__ + ' : make a force trigger')
        self.write('TRIGGER:SEQUENCE:IMMEDIATE')
        
        
    def setloop(self,channelnum,looptimes):
        '''
        Set the loop times for channle channelnum
        '''
        logging.info(__name__ + ' : set loop times for some certain channel')
        self.write('SEQUENCE:ELEMENT%i' % channelnum + ':LOOP:COUNT %i' % looptimes)
        
    def deletewaveform(self,wavename):
        '''
        delete a waveform in the waveform list
        '''        
        logging.info(__name__ + ' : delete a waveform with the name: %s' % wavename)
        self.write('WLIST:WAVEFORM:DELETE "%s"' % wavename)
        
        
    def set_ch_offset(self,ch_num,offset):
        '''
        Get the offset of a channle
        '''
        logging.info(__name__ + ' : get the offset of %ith channle' % ch_num + ' to %f' % offset)
        self.write('SOURCE%i' % ch_num + ':VOLTAGE:LEVEL:IMMEDIATE:OFFSET %f' % offset)
        
    def goto_state(self,element,state):
        '''
        Set the goto state of the chosen element to be on of off
        '''
        logging.info(__name__ + ' : set the goto state of the %ith' % element + ' element to be %i' % state)
        self.write('SEQUENCE:ELEMENT%i' % element + ':GOTO:STATE %i' % state)
        
    def goto_index(self,element,index):
        '''
        Set the chosen element go to the desired index
        '''
        logging.info(__name__ + ' : set the %i' % element + ' go to index %i' % index)
        self.write('SEQUENCE:ELEMENT%i' % element + ' :GOTO:INDEX %i' % index)
        
    def addmarker(self,wavename,datastr):
        '''
        Add the marker to a waveform
        '''
        logging.info(__name__ + ' : add the marker to the waveform %s' % wavename)
        self.write('WLIST:WAVEFORM:MARKER:DATA %s' % datastr)
        
    def deleteall(self):
        '''
        Delete all user-defined waveforms
        '''        
        logging.info(__name__ + ' : delete all the user-defined waveforms')
        self.write('WLIST:WAVEFORM:DELETE ALL')
        
    def restore(self, filename):
        '''
        Set the AWG sequence using a .awg file from the location we set
        '''
        logging.info(__name__ + ' : set the AWG with file ' + filename)
        self.write('AWGCONTROL:SRESTORE "%s"'  % filename)
        
    def save_setting(self, filename):
        '''
        Save the setting of the AWG to a .awg file to the location we want
        '''
        logging.info(__name__ + ' : save the AWG setting the file ' + filename)
        self.write('AWGCONTROL:SSAVE "%s"' % filename)
    
    # Xi: add theses functions for the AWG calibration on 2017-07-17
    def channel_offset(self, channel_num, offset):
        '''
        Set the channel offset to the desired value
        '''
        logging.info(__name__ + ' : set channel %i' % channel_num +' to value %d' % offset )
        if channel_num == 1:
            self.set_ch1offset(offset)
        if channel_num == 2:
            self.set_ch2offset(offset)
        if channel_num == 3:
            self.set_ch3offset(offset)
        if channel_num == 4:
            self.set_ch4offset(offset)

    def channel_skew(self, channel_num, skew):
        '''
        Set the channel skew to the desired value
        '''
        logging.info(__name__ + ' : set channel %i' % channel_num +' to value %d' % skew )
        if channel_num == 1:
            self.set_ch1skew(skew)
        if channel_num == 2:
            self.set_ch2skew(skew)
        if channel_num == 3:
            self.set_ch3skew(skew)
        if channel_num == 4:
            self.set_ch4skew(skew)

    def channel_amp(self, channel_num, amp):
        '''
        Set the channel skew to the desired value
        '''
        logging.info(__name__ + ' : set channel %i' % channel_num +' to value %d' % amp )
        if channel_num == 1:
            self.set_ch1amp(amp)
        if channel_num == 2:
            self.set_ch2amp(amp)
        if channel_num == 3:
            self.set_ch3amp(amp)
        if channel_num == 4:
            self.set_ch4amp(amp)