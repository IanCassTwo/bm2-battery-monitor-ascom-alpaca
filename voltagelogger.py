import threading
import sched
import time
import csv
from datetime import datetime
from ble.client import Client
from config import Config
import logging

class VoltageLogger:
    def __init__(self, client):
        self.client = client
        self.logger = logging.getLogger()
        self.interval = Config.interval
        self.prefix = Config.prefix
        self.running = False
        self.scheduler = sched.scheduler(time.time, time.sleep)
        self.thread = threading.Thread(target=self._run_scheduler)
        self.thread.daemon = True
        self.csvfile = None
        self.csvwriter = None

    def start(self):
        if not self.running:
            self.logger.info("CSV logger started")
            self.client.connect("logger")
            self.running = True
            timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
            filename = f"logs/{self.prefix}_{timestamp}.csv"
            self.csvfile = open(filename, 'a', newline='')
            self.csvwriter = csv.writer(self.csvfile)
            self._schedule_next()
            if not self.thread.is_alive():
                self.thread = threading.Thread(target=self._run_scheduler)
                self.thread.daemon = True
                self.thread.start()

    def restart(self):
        self.stop()
        time.sleep(1)  # Add a small delay to ensure clean restart
        self.start()

    def stop(self):
        self.logger.info("CSV logger stopped")
        self.running = False
        self.client.disconnect("logger")
        self.scheduler.empty()
        if self.thread.is_alive():
            self.thread.join()
        if self.csvfile:
            self.csvfile.close()

    def _log_voltage(self):
        if self.running:
            if not self.client.isConnected("logger"):
                self.logger.warn("Client is not connected. Restarting logger.")
                self.restart()
            voltage = self.client.getVoltage()
            self.csvwriter.writerow([time.time(), voltage])
            self.csvfile.flush()
            self._schedule_next()

    def _schedule_next(self):
        if self.running:
            self.scheduler.enter(self.interval, 1, self._log_voltage)

    def _run_scheduler(self):
        self.scheduler.run()

