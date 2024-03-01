from datetime import datetime


class FileSource:
    """Data source from a text file.
    
    Format of the file :
     * text file
     * each line is a single packet
     * each line is composed of 2 parts separated by a ,
     * first part : the timestamp in isoformat (it will be converted using datetime.fromisoformat)
     * second part : the hex string received from the gateway hardware
    """
    
    def __init__(self, fpath : str) -> None:
        self.file = open(fpath)

    def __iter__(self):
        return self

    def __next__(self):
        while (True):
            line = self.file.readline()
            if (line=="") :
                raise StopIteration  
            try:
                line=line.strip()
                ts,data = line.split(',',1)
            except ValueError:
                continue
            
            return datetime.fromisoformat(ts),data
        
        
        