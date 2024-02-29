from struct import unpack
from BaseHandlers import DecodedDataHandler


class Packet :
    "Packet decoder. Transform raw bytes to chunk of data interpreted by the codecs"

    DATA_FORMAT = "=BBhhhhhhhhhhhhii"

    def fromstr(strdata):
        "Create a packet from the hex representation of raw data"

        return Packet(bytes.fromhex(strdata))


    def __init__(self, rawdata) -> None:
        "Constructor, rawdata is supposed to be bytes"

        self.raw = list(unpack(Packet.DATA_FORMAT,rawdata))


    @property
    def id(self):
        "Returns the id from the rawdata packet"

        return self.raw[0]


    def decode(self, codec:list, handler : DecodedDataHandler):
        """Apply codec and transfer the result to the handler
        
        Loop over the raw data decoded using the DATA_FORMAT, then apply sequentially
        the triplets from the codec list and pass the result to the handler. 
        codec : a list of triplets 
                (transformation_function, 'name of the property', 'unit')
        handler : the handler to be called
        """
        
        for i,f in enumerate(codec) :
            converted_value = f[0](self.raw[i])
            if(converted_value):
                handler.handle_property(f[1], converted_value, f[2])
