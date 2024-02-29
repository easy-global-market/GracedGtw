import logging
log = logging.getLogger(__name__)


class DecodedDataHandler:
    """Base class to handle the encoding to a target format
    
    Defines 3 base functions :
    - begin is called once right before a packed is being decoded
    - handle property is called for each decoded value in the packet
    - end is called right after the packet was decoded
    """
    def begin(self, id, timestamp):
        """Prepare for the packet decoding
        
        id : device id as decoded from the first bytes of the packet
        timestamp : a datetime object
        """
        pass

    def handle_property(self, name, value, unit):
        """ Handle the data from a decoded property
        
        name : name of the decoded property
        value : value decoded
        unit : unit (see UNECE/CEFACT Trade Facilitation Recommendation No.20)
        """
        pass

    def end(self):
        "Called one at the end of a packet decoding to give a chance to flush pending data."
        pass


class ListOfHandlers(DecodedDataHandler):
    "Handler that dipatches the function calls to a list of other handlers"

    def __init__(self) -> None:
        self.handlers = []

    def append(self, handler : DecodedDataHandler):
        "Append a handler to the list"
        self.handlers.append(handler)

    def begin(self, id, timestamp):
        for h in self.handlers:
            try:
                h.begin(id, timestamp)
            except:
                log.error(f"Catched exception in handler of type {type(h)} during call to begin")

    def handle_property(self, name, value, unit):
        for h in self.handlers:
            try:
                h.handle_property(name, value, unit)
            except:
                log.error(f"Catched exception in handler of type {type(h)} during call to handle_property {name=} {value=} {unit=}")

    def end(self):
        for h in self.handlers:
            try:
                h.end()
            except:
                log.error(f"Catched exception in handler of type {type(h)} during call to end")


class DebugHandler(DecodedDataHandler):
    "Debugging handler : log in DEBUG level each call to its functions."
    
    def begin(self, id, timestamp):
        self.id = id
        log.debug(f"START Handling packet : device {id} : TS={timestamp.isoformat()}")

    def handle_property(self, name:str, value, unit):
        if (name != ""):
            log.debug(f"   packet data : {name} : {value} [{unit}]")

    def end(self):
        log.debug(f"END Handling packet : device {self.id}")