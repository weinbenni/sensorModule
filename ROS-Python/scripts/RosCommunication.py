class RosCommunicationUint16(object):
    def __init__(self):
        self.__uint16Data = 0

    def callback(self, msg):
        self.__uint16Data = msg.data
        
    def GetUINT16Data(self):
        return self.__uint16Data
