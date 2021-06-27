import pipeline

class Module:

    def __init__(self, name):
        self.name = name

    def handleRequest(self, pipeline):
        raise NotImplementedError("handleRequest")

    def sendRequest(self, pipeline):
        raise NotImplementedError("sendRequest")
        

