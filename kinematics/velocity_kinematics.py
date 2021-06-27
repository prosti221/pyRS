from sympy import *
from link import Link
from latex import print_simple, print_latex

def compute_angVel(links):                                                      
    #Jw_1
    if links[0].link_type == "revolute":                                        
        Jw = [[0, 0, 1]]                                                        
    else:                                                                       
        Jw = [[0, 0, 0]]
   
    #Jw_n
    for i in range(1, len(links)):                                              
        if(links[i].link_type == "revolute"):                                   
            if(isParallelZ(links[i-1], links[i])):                              
                Jw.append(Jw[-1])                                               
            else:
                Jw.append(links[i-1].getZ())
        else:                                                                   
            Jw.append([0, 0, 0])                                                
    return Matrix(Jw).T                                                         
                                                                                
def compute_linVel(links):
    n = len(links)
    A_n = eye(4)                                                                
    for i in range(0, len(links)):                                              
        A_n = A_n*links[i].A                                                    
    o_n = trigsimp(A_n).col(3)[0:3]
    
    #Jv_1
    if links[0].link_type == "revolute":
        Jv = trigsimp(Matrix([0, 0, 1]).cross(Matrix(o_n)))
    else:
        Jv =  Matrix(links[0].getZ())                                             
    
    #Jw_n
    A_x = eye(4)                                                                
    for i in range(1, len(links)):                                              
        A_x = A_x * links[i-1].A                                                
        if links[i].link_type == "revolute":                                    
            col = Matrix(A_x.col(2)[0:3]).cross(Matrix(o_n) - Matrix(A_x.col(3)[0:3]))
            Jv = Jv.col_insert(i, col)                                          
        else:                                                                   
            Jv = Jv.col_insert(i, Matrix(A_x.col(2)[0:3]))
    
    return trigsimp(Jv)                                                         

"""                                                                                
def compute_singularities(Jv):
    det = simplify(Jv.det())
    return det                                                  
"""                                                                             
                                                                                
def isParallelZ(link_1, link_2):                                                
    z_1 = link_1.getZ()                                                         
    z_2 = link_2.getZ()                                                         
    cross = Matrix(z_1).T.cross(Matrix(z_2).T)                                  
    if sqrt(cross[0]**2 + cross[1]**2 + cross[2]**2) == 0:                      
        return True                                                             
    return False                                                                

