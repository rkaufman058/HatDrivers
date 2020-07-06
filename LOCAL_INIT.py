# -*- coding: utf-8 -*-
"""
Created on Wed Jun 24 11:05:31 2020

@author: Hatlab_3
"""

import matplotlib.pyplot as plt
import numpy as np
import qcodes as qc
from qcodes import Instrument
import ctypes


from hatdrivers.Agilent_ENA_5071C import Agilent_ENA_5071C
from hatdrivers.Keysight_N5183B import Keysight_N5183B
from hatdrivers.Yokogawa_GS200 import YOKO
from hatdrivers.SignalCore_sc5511a import SignalCore_sc5511a
from hatdrivers.MiniCircuits_Switch import MiniCircuits_Switch
from hatdrivers.switch_control import SWT as SWTCTRL
from hatdrivers.Keysight_MXA_N9020A import Keysight_MXA_N9020A
# from hatdrivers.YROKO import YROKO_Client

Instrument.close_all()

MXA = Keysight_MXA_N9020A("MXA", address = 'TCPIP0::169.254.180.116::INSTR')
#%%
VNA = Agilent_ENA_5071C("vna", address = "TCPIP0::169.254.152.68::inst0::INSTR", timeout = 30)

SigGen = Keysight_N5183B("SigGen", address = "TCPIP0::169.254.29.44::inst0::INSTR")
QGen = Keysight_N5183B("QGen", address = "TCPIP0::169.254.161.164::inst0::INSTR")
yoko2 = YOKO('yoko2', address = "TCPIP::169.254.47.131::inst0::INSTR")

dll_path = r'C:\Users\Hatlab_3\Desktop\RK_Scripts\New_Drivers\HatDrivers\DLL\sc5511a.dll'
SigCore5 = SignalCore_sc5511a('SigCore5', dll = ctypes.CDLL(dll_path), serial_number = b'10001852')

#Switches need to be initialized externally, then fed into the switch_control file explicitly now
SWT1 = MiniCircuits_Switch('SWT1',address = 'http://169.254.47.255')
SWT2 = MiniCircuits_Switch('SWT2',address = 'http://169.254.47.253')



swt_modes = { '1_to_G':['1x00xxx0','xxx11010'],
              '1_to_B':['1x00xxx0','x0xx0010'],
              '1_to_F':['1x00xxx0','xxx11111'],
              '1_to_E':['1x00xxx0','xx101010'],
                          
              '5_to_B':['xxxx10x1','x0xx0010'],              
              '5_to_G':['xxxx10x1','xxx11010'],              
              '5_to_F':['xxxx10x1','xxx11111'],              
              '5_to_E':['xxxx10x1','xx101010'],              

              '11_to_F':['1x10xxx0','xxx11010'],              
              '11_to_B':['1x10xxx0','x0xx0010'],              
              '11_to_E':['1x10xxx0','xx101010'], 
              '11_to_G':['1x10xxx0','xxx11010'],
              '11_to_A':['1x10xxx0','1x1xxx0x'],  

              '2_to_E':['xxxx00x1','xx101010'], 
              '2_to_B':['xxxx00x1','x0xx0010'], 
              '2_to_F':['xxxx00x1','xxx11111'], 
              '2_to_G':['xxxx00x1','xxx11010'], 

              '5_to_F_trans':['xxxx10x1','x1xx0111'],              
              '5_to_E_trans':['xxxx10x1','xx101111'],              
              '5_to_G_trans':['xxxx10x1','xxx11111'], 

              '2_to_B_trans':['xxxx00x1','x0xx0111'],   
              '2_to_F_trans':['xxxx00x1','x1xx0111'],
              '2_to_G_trans':['xxxx00x1','xxx11111'],   
                                         
              '11_to_B_trans':['1x10xxx0','x0xx0111'],              
              '11_to_E_trans':['1x10xxx0','xx101111'],              
              '11_to_G_trans':['1x10xxx0','xxx11111'],
                                                                    
              '1_to_B_trans':['1x00xxx0','x0xx0111'],              
              '1_to_E_trans':['1x00xxx0','xx101111'],              
              '1_to_F_trans':['1x00xxx0','x1xx0111'],

              '8_to_B_trans':['xxxxx111','x0xx0111'],
              '5_to_A_trans':['xxxx10x1','x1xx0111'],

              '8_to_A': ['xxxxx111','x1xx0010'],
              '3_to_D': ['xxxxxxxx','xx0xxx0x'],
              
              'flake_ref': ['xxxx10x1','x0xx0010'],
              'flake_trans': ['01xoxxx0','x0xx0010'] } 

SWT = SWTCTRL(SWT1,SWT2,swt_modes)

# YROKO1 = instruments.create('YROKO1','YROKO_Client')

