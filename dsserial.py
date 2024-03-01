from datetime import datetime

import serial


DATA_HEAD = b"DATA:"

class SerialSource:
    "Data source from a serial device where the TETRIS hardware gateway is plugged."
    
    def __init__(self, device : str) -> None:
        self.file = serial.Serial(device)

    def __iter__(self):
        return self

    def __next__(self):
        while(True):
            line = self.file.readline()
            if (line.startswith(DATA_HEAD)):
                data = line.split(DATA_HEAD)[1].decode().strip()
                return datetime.now(),data

        
        