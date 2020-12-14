# -*- coding: utf-8 -*-
"""
Created on Wed Nov 18 10:15:37 2020

@author: Hatlab_3
"""
from pprint import pprint
import time
from matplotlib import pyplot as plt
import h5py
from qcodes import Instrument, Station, find_or_create_instrument
from plottr.data import datadict_storage as dds, datadict as dd
import inspect

import numpy as np
from qcodes import Station, Instrument
from qcodes.utils import validators

from instrumentserver import QtWidgets
from instrumentserver.serialize import (
    saveParamsToFile, loadParamsFromFile, toParamDict, fromParamDict)

from instrumentserver.gui import widgetDialog
from instrumentserver.params import ParameterManager
from instrumentserver.gui.instruments import ParameterManagerGui
from instrumentserver.client import Client, ProxyInstrument

Instrument.close_all()

cli = Client()
pm = cli.create_instrument(instrument_class = 'instrumentserver.params.ParameterManager', name = 'pm')
VNA = cli.create_instrument(instrument_class = 'hatdrivers.Agilent_ENA_5071C.Agilent_ENA_5071C', name = 'VNA', address = "TCPIP0::169.254.29.44::inst0::INSTR", timeout = 30)
SigGen = cli.create_instrument(instrument_class =  "hatdrivers.Keysight_N5183B.Keysight_N5183B", name = 'SigGen', address = "TCPIP0::169.254.29.44::inst0::INSTR")
yoko2 = cli.create_instrument(instrument_class =  "hatdrivers.Yokogawa_GS200.YOKO", name = 'yoko2', address = "TCPIP::169.254.47.131::INSTR")
# dialog = widgetDialog(ParameterManagerGui(pm))