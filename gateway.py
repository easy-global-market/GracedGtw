# Import config first, so take a chance to configure logging properly 
from config import devices, SDEVICE, handler

# Other imports
import argparse
from packet import Packet

# Local logging
import logging
log = logging.getLogger(__name__)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(
                    prog='TETRIS IoT Gateway',
                    description='Decode and transmit IoT data packets',
                    epilog='TETRIS/EGM - GRACED Project')
    parser.add_argument('-f','--file',action='store')
    parser.add_argument("-c", "--create", action="store_true", help="Update device entities before running")
    parser.add_argument("-l", "--logfile", action="store", help="Log the processed timestamp and data packet in a file in a format readable by the -f option")
    args = parser.parse_args()
    print(args)

    if (args.logfile):
        logfile = open(args.logfile,"a")
    else:
        logfile = None

    # Entities updater
    if (args.create) :
        from config import create_entities
        create_entities()
        exit(1)

    # Setup input stream
    if (not args.file) :
        import dsserial
        datasource = dsserial.SerialSource(SDEVICE) 
    else :
        import dsfile
        datasource = dsfile.FileSource(args.file)
 
    device_decoder = {k:v[0] for k,v in devices.items()}

    # Process the stream
    for time_stamp, data in datasource:
        if (logfile):
            logfile.write(f"{time_stamp.isoformat()},{data}\n")
        packet = Packet.fromstr(data)
        codec = device_decoder.get(packet.id)
        if (codec) :
            handler.begin(packet.id, time_stamp)
            packet.decode(codec, handler)
            handler.end()
        else:
            log.warning(f"No CODEC for {packet.id}")
                