# -*- coding: utf-8 -*-
"""
Created on Wed Jun 24 19:31:35 2020

@author: Ryan Kaufman - modified from the original qtlab driver by xi cao
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


class SWT(): #no need to subclass object anymore, thankfully
    '''
    This is a class that is used to control all the Mini Circuits swtiches we have.
    To use this in the qtlab, do:

    from hatlab import switch_control
    SWT = switch_control.SWT()
    
    then you can just use SWT like a usual switch (I make the method name to be the 
    same as that in the single switch driver so it will be easy to use).  
    '''
    def __init__(self, SWT1, SWT2, modes_dict):
        '''
        Grab the switch instrument. If we have more swtiches in the future, we can 
        add switch3, 4, 5, ... in the same way.
        
        Input:
            None.
        Output:
            None.
        '''
        self.switch1 = SWT1
        self.switch2 = SWT2
        
        self.modes = modes_dict
        print ('hello, this is switch')
        
    def portvalue(self):
        '''
        Get the port value of each swtich and print them.
        
        Input:
            None.
        Output:
            None. But will print the port value of each swtich on the screen.
        '''
        
        print ('Switch 1 port value is:')
        swt1_value = self.switch1.portvalue()
        print (swt1_value)
        print ('Switch 2 port value is:')
        swt2_value = self.switch2.portvalue()
        print (swt2_value)
        
        return (swt1_value, swt2_value)
        
    def set_switch(self, switch_name, channel, state):
        '''
        Set the switch state as desired.
        
        Input:
            switch_name (int or str): the number of the swtich you want to access.
            channel (str): the name of the channel (eg. A, B, H) that you want 
                           to access (Note: letter P let you change all the swtich in the same time).
            state (str): the state you want to change to (0 or 1 for A~H, and a string of 0 and 1 for P).
        Oupput:
            None. But will print an error message if the switch name is wrong.
        '''
        if str(switch_name) == '1':
            self.switch1.set_switch(str(channel), str(state))
        elif str(switch_name) == '2':
            self.switch2.set_switch(str(channel), str(state))
        else:
            print ('Confucius says there is no such switch. Nothing has been changed.')
    
             
    def set_mode_dict(self, mode):
        '''
        Set the states of all swtiches to a pre-set mode.
        All the mode we wish to use during the experiment should be set above the 
        class definition before we use the swtich.
        
        Input:
            mode (str): the name of the mode you wish to use.
        Output:
            None. But will print an error message if the mode name is wrong.
        '''
        current_states = self.portvalue()
        if mode in self.modes:
            self.set_switch(1, 'P', self.create_new_mode_string(current_states[0], self.modes[mode][0]))
            self.set_switch(2, 'P', self.create_new_mode_string(current_states[1], self.modes[mode][1]))
        else:
            print  ('Confucius say there is no such mode. Nothing has been changed.')
            
            
    def set_SA_mode(self, mode):
        '''
        Set the states of some of the switched to a pre-set mode for spectrum analyzer.
        You should set to the mode you want to look at through self.set_mode then use 
        this method to determin what you want to at.
        
        Input:
            mode (str): the name of the mode you wish to use.
        Output:
            None. But will print an error message if the mode name is wrong.
        '''
        if mode == 'Q_drive_mon':
            self.set_switch(2, 'G', '1')
            self.set_switch(2, 'F', '0')
        elif mode == 'C_drive_mon':
            self.set_switch(2, 'G', '0')
            self.set_switch(2, 'F', '0')
        elif mode == 'VNA_mon':
            self.set_switch(1, 'H', '1')
            self.set_switch(2, 'F', '1')
        else:
            print ('Confucius say there is no such mode. Nothing has been changed.')
            
    def create_new_mode_string(self, current_state, new_state):
        if len(current_state)  != len(new_state):
            raise ValueError("current_state and new_state must be the same length.")
        output = ""
        for i in range(len(new_state)):
            if(new_state[i] != "0" and new_state[i] != "1" ):
                output += current_state[i]
            else:
                output += new_state[i]
        return output