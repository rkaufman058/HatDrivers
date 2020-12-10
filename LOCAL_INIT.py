# -*- coding: utf-8 -*-
"""
Created on Wed Jun 24 11:05:31 2020

@author: Hatlab_3
"""

import matplotlib.pyplot as plt
import numpy as np
from qcodes import (Instrument, VisaInstrument,
                    ManualParameter, MultiParameter,
                    validators as vals, Parameter, Station)
import easygui
import ctypes

#base drivers
# from hatdrivers.Agilent_ENA_5071C import Agilent_ENA_5071C
# from hatdrivers.Keysight_P9374A import Keysight_P9374A
from hatdrivers.Keysight_N5183B import Keysight_N5183B
from hatdrivers.Yokogawa_GS200 import YOKO
from hatdrivers.SignalCore_sc5511a import SignalCore_sc5511a
from hatdrivers.MiniCircuits_Switch import MiniCircuits_Switch
from hatdrivers.switch_control import SWT as SWTCTRL
from hatdrivers.Keysight_MXA_N9020A import Keysight_MXA_N9020A
# from hatdrivers.YROKO import YROKO_Client

#customized drivers
from hatdrivers.Hat_P9374A import Hat_P9374A
from hatdrivers.Hat_ENA5071C  import Hat_ENA5071C
#Metainstruments and tools ... 
from hatdrivers.meta_instruments import Modes



#%%
# MXA = Keysight_MXA_N9020A("MXA", address = 'TCPIP0::169.254.180.116::INSTR')
# VNA = Agilent_ENA_5071C("VNA", address = "TCPIP0::169.254.169.64::inst0::INSTR", timeout = 30)
pVNA = Hat_P9374A("pVNA", address = "TCPIP0::Hatlab_3-PC::hislip0,4880::INSTR", timeout = 3)
#for little VNA: TCPIP0::Hatlab_3-PC::hislip0,4880::INSTR
#For big VNA: (RIP): TCPIP0::169.254.152.68::inst0::INSTR
#For big VNA2: TCPIP0::169.254.169.64::inst0::INSTR
SigGen = Keysight_N5183B("SigGen", address = "TCPIP0::169.254.29.44::inst0::INSTR")
# QGen = Keysight_N5183B("QGen", address = "TCPIP0::169.254.161.164::inst0::INSTR")
#%%
try: 
    yoko2 = YOKO('yoko2', address = "TCPIP::169.254.47.131::INSTR")
except: 
    print("YOKO not connected")
#%%
# # Switches need to be initialized externally, then fed into the switch_control file explicitly now
SWT1 = MiniCircuits_Switch('SWT1',address = 'http://169.254.47.255')
SWT2 = MiniCircuits_Switch('SWT2',address = 'http://169.254.47.253')

#%%update SWT Config

swt_modes = {
    "4":["xxx0xx0x", "xxxxxxxx"],
    "5":["xxx00x1x","xxxxxxxx"],
    "6":["xxx01x1x", "xxxxxxxx"],
    "A":["xxxxxxxx", "xxx10100"], 
    "B":["xxxxxxxx", "x100xx00"], 
    "G":["xxxxxxxx", "xxx11x00"]
    }

SWT = SWTCTRL(SWT1,SWT2,swt_modes)

#%% Load previous modes
Modes.load_from_folder(globals(),path = "H:\Data\Fridge Texas\Cooldown_20201203\SHARCs\SHARC41\mode_info")
new_current_center = -7.05e-5 #A
#%%SignalCores 
# dll_path = r'C:\Users\Hatlab_3\Desktop\RK_Scripts\New_Drivers\HatDrivers\DLL\sc5511a.dll'
# SigCore5 = SignalCore_sc5511a('SigCore5', dll = ctypes.CDLL(dll_path), serial_number = b'10001852')
# YROKO1 = instruments.create('YROKO1','YROKO_Client')



