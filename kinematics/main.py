from sympy import *
from sympy.physics.vector import *
from velocity_kinematics import *
from dynamics import *
from link import Link

if __name__ == "__main__":
    """
        Link(link_type, link_num(i), link_length(a), link_twist(alpha), link_offset(d), joint_angle(theta))
        use symbols('x') for symbols
        Always give angles in terms of pi
    """
    #Configuration
    theta = '\u03B8'
    q = []      #joint variables
    DOF = 0     #Degrees of freedom
    links = []  #Link objects representing each link of the robot and its DH parameters

    #Forward kinematics
    T = eye(4)  #Transformation matrix from base to end effector

    #Velocity kinematics
    Jv = 0  #Linear component of the jacobian
    Jw = 0  #Angular component of the jacobian
    J = 0   #The complete jacobian [Jv Jw] (6xDOF)

    #Dynamics
    D = 0   #Inertia matrix
    C = 0   #Coriolis/centrifugal matrix
    g = 0   #gravity vector
    Ke = 0  #Total kinetic energy
    Pe = 0  #Total potential energy
  
    links.append( Link(link_type="revolute", link_num=1, link_length=0, link_twist=-pi/2, link_offset=symbols('L_1'), joint_angle=dynamicsymbols('%s_1' %(theta)) ) )
    links.append( Link(link_type="revolute", link_num=2, link_length=symbols('L_2'), link_twist=pi/2, link_offset=0, joint_angle=dynamicsymbols('%s_2' %(theta))) )
    links.append( Link(link_type="prismatic", link_num=3, link_length=0, link_twist=0, link_offset=dynamicsymbols('L_3'), joint_angle=0) )
    
    DOF = len(links)

    #Set the masses if needed
    links[0].m = symbols("m_1")
    links[1].m = symbols("m_2")
    links[2].m = symbols("m_3")

    #Fill q                                                           
    for i in range(DOF):                                                        
        if links[i].link_type == "prismatic":                                    
            q.append(links[i].link_offset)                                      
        else:                                                                   
            q.append(links[i].joint_angle) 
   
    q = Matrix(q)
    T = eye(4)

    #Forward kinematics
    for link in links: 
        T = T * link.A
  
    Jv = compute_linVel(links)
    Jw = compute_angVel(links)
    J = Jv 

    #Jacobian
    for i in range(1, 4):
        J = J.row_insert(3 + i, Jw.row(i-1))

    D, Ke = compute_kinetic(J, links, DOF, q)
    C = compute_cristoffel(D, DOF, q)

