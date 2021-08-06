from time import sleep
from pipeline import Pipeline, Message
from render import Render

class Console:
    def __init__(self, pipeline):
        self.pipeline = pipeline

    def listen(self):
        for typ in self.pipeline.messages:
            for msg in self.pipeline.messages[typ]:
                print(msg)

if __name__ == "__main__":
    bus = Pipeline()
    cmd = Console(bus)
    renderer = Render()

    while True:
        renderer.sendRequest(bus)
        cmd.listen()
        sleep(1)


        
