Entry points:
  - gateway.py : the command line program
  - config.py  : the configuration taken into account by gateway.py (self-documented) 

Installation :
  - clone repository
  - create/activate virtual environment (if needed)
  - pip install -r requirements.txt
  - > cp config_template.py config.py
  - Edit the config.py file to adjust to your settings

To listen the serial device, decode packets and push data to NGSI-LD
  - Plug the gateway harware 
  - do this once : 
    > python gateway.py -c
  - then, to run the gateway : (possibly in a process manager)
    > python gateway.py 

It is possible to read files as an input (for debug, testing or replay purposes)
  - python -f <FILENAME> gateway.py
  - format of the file :
    * text file
    * each line is a single packet
    * each line is composed of 2 parts separated by a ,
    * first part : the timestamp in isoformat (it will be converted using datetime.fromisoformat)
    * second part : the hex string received from the gateway hardware


> python gateway.py -h
usage: TETRIS IoT Gateway [-h] [-f FILE] [-c]

Decode and transmit IoT data packets

options:
  -h, --help            show this help message and exit
  -f FILE, --file FILE
  -c, --create          Update device entities before running

TETRIS/EGM - GRACED Project