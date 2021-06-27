from dataclasses import dataclass

@dataclass
class Message:
    msg_type: str # Name of the module(Render, Input, Kinematics)
    msg_name: str # Function to perform
    msg_param: dict # Required parameters

class Pipeline:
    def __init__(self):
        self.messages = {} #{type : messages[]}

    def getMsg(self, msg_type):
        if msg_type in self.messages:
            return self.messages[msg_type].pop(-1)

    def postMsg(self, msg):
        if msg.msg_type not in self.messages:
            self.messages[msg.msg_type] = [msg]
        else:
            self.messages[msg.msg_type].append(msg)
