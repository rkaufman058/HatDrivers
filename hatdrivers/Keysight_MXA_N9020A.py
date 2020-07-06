# -*- coding: utf-8 -*-
"""
Created on Mon Jul  6 15:40:26 2020

@author: Ryan Kaufman, loosely based on original qtlab code by Erick Brindock
"""

import visa
import types
import logging
import numpy as np
import time
from qcodes import (Instrument, VisaInstrument,
                    ManualParameter, MultiParameter,
                    validators as vals)

class Keysight_MXA_N9020A(VisaInstrument): 
    def __init__(self, name, address = None, **kwargs):
        '''
        Initializes the Keysight_MXA_N9020A, and communicates with the wrapper.

        Input:
          name (string)    : name of the instrument
          address (string) : GPIB address
          reset (bool)     : resets to default values, default=False
        '''
        if address == None: 
            raise Exception('TCP IP address needed')
        logging.info(__name__ + ' : Initializing instrument Keysight_MXA_N9020A')
        
        super().__init__(name, address, terminator = '\n', **kwargs)

        self.add_parameter("fstart", 
                           get_cmd = 'FREQ:STAR?', 
                           set_cmd = 'FREQ:STAR {}', 
                           vals = vals.Numbers(10),
                           get_parser = float, 
                           unit = 'Hz')
        self.add_parameter("fstop", 
                           get_cmd = 'FREQ:STOP?', 
                           set_cmd = 'FREQ:STOP {}', 
                           vals = vals.Numbers(10),
                           get_parser = float, 
                           unit = 'Hz')
        self.add_parameter("fcenter", 
                           get_cmd = 'FREQ:CENT?', 
                           set_cmd = 'FREQ:CENT {}', 
                           vals = vals.Numbers(10),
                           get_parser = float, 
                           unit = 'Hz')
        self.add_parameter("fspan", 
                           get_cmd = 'FREQ:SPAN?', 
                           set_cmd = 'FREQ:SPAN {}', 
                           vals = vals.Numbers(0),
                           get_parser = float, 
                           unit = 'Hz'
                           )
        self.add_parameter("RBW", 
                           get_cmd = 'BAND?', 
                           set_cmd = 'BAND {}', 
                           vals = vals.Numbers(10),
                           get_parser = float, 
                           unit = 'Hz')
        self.add_parameter("RBW_auto", 
                           get_cmd = 'BAND:AUTO?', 
                           set_cmd = 'BAND:AUTO {}', 
                           vals = vals.Ints(0,1),
                           get_parser = int
                           )
        self.add_parameter("VBW", 
                           get_cmd = 'BAND:VID?', 
                           set_cmd = 'BAND:VID {}', 
                           vals = vals.Numbers(1, 8e6),
                           get_parser = float, 
                           unit = 'Hz')
        self.add_parameter("VBW_auto", 
                           get_cmd = 'BAND:VID:AUTO?', 
                           set_cmd = 'BAND:VID:AUTO {}', 
                           vals = vals.Ints(0,1),
                           get_parser = int
                           )
        self.add_parameter("trigger_source", 
                           get_cmd = 'TRIG:SOUR?', 
                           set_cmd = 'TRIG:SOUR {}', 
                           vals = vals.Enum('ext1','ext2','imm'),
                           get_parser = str
                           )
        self.add_parameter("sweep_time", 
                           get_cmd = 'SWE:TIME?', 
                           set_cmd = 'SWE:TIME {}', 
                           vals = vals.Numbers(1e-6, 6000), 
                           get_parser = float, 
                           unit = 's')
        self.add_parameter("sweep_time_auto", 
                           get_cmd = 'SWE:TIME:AUTO?', 
                           set_cmd = 'SWE:TIME:AUTO {}', 
                           vals = vals.Ints(0,1),
                           get_parser = int
                           )
        self.add_parameter("sweep_time_auto_rules", 
                           get_cmd = 'SWE:TIME:AUTO:RUL?',
                           set_cmd = 'SWE:TIME:AUTO:RUL {}',
                           vals = vals.Enum('norm', 'normal', 'accuracy','acc', 'sres', 'sresponse'),
                           get_parser = str
                           )
        self.add_parameter("continuous_measurement", 
                           get_cmd = 'INIT:CONT?', 
                           set_cmd = 'INIT:CONT {}',
                           vals = vals.Ints(0,1), 
                           get_parser = float
                           )
        self.add_parameter('mode', 
                           get_cmd = ':INSTRUMENT?',
                           set_cmd = ':INSTRUMENT {}'
                           )
        
        #adding trace parameters, only gettable with custom commands below
        self.add_parameter("trace_1", set_cmd = None, get_cmd = self.do_get_trace_1)
        self.add_parameter("trace_2", set_cmd = None, get_cmd = self.do_get_trace_2)
        self.add_parameter("trace_3", set_cmd = None, get_cmd = self.do_get_trace_3)
        self.add_parameter("trace_4", set_cmd = None, get_cmd = self.do_get_trace_4)
        self.add_parameter("trace_5", set_cmd = None, get_cmd = self.do_get_trace_5)
        self.add_parameter("trace_6", set_cmd = None, get_cmd = self.do_get_trace_6)
        
        self.connect_message()
        
        
    def do_get_trace_1(self):
        '''
        Reads the style of trace 1
            Output:
                values (list) : [Display, Update, Type, Detector] ON = 1 OFF =2
        '''
        logging.info(__name__ + ' Reading state of trace 1')
        return ['Disp: ' + self.ask('TRAC1:DISP?'),
                'Upd: ' + self.ask('TRAC1:UPD?'),
                'Type: ' + self.ask('TRAC1:TYPE?'),
                'Det: ' + self.ask('DET:TRAC1?')]
    
    def do_get_trace_2(self):
        '''
        Reads the style of trace 2
            Output:
                values (list) : [Display, Update, Type, Detector] ON = 1 OFF =2
        '''
        logging.info(__name__ + ' Reading state of trace 2')
        return ['Disp: ' + self.ask('TRAC2:DISP?'),
                'Upd: ' + self.ask('TRAC2:UPD?'),
                'Type: ' + self.ask('TRAC2:TYPE?'),
                'Det: ' + self.ask('DET:TRAC2?')]
    
    def do_get_trace_3(self):
        '''
        Reads the style of trace 3
            Output:
                values (list) : [Display, Update, Type, Detector] ON = 1 OFF =2
        '''
        logging.info(__name__ + ' Reading state of trace 3')
        return ['Disp: ' + self.ask('TRAC3:DISP?'),
                'Upd: ' + self.ask('TRAC3:UPD?'),
                'Type: ' + self.ask('TRAC3:TYPE?'),
                'Det: ' + self.ask('DET:TRAC3?')]
    
    def do_get_trace_4(self):
        '''
        Reads the style of trace 4
            Output:
                values (list) : [Display, Update, Type, Detector] ON = 1 OFF =2
        '''
        logging.info(__name__ + ' Reading state of trace 4')
        return ['Disp: ' + self.ask('TRAC4:DISP?'),
                'Upd: ' + self.ask('TRAC4:UPD?'),
                'Type: ' + self.ask('TRAC4:TYPE?'),
                'Det: ' + self.ask('DET:TRAC4?')]
    
    def do_get_trace_5(self):
        '''
        Reads the style of trace 5
            Output:
                values (list) : [Display, Update, Type, Detector] ON = 1 OFF =2
        '''
        logging.info(__name__ + ' Reading state of trace 5')
        return ['Disp: ' + self.ask('TRAC5:DISP?'),
                'Upd: ' + self.ask('TRAC5:UPD?'),
                'Type: ' + self.ask('TRAC5:TYPE?'),
                'Det: ' + self.ask('DET:TRAC5?')]
    
    def do_get_trace_6(self):
        '''
        Reads the style of trace 6
            Output:
                values (list) : [Display, Update, Type, Detector] ON = 1 OFF =2
        '''
        logging.info(__name__ + ' Reading state of trace 6')
        return ['Disp: ' + self.ask('TRAC6:DISP?'),
                'Upd: ' + self.ask('TRAC6:UPD?'),
                'Type: ' + self.ask('TRAC6:TYPE?'),
                'Det: ' + self.ask('DET:TRAC6?')]
    
##### Other Custom Commands #####

    def trace_on(self, channel = 1):
        '''
        Sets the trace mode to ON (ie Display on, Update on)
            Input:
                channel (int) : channel to alter [1-6]
        '''
        logging.info(__name__ + ' Setting channel %s to on' %channel)
        self.write('TRAC%s:UPD 1' % channel)
        self.write('TRAC%s:DISP 1' % channel)
        
    def get_data(self, count = 0, channel = 1):
        '''
        Reads the data from the current sweep (NEEDS TESTED)
            Input:
                count (int) : sets max hold value between 1 and 10,000
                0 uses the value stored in the instrument
                channel (int):
            Output:
                data (numpy 2dArray) : [x, y] values
        '''
        data = None
        if count is not 0:
            if count > 10000:
                count = 10000
                logging.warning(__name__ +
                                ' Count too high. set to max value 10000')            
            self.write('AVER:COUN %s' % count)
        if channel < 1 or channel > 6:
            raise ValueError('channel must be between 1 and 6')
        else:
            self.write('AVER:CLE')
        while data is None:
            try:
                data = self.ask('CALC:DATA%s?' % channel)
            except Exception as e:
                print ('Running test.')
                logging.info(__name__ + str(type(e)) + 
                            ' raised. Count not done')
            else:
                print('Count complete')
                logging.info(__name__ + ' Reading the trace data')
                data = data.lstrip('[').rstrip(']').split(',')
                data = [float(value) for value in data]
                np_array = np.reshape(data, (-1,2))
                return np_array
                
    def get_previous_data(self, channel = 1):
        '''
        Reads the data already acquired without starting a new test
        '''
        return self.ask('CALC:DATA%s?' %channel)           
                
    def get_average(self):
        '''
        Reads the average of the current sweep
            Output: 
                average (float) :the average
        '''
        logging.info(__name__ + ' Reading the average value')
        return self.ask('CALC:DATA:COMP? MEAN')
    def trace_type(self, trace_type, channel = 1):
        '''
        Sets the type of the trace on the specified channel
            Input:
                trace_type (string) : 
                    ['writ', 'write', 'aver', 'average', 'maxh', 'maxhold', 
                     'minh', 'minhold']
                channel (int) : channel 1-6
        '''
        self.is_valid_channel(channel)
        trace_type = trace_type.lower()
        if trace_type not in TRACE_TYPES:
            raise ValueError('%s is not a valid trace type' % trace_type)
        logging.info(__name__ + 
            ' setting trace type to {} on channel {}'.format(trace_type,
                                                            channel))
        self.write('TRAC{}:TYPE {}'.format(channel, 
                                                           trace_type))
        
    def trace_detector(self, detector, channel = 1):
        '''
        Sets the detector for the trace on the specified channel
            Input:
                detector (string) : 
                    ['aver', 'average', 'neg', 'negative', 'norm', 'normal', 
                    'pos', 'positive', 'samp', 'sample', 'qpe', 'qpeak', 'eav',
                    'eaverage', 'rav', 'raverage']
                channel (int) : channel 1-6
        '''
        self.is_valid_channel(channel)
        if detector not in TRACE_DETECTORS:
            raise ValueError('%s is not a valid detector type' % detector)
        logging.info(__name__ + 
            ' setting the detector to {} for channel {}'.format(detector,
                                                                channel))
        self.write('DET:TRAC{} {}'.format(channel, detector))
    def trace_view(self, channel = 1):
        '''
        Sets the trace mode to VIEW (ie Display on, Update off)
            Input:
                channel (int) : channel to alter [1-6]
        '''
        logging.info(__name__ + ' Setting channel %s to view' %channel)
        self.write('TRAC%s:UPD 0' %channel)
        self.write('TRAC%s:DISP 1' %channel)
        
    def trace_blank(self, channel = 1):
        '''
        Sets the trace mode to BLANK (ie Display off, Update off)
            Input:
                channel (int) : channel to alter [1-6]
        '''
        logging.info(__name__ + ' Setting channel %s to blank' %channel)
        self.write('TRAC%s:UPD 0' %channel)
        self.write('TRAC%s:DISP 0' %channel)
        
    def trace_background(self, channel = 1):
        '''
        Sets the trace mode to BACKGROUND (ie Display off, Update on)
            Input:
                channel (int) : channel to alter [1-6]
        '''
        logging.info(__name__ + ' Setting channel %s to background' %channel)
        self.write('TRAC%s:UPD 1' %channel)
        self.write('TRAC%s:DISP 0' %channel)
        
    def clear_trace(self, *trace_channel):
        '''
        Clears the specified trace without effecting state of function or 
        variable
            Input:
                trace_channel (int) : 1|2|3|4|5|6 channel to be cleared
        '''
        logging.info(__name__ + ' Clearing the trace')
        for i in trace_channel:
            self.write('TRAC:CLE TRACE%s' %i)
    def reset(self):
        '''
        Resets the device to default state
        '''
        logging.info(__name__ + ' : resetting the device')
        self.write('*RST')
    def send_command(self, command):
        '''
        Sends a command to the instrument
            Input:
                command (string) : command to be sent (see manual for commands)
        '''
        self.write(command)
    def retrieve_data(self, query):
        '''
        Reads data from the instrument
            Input:
                query (string) : command to be sent (see manual for commands)
            Output:
                varies depending on command sent
        '''
        return self.ask(query)
        
    def is_valid_channel(self, channel):
        min_chan_val = 1
        max_chan_val = 6
        if channel < min_chan_val or channel > max_chan_val:
            raise ValueError('channel must be between {} and {}'.format(min_chan_val, max_chan_val))
        else:
            return channel


    def marker_Y_value(self, markernum = 1):
        '''
        Get the Y value for the No. markernum marker
        '''
        logging.info(__name__ + ' : get Y value of %i marker' % markernum)
        mode = self.get_mode()
        if mode == 'BASIC':
            return float(self.ask(':CALCULATE:SPECTRUM:MARKER%i:Y? ' % markernum)) 
        elif mode == 'SA':
            return float(self.ask(':CALCULATE:MARKER%i:Y? ' % markernum))

    def marker_X_value(self, markernum = 1):
        '''
        Get the Y value for the No. markernum marker
        '''
        logging.info(__name__ + ' : get X value of %i marker' % markernum)
        mode = self.get_mode()
        if mode == 'BASIC':
            return float(self.ask(':CALCULATE:SPECTRUM:MARKER%i:X? ' % markernum)) 
        elif mode == 'SA':
            return float(self.ask(':CALCULATE:MARKER%i:X? ' % markernum)) 
            
    def new_peak(self, markernum = 1):
        '''
        Set the chosen marker on a peak
        '''
        logging.info(__name__ + ' : set the %i marker on a peak' % markernum)
        mode = self.get_mode()
        if mode == 'BASIC':
            self.write(':CALCULATE:SPECTRUM:MARKER%i:MAXIMUM' % markernum)
        elif mode == 'SA':
            self.write(':CALCULATE:MARKER%i:MAXIMUM' % markernum)
        
    def next_peak(self, markernum = 1):
        '''
        Set the chosen marker to the next peak
        '''
        logging.info(__name__ + ' : set the %i marker to the next peak' % markernum)
        mode = self.get_mode()
        if mode == 'BASIC':            
            self.write(':CALCULATE:SPECTRUM:MARKER%i:MAXIMUM:NEXT' % markernum)
        elif mode == 'SA':
            self.write(':CALCULATE:MARKER%i:MAXIMUM:NEXT' % markernum)
            
    def next_peak_right(self, markernum = 1):
        '''
        Set the chosen marker to the next peak right
        '''
        logging.info(__name__ + ' : set the %i marker to the next peak right' % markernum)
        mode = self.get_mode()
        if mode == 'BASIC':
            self.write(':CALCULATE:SPECTRUM:MARKER%i:MAXIMUM:RIGHT' % markernum)    
        elif mode == 'SA':
            self.write(':CALCULATE:MARKER%i:MAXIMUM:RIGHT' % markernum)  
            
    def next_peak_left(self, markernum = 1):
        '''
        Set the chosen marker to the next peak
        '''
        logging.info(__name__ + ' : set the %i marker to the next peak left' % markernum)
        mode = self.get_mode()
        if mode == 'BASIC':
            self.write(':CALCULATE:SPECTRUM:MARKER%i:MAXIMUM:LEFT' % markernum) 
        elif mode == 'SA':
            self.write(':CALCULATE:MARKER%i:MAXIMUM:LEFT' % markernum) 
            
    def marker_off(self, markernum = 1):
        '''
        Turn off the chosen marker
        '''
        logging.info(__name__ + ' : turn off the %i marker' % markernum)
        mode = self.get_mode()
        if mode == 'BASIC':
            self.write(':CALCULATE:SPECTRUM:MARKER%i:MODE OFF' % markernum)
        elif mode == 'SA':
            self.write(':CALCULATE:MARKER%i:MODE OFF' % markernum)

    def marker_to_center(self, markernum = 1):
        '''
        Set the marker frequency to be the center frequency
        '''
        logging.info(__name__ + ' : turn off the %i marker' % markernum)
        mode = self.get_mode()
        if mode == 'BASIC':
            self.write(':CALCULATE:SPECTRUM:MARKER%i:CENTER' % markernum)
        elif mode == 'SA':
            self.write(':CALCULATE:MARKER%i:CENTER' % markernum)
        
        