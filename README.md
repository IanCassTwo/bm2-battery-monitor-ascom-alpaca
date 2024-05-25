# ASCOM Alpaca driver for the BM2 Battery Monitor

![Image of a BM2(/images/bm2.jpg)

This driver implements an ASCOM Alpaca  Safety Monitor and a read-only Switch for the BM2 Bluetooth BLE battery monitor. The motivation for writing this was to allow me to monitor the voltage of my 50ah leisure battery and to allow a clean shutdown when the voltage drops too low. The saftey monitor will trigger an event in the advanced sequencer in NINA to abort my imaging session. The actual real-time voltage level is exposed as a read-only switch.

Tested with:-
* NINA

To get this driver to work, clone this repo and install the dependencies below :-

```
pip install -r requirements.txt
```

I hope to provide a Windows binary soon

This project was made possible by the ASCOM AlpycaDevice SDK https://github.com/ASCOMInitiative/AlpycaDevice, KrystianD who worked out the encryption https://github.com/KrystianD/bm2-battery-monitor/ and SimpleBLE which is much easier to work with than Bleak https://github.com/OpenBluetoothToolbox/SimpleBLE/
