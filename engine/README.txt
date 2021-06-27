Goal:
    Build and engine that can simulate basic robot configuration and use DH-generator to do the math

Modules Input, Render, Scene:
    These will communicate through messages. Each module will have a handleMsg() function and postMsg() function.
    A message pipeline will keep track of these messages.



Framework:
    Draw class
    Input class #Based on some positional input, calculate joint variables.
    

Classes:
    Module()
    Msg() \\Struct-like type
    Pipeline()

Frameworks:
    Draw()
    Kinematics()

