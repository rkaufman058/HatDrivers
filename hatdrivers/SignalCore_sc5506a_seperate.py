# -*- coding: utf-8 -*-
"""
Created on Thu Aug 18 15:45:51 2019

@author: Chao
"""
import ctypes as ct
import logging
from typing import Any, Dict, Optional

from qcodes import Instrument
from qcodes.utils.validators import Numbers
from Hatlab_QCoDes_Drivers import DLLPATH

class Device_info_t(ct.Structure):
    _fields_ = [("serial_number", ct.c_uint32),
                ("module_serial_number", ct.c_uint32),
                ("firmware_revision", ct.c_float),
                ("hardware_revision", ct.c_float),
                ("calibration_date", ct.c_uint32),
                ("manufacture_date", ct.c_uint32)
                ]

class SignalCore_SC5506A(Instrument):
    def __init__(self, name: str, serial_number: str, dll=None, channel=1, debug=False, **kwargs: Any):
        super().__init__(name, **kwargs)
        if dll is not None:
            self._dll = ct.CDLL(dll)
        else:
            self._dll = ct.CDLL(DLLPATH + '//sc5506a_usb.dll')  # access dll file

        self._serial_number = ct.c_char_p(bytes(serial_number, 'utf-8'))
        if channel not in [1, 2]:
            raise TypeError("Device channel must be 1 or 2")
        self.channel = channel

        # --------------------------------define functions------------------------------
        self._OpenDevice = self._dll.sc5506a_OpenDevice
        self._CloseDevice = self._dll.sc5506a_CloseDevice
        self._RegWrite = self._dll.sc5506a_RegWrite
        self._RegRead = self._dll.sc5506a_RegRead

        self._SetFrequency = self._dll.sc5506a_SetFrequency
        self._SetPower = self._dll.sc5506a_SetPowerLevel

        # -----------------------------------------------------------------------------

        self._handle = ct.wintypes.HANDLE()
        err = self._OpenDevice(self._serial_number,
                               ct.byref(self._handle))  # try activate device to confrim the device is connected
        if err == 0 and debug:
            print('QuSigCore ' + serial_number + ' is connected')

        self._CloseDevice(self._handle)
        self._device_info = Device_info_t(0, 0, 0, 0)
        idn = self.get_idn()
        fw_version = idn["firmware_revision"]
        if fw_version < 4.0:
            raise NotImplementedError("This driver is only designed for SC5506A with firmware version >= 4.0, it seems "
                                      f"that you have firmware version=={fw_version}. You can try to update the firmware"
                                      f" using the kits given in firmwareUpdata/sc5506a_rev2_fw_update, remember to "
                                      f"carefully read the readMe.txt")
        self.do_set_auto_level_disable(0)  # setting this to 1 will lead to unstable output power
        # ------------Params-----------------------------------------------------------------
        self.add_parameter('output_status',
                           label='output_status',
                           get_cmd=self.do_get_output_status,
                           get_parser=int,
                           set_cmd=self.do_set_output_status,
                           set_parser=int,
                           vals=Numbers(min_value=0, max_value=1))

        self.add_parameter('power',
                           label='power',
                           get_cmd=self.do_get_power,
                           get_parser=float,
                           set_cmd=self.do_set_power,
                           set_parser=float,
                           unit='dBm',
                           vals=Numbers(min_value=-144, max_value=19))

        self.add_parameter('frequency',
                           label='frequency',
                           get_cmd=self.do_get_frequency,
                           get_parser=float,
                           set_cmd=self.do_set_frequency,
                           set_parser=float,
                           unit='Hz',
                           vals=Numbers(min_value=0, max_value=6e9))

        self.add_parameter('reference_source',
                           label='reference_source',
                           get_cmd=self.do_get_reference_source,
                           get_parser=int,
                           set_cmd=self.do_set_reference_source,
                           set_parser=int,
                           vals=Numbers(min_value=0, max_value=1))

        self.add_parameter('auto_level_disable',
                           label='0 = power is leveled on frequency change',
                           get_cmd=self.do_get_auto_level_disable,
                           get_parser=int,
                           set_cmd=self.do_set_auto_level_disable,
                           set_parser=int,
                           vals=Numbers(min_value=0, max_value=1))

        self.add_parameter('temperature',
                           label='temperature',
                           get_cmd=self.do_get_device_temp,
                           get_parser=float,
                           unit="C",
                           vals=Numbers(min_value=0, max_value=200))

    #
    def activate_device_control(self):
        err = self._OpenDevice(self._serial_number,
                               ct.byref(self._handle))  # activate device control, get device handle
        if err != 0:
            print('device connection error')

    #
    #
    def do_set_output_status(self, enable):
        ch_en = 2 * (self.channel - 1) + enable
        self.activate_device_control()
        completed = self._RegWrite(self._handle, ct.c_ubyte(0x12), ct.c_ulonglong(ch_en))  # set output statue
        self._CloseDevice(self._handle)  # end device control

        return completed

    def do_set_frequency(self, frequency):
        freq = ct.c_ulonglong(int(frequency))
        ch = ct.c_uint(self.channel - 1)
        self.activate_device_control()
        err = self._SetFrequency(self._handle, ch, freq)
        self._CloseDevice(self._handle)

        return err

    #
    def do_set_power(self, power):
        power = ct.c_float(power)
        ch = ct.c_uint(self.channel - 1)
        self.activate_device_control()
        err = self._SetPower(self._handle, ch, power)
        self._CloseDevice(self._handle)
        return err


    # def do_set_power(self, pwr):
    #     pwr_b = f"{int(abs(pwr)*100):016b}"
    #     if pwr < 0:
    #         pwr_b = "1" + pwr_b[1:]
    #     ch_num = 2 * (self.channel - 1)
    #     pwr_b = int(str(ch_num) + pwr_b, 2)
    #     self.activate_device_control()
    #     completed = self._RegWrite(self._handle, ct.c_ubyte(0x11), ct.c_ulonglong(pwr_b))  # set output power
    #     self._CloseDevice(self._handle)  # end device control
    #     return completed


    def do_set_auto_level_disable(self, disable):
        disable = ct.c_bool(disable)
        ch = ct.c_uint(self.channel - 1)
        self.activate_device_control()
        err = self._dll.sc5506a_DisableAutoLevel(self._handle, ch, disable)
        self._CloseDevice(self._handle)

        return err

    #
    def do_set_standby(self, stand_by_on):
        mode = 2 * (self.channel - 1) + stand_by_on
        self.activate_device_control()
        err = self._RegWrite(self._handle, ct.c_ubyte(0x15), ct.c_ulonglong(mode))  # set output statue
        self._CloseDevice(self._handle)

        return err

    #
    def do_set_reference_source(self, lock_to_external):
        self.activate_device_control()
        err = self._RegWrite(self._handle, ct.c_ubyte(0x16), ct.c_ulonglong(lock_to_external))  # set output statue
        self._CloseDevice(self._handle)

        return err

    #
    def do_get_output_status(self):
        status = ct.c_uint()
        self.activate_device_control()
        self._RegRead(self._handle, ct.c_ubyte(0x18), ct.c_ulonglong(0x00), ct.byref(status))
        self._CloseDevice(self._handle)
        status = status.value
        if self.channel == 1:
            RFout_status = (status & (1 << 19)) >> 19
            Standby_status = (status & (1 << 17)) >> 17
        else:
            RFout_status = (status & (1 << 18)) >> 18
            Standby_status = (status & (1 << 16)) >> 16

        return RFout_status and (not Standby_status)

    #
    def do_get_reference_source(self):
        status = ct.c_uint()
        self.activate_device_control()
        self._RegRead(self._handle, ct.c_ubyte(0x18), ct.c_ulonglong(0x00), ct.byref(status))
        self._CloseDevice(self._handle)
        status = status.value
        ref_status = (status & (1 << 4)) >> 4
        ref_det = (status & (1 << 5)) >> 5

        return (ref_status and ref_det)

    def do_get_frequency(self):
        freq_1 = ct.c_ulonglong()
        self.activate_device_control()
        if self.channel == 1:
            self._RegRead(self._handle, ct.c_ubyte(0x25), ct.c_ulonglong(int(0)), ct.byref(freq_1))
        else:
            self._RegRead(self._handle, ct.c_ubyte(0x25), ct.c_ulonglong(int(2)), ct.byref(freq_1))
        self._CloseDevice(self._handle)

        return freq_1.value

    def do_get_power(self):
        power_1 = ct.c_short()
        self.activate_device_control()
        if self.channel == 1:
            self._RegRead(self._handle, ct.c_ubyte(0x25), ct.c_ulonglong(int(1)), ct.byref(power_1))
        else:
            self._RegRead(self._handle, ct.c_ubyte(0x25), ct.c_ulonglong(int(3)), ct.byref(power_1))
        self._CloseDevice(self._handle)

        power = power_1.value
        if power >> 16 < 0:
            return -1 * (power & 0b0111111111111111) / 100.0
        else:
            return power_1.value / 100.0

    def do_get_auto_level_disable(self):
        status = ct.c_uint()
        self.activate_device_control()
        self._RegRead(self._handle, ct.c_ubyte(0x18), ct.c_ulonglong(0x00), ct.byref(status))
        self._CloseDevice(self._handle)
        status = status.value
        if self.channel == 1:
            autoleveldisable_status = (status & (1 << 23)) >> 23
        else:
            autoleveldisable_status = (status & (1 << 22)) >> 22

        return autoleveldisable_status

    def do_get_device_temp(self):
        temp = ct.c_float()
        self.activate_device_control()
        self._dll.sc5506a_GetTemperature(self._handle, ct.byref(temp))
        self._CloseDevice(self._handle)

        return temp.value

    def get_all(self):
        f1 = self.do_get_frequency()
        p1 = self.do_get_power()
        out = self.do_get_output_status()
        ext_lock = self.do_get_reference_source()
        print('frequency: ', f1)
        print('power: ', p1)
        print('RFout: ', out)
        print('EXTlock: ', ext_lock)

        return out, f1, p1, ext_lock

    def get_idn(self) -> Dict[str, Optional[str]]:

        temp = ct.c_float()
        self.activate_device_control()
        self._dll.sc5506a_GetDeviceInfo(self._handle, ct.byref(self._device_info))
        self._CloseDevice(self._handle)
        device_info = self._device_info
        def date_decode(date_int:int):
            date_str = f"{date_int:032b}"
            yr = f"20{int(date_str[:8],2)}"
            month = f"{int(date_str[8:16],2)}"
            day = f"{int(date_str[16:24],2)}"
            return f"{month}/{day}/{yr}"
        IDN: Dict[str, Optional[str]] = {
            'vendor': "SignalCore",
            'model': "SC5506A",
            'serial_number': self._serial_number.value.decode("utf-8"),
            "module_serial_number": hex(device_info.module_serial_number)[2:],
            'firmware_revision': device_info.firmware_revision,
            'hardware_revision': device_info.hardware_revision,
            'calibration_data': date_decode(device_info.calibration_date),
            'manufacture_date': date_decode(device_info.manufacture_date)
            }
        return IDN


if __name__ == "__main__":
    SC1 = SignalCore_SC5506A("SC1", "100024DE")
    print(SC1.frequency())