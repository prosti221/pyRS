from sympy import *

class Link:                                                                    
    def __init__(self, link_type, link_num, link_length, link_twist, link_offset, joint_angle):
        self.link_type = link_type                                              
        self.link_num = link_num                                                
        self.link_length = link_length                                          
        self.link_twist = link_twist                                            
        self.link_offset = link_offset                                          
        self.joint_angle = joint_angle
        self.m = 0
                                                                                
        self.A = Matrix([[cos(self.joint_angle), -sin(self.joint_angle)*cos(self.link_twist) , sin(self.joint_angle)*sin(self.link_twist), self.link_length * cos(self.joint_angle)],
                    [sin(self.joint_angle), cos(self.joint_angle)*cos(self.link_twist) , -cos(self.joint_angle)*sin(self.link_twist), self.link_length * sin(self.joint_angle)],
                    [0, sin(self.link_twist), cos(self.link_twist), self.link_offset],
                    [0, 0, 0, 1]])                                              
    def getZ(self):                                                             
        return self.A.col(2)[0:3]                                               
                                                                                
    def getOrigin(self):                                                        
        return self.A.col(3)[0:3]                                               

