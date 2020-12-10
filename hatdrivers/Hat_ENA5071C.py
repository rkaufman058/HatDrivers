# -*- coding: utf-8 -*-
"""
Created on Tue Dec  8 16:49:14 2020

@author: Ryan Kaufman
"""

from hatdrivers.Agilent_ENA_5071C import Agilent_ENA_5071C
import numpy as np
import logging
import time

class Hat_ENA5071C(Agilent_ENA_5071C): 
    
    def __init__(self,name: str, address: str = None, terminator: str = "\n", **kwargs):
        if address == None:
            raise Exception('TCPIP Address needed')
        super().__init__(name, address, terminator = terminator, **kwargs)

    def average_restart(self):
        self.write('SENS1:AVER:CLE')  

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
        
    def data_to_mem(self):        
        '''
        Calls for data to be stored in memory
        '''
        logging.debug(__name__+": data to mem called")
        self.write(":CALC1:MATH:MEM")
    def average(self, number, tracetype = 'PLOG'): 
        #setting averaging timeout, it takes 52.02s for 100 traces to average with 1601 points and 2kHz IFBW
        '''
        Sets the number of averages taken, waits until the averaging is done, then gets the trace
        '''
        assert number > 0
        
        prev_trform = self.trform()
        self.trform(tracetype)
        self.trigger_source('BUS')
        
        buffer_time = 2 #s
        if number == 1:
           
            self.averaging(0)
            self.average_trigger(0)
            s_per_trace = self.sweep_time()
            self.timeout(number*s_per_trace+buffer_time)
            self.trigger()
            return self.gettrace()
        else: 
            #wait just a little longer for safety #TODO: find a way to make this better
            
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
    
    #DO NOT CHANGE THE DEFAULT KEYWORD ARGUMENTS HERE, CHANGE THEM WHEN YOU CALL THE FUNCTION WITH THE KEYWORD ARGUMENT
    #ex: VNA.savetrace(avgnum = 200)
    def savetrace(self, avgnum = 3, savedir = None): 
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
        
        
    def save_important_info(self, savepath = None, print_info = False):
        if savepath == None and print_info == False:
            import easygui 
            savepath = easygui.filesavebox("Choose where to save VNA info: ", default = savepath)
            assert savepath != None
        if print_info == False: 
            file = open(savepath, 'w')
            file.write(self.name+'\n')
            file.write("Power: "+str(self.power())+'\n')
            file.write("Frequency: "+str(self.fcenter())+'\n')
            file.write("Span: "+str(self.fspan())+'\n')
            file.write("EDel: "+str(self.electrical_delay())+'\n')
            file.write("Num_Pts: "+str(self.num_points())+'\n')
        print("Power: "+str(self.power())+'\n'+"Frequency: "+str(self.fcenter())+'\n'+"Span: "+str(self.fspan())+'\n'+"EDel: "+str(self.electrical_delay())+'\n'+"Num_Pts: "+str(self.num_points())+'\n')
        file.close()
        return savepath
    
    def trigger(self): 
        self.write(':TRIG:SING')
        return None
    def set_to_manual(self, trform = 'PHAS'): 
        self.rfout(1)
        self.averaging(1)
        self.avgnum(1)
        self.average_trigger(0)
        self.trform(trform)
        self.trigger_source('INT')
    def renormalize(self, num_avgs): 
        self.averaging(1)
        self.average_restart()
        self.average_trigger(0)
        self.avgnum(num_avgs)
        s_per_trace = self.sweep_time()
        wait_time = s_per_trace*num_avgs + 2
        print(f'Renormalizing, waiting {wait_time} seconds for averaging...')
        time.sleep(wait_time)
        self.data_to_mem()
        self.math('DIV')
        self.set_to_manual(trform = 'MLOG')