from sympy import *
from link import Link
from IPython.display import display


init_printing(use_latex=True)
theta = '\u03B8'

def print_latex(obj, links):
    if type(obj) == list:
        for element in obj:
            cpy = Matrix(element)
            for link in links:
                cpy = cpy.subs(sin(link.joint_angle), symbols('s_%d'%(link.link_num)))
                cpy = cpy.subs(cos(link.joint_angle), symbols('c_%d'%(link.link_num)))
                #cpy = cpy.subs(link.joint_angle.diff(), symbols('\dot{q_%d}'%(link.link_num)))
            print(latex(cpy))
        return

    cpy = Matrix(obj)
    for link in links:
        if link.link_type == "revolute":
            cpy = cpy.subs(sin(link.joint_angle), symbols('s_%d'%(link.link_num)))
            cpy = cpy.subs(cos(link.joint_angle), symbols('c_%d'%(link.link_num)))
            #cpy = cpy.subs(link.joint_angle.diff(), symbols('\dot{q_%d}'%(link.link_num)))
    print(latex(cpy, mode='equation'))

def print_simple(obj, links):
    if type(obj) == list:
        for element in obj:
            cpy = Matrix(element)
            for link in links:
                if link.link_type == "revolute":
                    cpy = cpy.subs(sin(link.joint_angle), symbols('s_%d'%(link.link_num)))
                    cpy = cpy.subs(cos(link.joint_angle), symbols('c_%d'%(link.link_num)))
                    #cpy = cpy.subs(link.joint_angle, symbols('q_%d'%(link.link_num)))
            pprint(cpy)
        return

    cpy = Matrix(obj)
    for link in links:
        if link.link_type == "revolute":
            cpy = cpy.subs(sin(link.joint_angle), symbols('s_%d'%(link.link_num)))
            cpy = cpy.subs(cos(link.joint_angle), symbols('c_%d'%(link.link_num)))
            #cpy = cpy.subs(link.joint_angle, symbols('q_%d'%(link.link_num)))
    pprint(cpy)
