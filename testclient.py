from ble.client import Client
import time
import logging

logging.basicConfig(level=logging.DEBUG)

client = Client()
client.connect("test")
time.sleep(1)
print(f"isConnected() {client.isConnected('test')}")
time.sleep(5)
print(f"Voltage is {client.getVoltage()}")
