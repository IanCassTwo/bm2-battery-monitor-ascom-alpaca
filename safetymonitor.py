
# -*- coding: utf-8 -*-
#
# -----------------------------------------------------------------------------
# safetymonitor.py - Alpaca API responders for Safetymonitor
#
# Author:   Your R. Name <your@email.org> (abc)
#
# -----------------------------------------------------------------------------
# Edit History:
#   Generated by Python Interface Generator for AlpycaDevice
#
# ??-???-????   abc Initial edit

from falcon import Request, Response, HTTPBadRequest, before
from logging import Logger
from shr import PropertyResponse, MethodResponse, PreProcessRequest, \
                get_request_field, to_bool
from exceptions import *        # Nothing but exception classes
from config import Config
from bm2.client import BM2Client

logger: Logger = None

# ----------------------
# MULTI-INSTANCE SUPPORT
# ----------------------
# If this is > 0 then it means that multiple devices of this type are supported.
# Each responder on_get() and on_put() is called with a devnum parameter to indicate
# which instance of the device (0-based) is being called by the client. Leave this
# set to 0 for the simple case of controlling only one instance of this device type.
#
maxdev = 0                      # Single instance
safe = 1
connected = 0
bm2 = None

# -----------
# DEVICE INFO
# -----------
# Static metadata not subject to configuration changes
## EDIT FOR YOUR DEVICE ##
class SafetymonitorMetadata:
    """ Metadata describing the Safetymonitor Device. Edit for your device"""
    Name = 'BM2 Batter Monitor Safetymonitor'
    Version = '0.01'
    Description = 'An ASCOM Safetymonitor for the BM2 bluetooth batter monitor'
    DeviceType = 'Safetymonitor'
    DeviceID = '14c9814f-0516-4288-870a-b31d4c35111d'
    Info = 'Alpaca BM2 Safetymonitor Device\nImplements ISafetymonitor\nASCOM Initiative'
    MaxDeviceNumber = maxdev
    InterfaceVersion = 1

def start_safetymonitor_device(logger: logger):
    logger = logger
    bm2 = BM2Client(Config.addr)


# --------------------
# RESOURCE CONTROLLERS
# --------------------

@before(PreProcessRequest(maxdev))
class action:
    def on_put(self, req: Request, resp: Response, devnum: int):
        resp.text = MethodResponse(req, NotImplementedException()).json

@before(PreProcessRequest(maxdev))
class commandblind:
    def on_put(self, req: Request, resp: Response, devnum: int):
        resp.text = MethodResponse(req, NotImplementedException()).json

@before(PreProcessRequest(maxdev))
class commandbool:
    def on_put(self, req: Request, resp: Response, devnum: int):
        resp.text = MethodResponse(req, NotImplementedException()).json

@before(PreProcessRequest(maxdev))
class commandstring:
    def on_put(self, req: Request, resp: Response, devnum: int):
        resp.text = MethodResponse(req, NotImplementedException()).json

@before(PreProcessRequest(maxdev))
class connected:
    def on_get(self, req: Request, resp: Response, devnum: int):
        resp.text = PropertyResponse(connected, req).json

    def on_put(self, req: Request, resp: Response, devnum: int):
        conn_str = get_request_field('Connected', req)
        conn = to_bool(conn_str)              # Raises 400 Bad Request if str to bool fails
        try:
            # --------------------------------
            ### CONNECT/DISCONNECT()PARAM) ###
            # --------------------------------
            if (conn):
                bm2.start()
                bm2.wait_for_connected()
                connected = 1
            else:
                bm2.stop()
                connected = 0
            resp.text = MethodResponse(req).json
        except Exception as ex:
            resp.text = MethodResponse(req, DriverException(0x500, 'Safetymonitor.Connected failed', ex)).json

@before(PreProcessRequest(maxdev))
class description:
    def on_get(self, req: Request, resp: Response, devnum: int):
        resp.text = PropertyResponse(SafetymonitorMetadata.Description, req).json

@before(PreProcessRequest(maxdev))
class driverinfo:
    def on_get(self, req: Request, resp: Response, devnum: int):
        resp.text = PropertyResponse(SafetymonitorMetadata.Info, req).json

@before(PreProcessRequest(maxdev))
class interfaceversion:
    def on_get(self, req: Request, resp: Response, devnum: int):
        resp.text = PropertyResponse(SafetymonitorMetadata.InterfaceVersion, req).json

@before(PreProcessRequest(maxdev))
class driverversion():
    def on_get(self, req: Request, resp: Response, devnum: int):
        resp.text = PropertyResponse(SafetymonitorMetadata.Version, req).json

@before(PreProcessRequest(maxdev))
class name():
    def on_get(self, req: Request, resp: Response, devnum: int):
        resp.text = PropertyResponse(SafetymonitorMetadata.Name, req).json

@before(PreProcessRequest(maxdev))
class supportedactions:
    def on_get(self, req: Request, resp: Response, devnum: int):
        resp.text = PropertyResponse([], req).json  # Not PropertyNotImplemented

@before(PreProcessRequest(maxdev))
class issafe:

    def on_get(self, req: Request, resp: Response, devnum: int):

        if not connected:
            resp.text = PropertyResponse(None, req,
                            NotConnectedException()).json
            return

        # What's our current voltage?
        voltage = bm2.get_voltage()

        ## check voltage against threshold
        if voltage < Config.threshold: 
            safe = 0
        else:
            safe = 1

        try:
            resp.text = PropertyResponse(safe, req).json
        except Exception as ex:
            resp.text = PropertyResponse(None, req,
                            DriverException(0x500, 'Safetymonitor.Issafe failed', ex)).json
