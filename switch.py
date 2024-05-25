
# -*- coding: utf-8 -*-
#
# -----------------------------------------------------------------------------
# switch.py - Alpaca API responders for Switch
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
from ble.client import Client
import logging

logger = logging.getLogger()

# ----------------------
# MULTI-INSTANCE SUPPORT
# ----------------------
# If this is > 0 then it means that multiple devices of this type are supported.
# Each responder on_get() and on_put() is called with a devnum parameter to indicate
# which instance of the device (0-based) is being called by the client. Leave this
# set to 0 for the simple case of controlling only one instance of this device type.
#
maxdev = 0                      # Single instance
client: Client=None

# -----------
# DEVICE INFO
# -----------
# Static metadata not subject to configuration changes
## EDIT FOR YOUR DEVICE ##
class SwitchMetadata:
    """ Metadata describing the Switch Device. Edit for your device"""
    Name = 'BM2 Battery Monitor read-only switch device'
    Version = '0.01'
    Description = 'An ASCOM read-only switch that exposes the voltage of your battery'
    DeviceType = 'Switch'
    DeviceID = '4266b3d2-892c-4d66-8584-637955a837c8'
    Info = 'Alpaca BM2 read-only switch\nImplements ISwitch\nASCOM Initiative'
    MaxDeviceNumber = maxdev
    InterfaceVersion = 1

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
        resp.text = PropertyResponse(client.isConnected("sw"), req).json
        logger.debug(f"connected: {resp.text}")

    def on_put(self, req: Request, resp: Response, devnum: int):
        conn_str = get_request_field('Connected', req)
        conn = to_bool(conn_str)              # Raises 400 Bad Request if str to bool fails

        try:
            # --------------------------------
            ### CONNECT/DISCONNECT()PARAM) ###
            # --------------------------------
            if (conn):

                client.connect("sw")
                logger.debug("connected: Starting battery monitor")
            else:                
                logger.debug("connected: Stopping battery monitor")
                client.disconnect("sw")
            resp.text = MethodResponse(req).json
        except Exception as ex:
            resp.text = MethodResponse(req, DriverException(0x500, 'Switch.Connected failed', ex)).json

@before(PreProcessRequest(maxdev))
class description:
    def on_get(self, req: Request, resp: Response, devnum: int):
        resp.text = PropertyResponse(SwitchMetadata.Description, req).json

@before(PreProcessRequest(maxdev))
class driverinfo:
    def on_get(self, req: Request, resp: Response, devnum: int):
        resp.text = PropertyResponse(SwitchMetadata.Info, req).json

@before(PreProcessRequest(maxdev))
class interfaceversion:
    def on_get(self, req: Request, resp: Response, devnum: int):
        resp.text = PropertyResponse(SwitchMetadata.InterfaceVersion, req).json

@before(PreProcessRequest(maxdev))
class driverversion():
    def on_get(self, req: Request, resp: Response, devnum: int):
        resp.text = PropertyResponse(SwitchMetadata.Version, req).json

@before(PreProcessRequest(maxdev))
class name():
    def on_get(self, req: Request, resp: Response, devnum: int):
        resp.text = PropertyResponse(SwitchMetadata.Name, req).json

@before(PreProcessRequest(maxdev))
class supportedactions:
    def on_get(self, req: Request, resp: Response, devnum: int):
        resp.text = PropertyResponse([], req).json  # Not PropertyNotImplemented

@before(PreProcessRequest(maxdev))
class maxswitch:

    def on_get(self, req: Request, resp: Response, devnum: int):
        try:

            resp.text = PropertyResponse(1, req).json
        except Exception as ex:
            resp.text = PropertyResponse(None, req,
                            DriverException(0x500, 'Switch.Maxswitch failed', ex)).json

@before(PreProcessRequest(maxdev))
class canwrite:

    def on_get(self, req: Request, resp: Response, devnum: int):
        try:

            resp.text = PropertyResponse(False, req).json
        except Exception as ex:
            resp.text = PropertyResponse(None, req,
                            DriverException(0x500, 'Switch.Canwrite failed', ex)).json

@before(PreProcessRequest(maxdev))
class getswitch:

    def on_get(self, req: Request, resp: Response, devnum: int):

        try:
            resp.text = PropertyResponse(True, req).json
        except Exception as ex:
            resp.text = PropertyResponse(None, req,
                            DriverException(0x500, 'Switch.Getswitch failed', ex)).json

@before(PreProcessRequest(maxdev))
class getswitchdescription:

    def on_get(self, req: Request, resp: Response, devnum: int):
        try:
            resp.text = PropertyResponse("Battery Voltage", req).json
        except Exception as ex:
            resp.text = PropertyResponse(None, req,
                            DriverException(0x500, 'Switch.Getswitchdescription failed', ex)).json

@before(PreProcessRequest(maxdev))
class getswitchname:

    def on_get(self, req: Request, resp: Response, devnum: int):
        try:
            resp.text = PropertyResponse("BM2 Voltage", req).json
        except Exception as ex:
            resp.text = PropertyResponse(None, req,
                            DriverException(0x500, 'Switch.Getswitchname failed', ex)).json

@before(PreProcessRequest(maxdev))
class getswitchvalue:

    def on_get(self, req: Request, resp: Response, devnum: int):

        if not client.isConnected("sw"):
            resp.text = PropertyResponse(None, req,
                            NotConnectedException()).json
            return
        
        try:
            resp.text = PropertyResponse(client.getVoltage(), req).json
        except Exception as ex:
            resp.text = PropertyResponse(None, req,
                            DriverException(0x500, 'Switch.Getswitchvalue failed', ex)).json

@before(PreProcessRequest(maxdev))
class minswitchvalue:

    def on_get(self, req: Request, resp: Response, devnum: int):

        try:
            resp.text = PropertyResponse(9, req).json
        except Exception as ex:
            resp.text = PropertyResponse(None, req,
                            DriverException(0x500, 'Switch.Minswitchvalue failed', ex)).json

@before(PreProcessRequest(maxdev))
class maxswitchvalue:

    def on_get(self, req: Request, resp: Response, devnum: int):
        try:
            resp.text = PropertyResponse(16, req).json
        except Exception as ex:
            resp.text = PropertyResponse(None, req,
                            DriverException(0x500, 'Switch.Maxswitchvalue failed', ex)).json

@before(PreProcessRequest(maxdev))
class setswitch:

    def on_put(self, req: Request, resp: Response, devnum: int):
        resp.text = MethodResponse(req, NotImplementedException()).json

@before(PreProcessRequest(maxdev))
class setswitchname:

    def on_put(self, req: Request, resp: Response, devnum: int):
        resp.text = MethodResponse(req, NotImplementedException()).json

@before(PreProcessRequest(maxdev))
class setswitchvalue:

    def on_put(self, req: Request, resp: Response, devnum: int):
        resp.text = MethodResponse(req, NotImplementedException()).json

@before(PreProcessRequest(maxdev))
class switchstep:

    def on_get(self, req: Request, resp: Response, devnum: int):
        try:
            resp.text = PropertyResponse(0.01, req).json
        except Exception as ex:
            resp.text = PropertyResponse(None, req,
                            DriverException(0x500, 'Switch.Switchstep failed', ex)).json
