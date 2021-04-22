# -*- coding: utf-8 -*-
"""
Created on Sat Jun 16 23:21:47 2018

@author: HatLab_Xi Cao
"""


from __future__ import division
import ctypes
from hatdrivers.alazar_utilities import atsapinew as ats
import numpy as np
from threading import Thread
import time
import h5py
#import logging
#import sys
#sys.path.append(r'C:\Python\qtlab-master\qtlab-master\\')
#import qt
# Configure board 
def ConfigureBoard(board):
    '''
    Set up the basic settings for the alazar card to get data.
    '''        
    
    # TODO: Select clock parameters as required to generate this
    # sample rate
    #
    # For example: if samplesPerSec is 100e6 (100 MS/s), then you can
    # either:
    #  - select clock source INTERNAL_CLOCK and sample rate
    #    SAMPLE_RATE_100MSPS
    #  - or select clock source FAST_EXTERNAL_CLOCK, sample rate
    #    SAMPLE_RATE_USER_DEF, and connect a 100MHz signal to the
    #    EXT CLK BNC connector
    global samplesPerSec
    samplesPerSec = 1000000000.0
#    blah=1E9
    board.setCaptureClock(ats.EXTERNAL_CLOCK_10MHz_REF,
                          1000000000,
                          ats.CLOCK_EDGE_RISING,
                          1)
    
    # TODO: Select channel A input parameters as required.
    board.inputControl(ats.CHANNEL_A,
                       ats.DC_COUPLING, #changed DC to AC --we acquire at 50 MHZ MJH 2016_10_24
                       ats.INPUT_RANGE_PM_400_MV,
#                       ats.INPUT_RANGE_PM_1_V,
                       ats.IMPEDANCE_50_OHM)
    
    # TODO: Select channel A bandwidth limit as required.
    board.setBWLimit(ats.CHANNEL_A, 0)
    
    
    # TODO: Select channel B input parameters as required.
    board.inputControl(ats.CHANNEL_B,
                       ats.DC_COUPLING,
                       #ats.INPUT_RANGE_PM_400_MV,
                       ats.INPUT_RANGE_PM_400_MV,                       
                       ats.IMPEDANCE_50_OHM)
    
    # TODO: Select channel B bandwidth limit as required.
    board.setBWLimit(ats.CHANNEL_B, 0)
    
    # TODO: Select trigger inputs and levels as required.                       
    board.setTriggerOperation(ats.TRIG_ENGINE_OP_J,
                              ats.TRIG_ENGINE_J,
                              ats.TRIG_EXTERNAL,
                              ats.TRIGGER_SLOPE_POSITIVE,
                              150,
                              ats.TRIG_ENGINE_K,
                              ats.TRIG_DISABLE,
                              ats.TRIGGER_SLOPE_POSITIVE,
                              200)
                              
    # TODO: Select external trigger parameters as required.
    # board.setExternalTrigger(ats.AC_COUPLING,ats.ETR_5V)
    board.setExternalTrigger(0,1)
    
    # TODO: Set trigger delay as required.
    triggerDelay_sec = 0.00000
    triggerDelay_samples = 0* int(triggerDelay_sec * samplesPerSec + 0.5)
    #triggerDelay_samples = 10
    board.setTriggerDelay(triggerDelay_samples)

    # TODO: Set trigger timeout as required.
    #
    # NOTE: The board will wait for a for this amount of time for a
    # trigger event.  If a trigger event does not arrive, then the
    # board will automatically trigger. Set the trigger timeout value
    # to 0 to force the board to wait forever for a trigger event.
    #
    # IMPORTANT: The trigger timeout value should be set to zero after
    # appropriate trigger parameters have been determined, otherwise
    # the board may trigger if the timeout interval expires before a
    # hardware trigger event arrives.
    triggerTimeout_sec = 1E-3 #10us
    triggerTimeout_clocks = 0*(int(triggerTimeout_sec / 10e-6 + 0.5))
    board.setTriggerTimeOut(triggerTimeout_clocks)

    # Configure AUX I/O connector as required
    board.configureAuxIO(ats.AUX_OUT_TRIGGER,0)    
                         


class demodulation():
    '''
    Class for demode the signal from the alazar card. 
    We write this as a class so that the calculation value can be passed back when doing the multi-thread calculation. 
    '''    
    
    def __init__(self, data):
        self.temp = data

    def demo(self, triarray, recordsPerBuffer, cycles_per_record, stride, num_sequences, record_average):
        if record_average:
            self.result = np.sum((np.sum((self.temp * triarray).reshape((recordsPerBuffer, cycles_per_record, stride)), axis = 2)).reshape(recordsPerBuffer // num_sequences, num_sequences , cycles_per_record), axis = 0)
        
        elif not record_average:
            self.result = np.sum((self.temp * triarray).reshape((recordsPerBuffer, cycles_per_record, stride)), axis = 2)


def single_buffer(data, recordsPerBuffer, cycles_per_record, stride, SinArray, CosArray, num_sequences, record_average, demodulate = True):
    '''
    Calculating the I and Q value from the raw data that comes from one buffer.
    Using four thread to calculate Signal and Reference's I and Q. 
    '''    
    
    
    temp = data.reshape((2, len(data)//2))
    
    sigI = demodulation(temp[0])
    sigQ = demodulation(temp[0])
    refI = demodulation(temp[1])
    refQ = demodulation(temp[1])
    
    t1 = Thread(target = sigQ.demo, args = (SinArray, recordsPerBuffer, cycles_per_record, stride, num_sequences, record_average))
    t2 = Thread(target = sigI.demo, args = (CosArray, recordsPerBuffer, cycles_per_record, stride, num_sequences, record_average))
    
    t3 = Thread(target = refQ.demo, args = (SinArray, recordsPerBuffer, cycles_per_record, stride, num_sequences, record_average))
    t4 = Thread(target = refI.demo, args = (CosArray, recordsPerBuffer, cycles_per_record, stride, num_sequences, record_average))
    
    t1.start()
    t2.start()
    t3.start()
    t4.start()
    
    t1.join()
    t2.join()
    t3.join()
    t4.join()
    
    if demodulate: 
        print('Demodulating...')
        Ref_mag = np.sqrt(refI.result**2 + refQ.result**2)
        #phase subtraction to remove generator drift
        Sig_I = (sigI.result*refI.result + sigQ.result*refQ.result)/Ref_mag
        Sig_Q = (-sigI.result*refQ.result + sigQ.result*refI.result)/Ref_mag
    else: 
        print('NOT Demodulating')
        Sig_I = sigI.result
        Sig_Q = sigQ.result
        
    Ref_I = refI.result
    Ref_Q = refQ.result
    
    del t1
    del t2
    del t3
    del t4
    del sigI
    del sigQ
    del refI
    del refQ

    return(Sig_I, Sig_Q, Ref_I, Ref_Q)
    

def use_weight_function(filename, SinArray, CosArray, t_avg):
    '''
    Add the weight function to the demode sin and cos array we will be using.
    Only calculate for one record here. 
    '''
    
    print(SinArray.shape)
    
    weight_function = h5py.File(filename, 'r')
#    weight_I = weight_function['I'].value[0, 0:SinArray.shape[0]]
#    weight_Q = weight_function['Q'].value[0, 0:SinArray.shape[0]]
    

    weight_I = weight_function['I'].value[0, 0:240]
    weight_Q = weight_function['Q'].value[0, 0:240]    
    
    weight_function.close()
    
    W_I = np.zeros(len(weight_I) * t_avg)
    W_Q = np.zeros(len(weight_Q) * t_avg)

    
    for i in range(len(weight_I)):
        W_I[i * t_avg : (i+1) * t_avg] = weight_I[i]
        W_Q[i * t_avg : (i+1) * t_avg] = weight_Q[i]
    
#    print SinArray.shape
#    print weight_I.shape
#    print W_Q.shape
    weighted_SinArray = SinArray * W_Q + CosArray * W_I
    weighted_CosArray = -SinArray * W_I + CosArray * W_Q
    
    return (weighted_SinArray, weighted_CosArray)
    


def alazar_premesurement_setting(t_avg, points_per_record, num_records, num_sequences, weight_function, demodulation = True):
      
    correction_points = points_per_record % 32
    if correction_points != 0: # check if not a multiple of 32
        points_per_record += (32-correction_points)
    points_per_cycle = 20
    size_of_point = 4 # bytes
    MIN_POINTS_PER_RECORD = 128
    bytes_per_record = 2 * (size_of_point * max(points_per_record, MIN_POINTS_PER_RECORD))
    

    
    total_bytes = bytes_per_record * num_records
    stride = 20 # for now we are not using this stride, set it equal to the t_avg
    
    MB25 = 26214400 # 25 MB
    num_buffers = np.ceil(total_bytes/MB25)
    MAX_NUM_BUFFERS = 81 # 2*(1024**3) / 25* (1024**2) ie 2GB/25MB
    num_ram_buffers = min(81, num_buffers)
    cycles_per_record = (points_per_record - t_avg) // stride + 1    

    
    record_per_buffer = int(num_records / num_ram_buffers)
    new_num_records = num_records
    if record_per_buffer % num_sequences != 0:
        record_per_buffer = int(record_per_buffer / num_sequences) * num_sequences
        new_num_records = record_per_buffer * num_ram_buffers

    if demodulation: 
        SinArray = np.arange(points_per_record)
        CosArray = np.arange(points_per_record)        
        SinArray = np.sin(2 * np.pi * SinArray / points_per_cycle) * np.sqrt(2 / t_avg)
        CosArray = np.cos(2 * np.pi * CosArray / points_per_cycle) * np.sqrt(2 / t_avg)
    else: 
        SinArray = np.ones(points_per_record)
        CosArray = np.ones(points_per_record)
    
    if weight_function['use_weight_function']:
#        print 'weighted'
        demode_window_length = weight_function['demode_window_length'] * t_avg
        demode_window_start = weight_function['demode_window_start'] * t_avg
        filename = weight_function['filename']
        for start in demode_window_start:
            print(demode_window_length)
            (SinArray[start : start + demode_window_length], 
             CosArray[start : start + demode_window_length]) = use_weight_function(filename, 
                                                                SinArray[start : start + demode_window_length], 
                                                                CosArray[start : start + demode_window_length],
                                                                t_avg)
    
    
    
    SinArray = np.tile(SinArray, record_per_buffer)
    CosArray = np.tile(CosArray, record_per_buffer)    
    
    
    return (MAX_NUM_BUFFERS, cycles_per_record, num_ram_buffers, SinArray, CosArray, new_num_records)
                    
                      
def AcquireData(board, measurement_parameters, weight_function, use_AWG=True, AWG=None, AWG2=None, demodulation = True):
    if use_AWG:
#        import time
#        import qt
#        AWG = qt.instruments['AWG']
        if AWG != None: 
            AWG.stop()
        if AWG2 != None: 
            AWG2.stop()
        time.sleep(3)
#        qt.msleep(3)
        
    
    t_avg = measurement_parameters['t_avg']
    points_per_record = measurement_parameters['points_per_record']
    num_records = measurement_parameters['num_records']
    num_sequences = measurement_parameters['num_sequences']
    record_average = measurement_parameters['record_average']
    
    (MAX_NUM_BUFFERS, cycles_per_record, num_ram_buffers, SinArray, CosArray, new_num_records) = alazar_premesurement_setting(t_avg, 
                                                                                                                              points_per_record, 
                                                                                                                              num_records, 
                                                                                                                              num_sequences,
                                                                                                                              weight_function, 
                                                                                                                              demodulation = demodulation)   
    
    if not record_average:
        print(f"Num_records: {num_records}\nCycles_per_record: {cycles_per_record}")
        I_out = np.zeros((num_records, cycles_per_record))
        Q_out = np.zeros((num_records, cycles_per_record))
        ref_I = np.zeros((num_records, cycles_per_record))
        ref_Q = np.zeros((num_records, cycles_per_record))

    # No pre-trigger samples in NPT mode
    preTriggerSamples = 0

    # TODO: Select the number of samples per record.
    postTriggerSamples = points_per_record
    
    # TODO: Select the number of records per DMA buffer.
    recordsPerBuffer = int(new_num_records / num_ram_buffers)
    
    # TODO: Select the number of buffers per acquisition.
    buffersPerAcquisition = num_ram_buffers
    
    # TODO: Select the active channels.
    channels = ats.CHANNEL_A | ats.CHANNEL_B
    print(f"CHANNELS: {channels}")
    channelCount = 0
    for c in ats.channels:
        channelCount += (c & channels == c)
        
    # Compute the number of bytes per record and per buffer
    memorySize_samples, bitsPerSample = board.getChannelInfo()
    bytesPerSample = (bitsPerSample.value + 7) // 8
    samplesPerRecord = preTriggerSamples + postTriggerSamples
    bytesPerRecord = bytesPerSample * samplesPerRecord
    bytesPerBuffer = bytesPerRecord * recordsPerBuffer * channelCount

    # TODO: Select number of DMA buffers to allocate
    bufferCount = 10

    # Allocate DMA buffers
    sample_type = ctypes.c_uint8
    if bytesPerSample > 1:
        sample_type = ctypes.c_uint16

    buffers = []
    for i in range(bufferCount):
        buffers.append(ats.DMABuffer(sample_type, bytesPerBuffer))
    
    # Set the record size
    board.setRecordSize(preTriggerSamples, postTriggerSamples)

    recordsPerAcquisition = int(recordsPerBuffer * buffersPerAcquisition)
    # Configure the board to make an NPT AutoDMA acquisition
    board.beforeAsyncRead(channels,
                          -preTriggerSamples,
                          samplesPerRecord,
                          recordsPerBuffer,
                          recordsPerAcquisition,
                          ats.ADMA_EXTERNAL_STARTCAPTURE | ats.ADMA_NPT)
    


    # Post DMA buffers to board
    for buffer in buffers:
        board.postAsyncBuffer(buffer.addr, buffer.size_bytes)

#    start = time.clock() # Keep track of when acquisition started
    try:
        board.startCapture() # Start the acquisition
        print("Capturing %d buffers. Press <enter> to abort" %
              buffersPerAcquisition)
        buffersCompleted = 0
        bytesTransferred = 0
        
        if buffersCompleted == 0 and use_AWG:
            AWG2.run()
            time.sleep(0.5)
            AWG.run()
#            qt.msleep(1)  
            time.sleep(0.5)
        
        
        while (buffersCompleted < buffersPerAcquisition and not
               ats.enter_pressed()):

            # Wait for the buffer at the head of the list of available
            # buffers to be filled by the board.
            print(buffersCompleted % len(buffers))
            buffer = buffers[buffersCompleted % len(buffers)]
            print(buffer.addr)
            board.waitAsyncBufferComplete(buffer.addr, timeout_ms = 3000)
            bytesTransferred += buffer.size_bytes
            
            
            if record_average:
                (I_temp, Q_temp, ref_I_temp, ref_Q_temp) = single_buffer(buffer.buffer, recordsPerBuffer, cycles_per_record, t_avg, SinArray, CosArray, num_sequences, record_average, demodulate = demodulation)
                print(f'Buffers Completed: {buffersCompleted}')
                
                if buffersCompleted == 0:
                    I_out = I_temp
                    Q_out = Q_temp
                    ref_I = ref_I_temp
                    ref_Q = ref_Q_temp
                else:
                    I_out += I_temp
                    Q_out += Q_temp 
                    ref_I += ref_I_temp
                    ref_Q += ref_Q_temp

            elif not record_average:
                #this fills in a 2d array one row at a time
                
                (I_out[buffersCompleted*recordsPerBuffer: (buffersCompleted+1)*recordsPerBuffer], 
                 Q_out[buffersCompleted*recordsPerBuffer: (buffersCompleted+1)*recordsPerBuffer], 
                 ref_I[buffersCompleted*recordsPerBuffer: (buffersCompleted+1)*recordsPerBuffer], 
                 ref_Q[buffersCompleted*recordsPerBuffer: (buffersCompleted+1)*recordsPerBuffer]) = single_buffer(buffer.buffer, recordsPerBuffer, cycles_per_record, t_avg, SinArray, CosArray, num_sequences, record_average, demodulate = demodulation)
            
            buffersCompleted += 1               
            
            # Add the buffer to the end of the list of available buffers.
            board.postAsyncBuffer(buffer.addr, buffer.size_bytes)
            
    finally:
        board.abortAsyncRead()
              
        
    # Compute the total transfer time, and display performance information.
    '''
    transferTime_sec = time.clock() - start
    print("Capture completed in %f sec" % transferTime_sec)
    buffersPerSec = 0
    bytesPerSec = 0
    recordsPerSec = 0
    if transferTime_sec > 0:
        buffersPerSec = buffersCompleted / transferTime_sec
        bytesPerSec = bytesTransferred / transferTime_sec
        recordsPerSec = recordsPerBuffer * buffersCompleted / transferTime_sec
    print("Captured %d buffers (%f buffers per sec)" %
          (buffersCompleted, buffersPerSec))
    print("Captured %d records (%f records per sec)" %
          (recordsPerBuffer * buffersCompleted, recordsPerSec))
    print("Transferred %d bytes (%f bytes per sec)" %
          (bytesTransferred, bytesPerSec))
    '''
    if record_average:
        I_out = I_out / (num_records / num_sequences)
        Q_out = Q_out / (num_records / num_sequences)
        ref_Q = ref_Q / (num_records / num_sequences)
        ref_I = ref_I / (num_records / num_sequences)
    elif not record_average:
        pass
    
    return (I_out, Q_out, ref_I, ref_Q)                       
                         
                         
                         
                         
                         
                         
                         
                         
                         
                         
                         
                         
                         
                         
                         
                         
                         
                         
                         
                         
                         
                         
                         
                         
                         
                         
                         
                         
                         
                         
                         
                         
                         