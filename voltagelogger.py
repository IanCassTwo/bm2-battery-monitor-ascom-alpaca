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
        self.csvlogger = self._init_logging()
        self.interval = Config.interval
        self.prefix = Config.prefix
        self.running = False
        self.scheduler = sched.scheduler(time.time, time.sleep)
        self.thread = threading.Thread(target=self._run_scheduler)
        self.thread.daemon = True

    def start(self):
        if not self.running:
            self.logger.info("CSV logger started")
            self.client.connect("logger")
            self.running = True
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

    def _log_voltage(self):
        if self.running:
            if not self.client.isConnected("logger"):
                self.logger.warn("Client is not connected. Restarting logger.")
                self.restart()
            voltage = self.client.getVoltage()
            self.csvlogger.info(f"{time.time()},{voltage}")
            self._schedule_next()

    def _schedule_next(self):
        if self.running:
            self.scheduler.enter(self.interval, 1, self._log_voltage)

    def _run_scheduler(self):
        self.scheduler.run()

    def _init_logging(self):

        logging.basicConfig(level=Config.log_level)
        logger = logging.getLogger('VoltageLogger')
        formatter = logging.Formatter('%(message)s')
        handler = logging.handlers.RotatingFileHandler('logs/voltages.csv',
                                                        mode='w',
                                                        delay=True,     # Prevent creation of empty logs
                                                        maxBytes=Config.max_size_mb * 1000000,
                                                        backupCount=Config.num_keep_logs)
        handler.setLevel(Config.log_level)
        handler.setFormatter(formatter)
        handler.doRollover()                                            # Always start with fresh log
        logger.addHandler(handler)
        logger.info("timestamp,voltage")
        return logger