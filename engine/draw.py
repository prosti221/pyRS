from pipeline import Message
from module import Module

class Draw(Module):

    def __init__(self):
        Module.__init__(self, "Draw")

    def handleRequest(self, pipeline):
        pass

    def sendRequest(self, pipeline):
        msg = Message(msg_type=self.name, msg_name="RENDER_LINK", msg_param={'x':1, 'y':2, 'z':3})
        pipeline.postMsg(msg)
