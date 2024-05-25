import simplepyble
import logging
import threading
import struct
import enum
from ble.encryption import decrypt

TARGET_NAME = "Battery Monitor"
CHARACTERISTIC_UUID = "0000fff4-0000-1000-8000-00805f9b34fb"
SERVICE_UUID = "0000fff0-0000-1000-8000-00805f9b34fb"

class PacketType(enum.Enum):
    VoltageReading = b"\xf5"
    HistoryCount = b"\xe7"
    StartHistory = b"\xff\xff\xfe"
    EndHistory = b"\xff\xfe\xfe"

class NotificationHandler:
    def __init__(self):
        self.logger = logging.getLogger()
        self.notification_data = 0.0

    def __call__(self, encrypted_data):        
        decrypted_data = decrypt(encrypted_data)

        def is_of_type(packet_type: PacketType) -> bool:
            return decrypted_data[0:len(packet_type.value)] == packet_type.value
        
        if is_of_type(PacketType.VoltageReading):
            self.notification_data = (struct.unpack(">H", decrypted_data[1:1 + 2])[0] >> 4) / 100
            #self.logger.info(f"Got notification: {self.notification_data}")
    
    def getNotificationData(self):
        return self.notification_data

class Client():
    def __init__(self):
        self.logger = logging.getLogger()
        self.lock = threading.Lock()
        self.peripheral = self._findPeripheral()
        self.notificationHandler = NotificationHandler()
        self._connection_count = 0
        self._module_states = {}

    def _findPeripheral(self):
        for i in range(3):
            self.logger.info(f"Searching for battery monitor [attempt #{i}]")
            adapters = simplepyble.Adapter.get_adapters()
            if len(adapters) == 0:
                self.logger.error("No adapters found")
                return None
            
            adapter = adapters[0]
            self.logger.debug(f"Selected bluetooth adapter: {adapter.identifier()} [{adapter.address()}]")

            adapter.scan_for(3000)

            peripherals = adapter.scan_get_results()

            for p in peripherals:
                if p.identifier() == TARGET_NAME:
                    self.logger.info(f"Found {p.identifier()} [{p.address()}]")
                    return p
    
    def isConnected(self, id):
        if self.lock:
            if self.peripheral != None:
                if not self.peripheral.is_connected():
                    # We're disconnected!
                    self._module_states = {}
                    return False
                return self._module_states.get(id, False) and self.peripheral.is_connected()
            
            return False

    def getVoltage(self):
        return float(self.notificationHandler.getNotificationData())

    def connect(self, id):
        self.logger.debug(f"connect called by {id}")
        with self.lock:
            if self._connection_count == 0:
                self._connect()
            self._connection_count += 1
            self._module_states[id] = True

    def disconnect(self, id):
        self.logger.debug(f"disconnect called by {id}")
        with self.lock:
            if id in self._module_states and self._module_states[id]:
                self._module_states[id] = False
                self._connection_count -= 1
                if self._connection_count == 0:
                    self._disconnect()

    def _connect(self):
        if self.peripheral == None:
            self.peripheral = self._findPeripheral()
            if self.peripheral == None:
                self.logger.fatal(f"Can't find {TARGET_NAME}")
                raise RuntimeError(f"Can't find {TARGET_NAME}")

        if self.peripheral.is_connected() == False:            
            self.peripheral.connect()
            self.peripheral.notify(SERVICE_UUID, CHARACTERISTIC_UUID, self.notificationHandler)

    def _disconnect(self):
            if self.peripheral != None:
                self.peripheral.disconnect()      