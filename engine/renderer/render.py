import numpy as np
import copy
import time
import pygame as pg


WIDTH = 900 
HEIGHT = 600

near = 0.1
far = 1000.0
fov = 90.0
aspect = float(WIDTH / HEIGHT)
e = 1.0/np.tan(fov/2)

#Camera border
top = np.tan(fov/2) * near
bottom = -top * aspect
right = top * aspect
left = bottom

#Projection matrix
matProj = np.array([[aspect * e, 0, 0, 0],
                    [0, e, 0 ,0], 
                    [0, 0, far/(far - near), 1.0],
                    [0, 0, (-far * near)/(far -near), 0]])

class Vertex:
    def __init__(self, x, y, z):
        self.coord = np.array([ x, y, z, 1])

class Polygon:
    def __init__(self, vertecies):
        self.vertecies = vertecies #1x3 

class Mesh:
    def __init__(self, m):
        self.m = m

class Object:
    def __init__(self, file):
        self.file = file
        self.mesh = None #True 3D representation of the object
    
    def load_mesh(self, mesh):
        self.mesh = mesh


def init():
    pg.init()
    screen = pg.display.set_mode((WIDTH, HEIGHT))
    screen.fill((255, 255, 255))
    pg.display.flip()
    
    return (screen, pg)


def update():
    pass

def create_cube():
    polygons = [
                #South
                Polygon( [Vertex(0, 0, 0), Vertex(0, 1, 0), Vertex(1, 1, 0)] ),
                Polygon( [Vertex(0, 0, 0), Vertex(1, 1, 0), Vertex(1, 0, 0)] ),
                
                #East
                Polygon( [Vertex(1, 0, 0), Vertex(1, 1, 0), Vertex(1, 1, 1)] ),
                Polygon( [Vertex(1, 0, 0), Vertex(1, 1, 1), Vertex(1, 0, 1)] ),

                #North
                Polygon( [Vertex(1, 0, 1), Vertex(1, 1, 1), Vertex(0, 1, 1)] ),
                Polygon( [Vertex(1, 0, 1), Vertex(0, 1, 1), Vertex(0, 0, 1)] ),

                #West
                Polygon( [Vertex(0, 0, 1), Vertex(0, 1, 1), Vertex(0, 1, 0)] ),
                Polygon( [Vertex(0, 0, 1), Vertex(0, 1, 0), Vertex(0, 0, 0)] ),

                #Top
                Polygon( [Vertex(0, 1, 0), Vertex(0, 1, 1), Vertex(1, 1, 1)] ),
                Polygon( [Vertex(0, 1, 0), Vertex(1, 1, 1), Vertex(1, 1, 0)] ),

                #Bot
                Polygon( [Vertex(1, 0, 1), Vertex(0, 0, 1), Vertex(0, 0, 0)] ),
                Polygon( [Vertex(1, 0, 1), Vertex(0, 0, 0), Vertex(1, 0, 0)] ),
                ]
    return Mesh(polygons)

def proj_mesh(mesh):
    #Check normals of polygons to decide which to project and draw
    for poly in mesh.m:
        for vertex in poly.vertecies:
            vertex.coord = np.dot(vertex.coord, matProj)
            w = vertex.coord[-1]
            if w != 0.0:
                vertex.coord /= w

def transform(mesh, theta_x=0, theta_y=0, theta_z=0, d_x=0, d_y=0, d_z=0):
    #Homogeneous transformation along the x-axis
    Rx = np.array([[1, 0, 0, d_x], 
                    [0, np.cos(np.deg2rad(theta_x)), -np.sin(np.deg2rad(theta_x)), 0], 
                    [0, np.sin(np.deg2rad(theta_x)), np.cos(np.deg2rad(theta_x)), 0],
                    [0, 0, 0, 1]])
    #Homogeneous transformation along the y-axis
    Ry = np.array([[np.cos(np.deg2rad(theta_y)), 0, np.sin(np.deg2rad(theta_y)), 0], 
                    [0, 1, 0, d_y], 
                    [-np.sin(np.deg2rad(theta_y)), 0, np.cos(np.deg2rad(theta_y)), 0],
                    [0, 0, 0, 1]])
    #Homogeneous transformation along the z-axis
    Rz = np.array(  [[np.cos(np.deg2rad(theta_z)), -np.sin(np.deg2rad(theta_z)), 0, 0], 
                    [np.sin(np.deg2rad(theta_z)), np.cos(np.deg2rad(theta_z)), 0, 0], 
                    [0, 0, 1, d_z],
                    [0, 0, 0, 1]])
    #R = R_z R_y R_x
    R = np.matmul(Rz, Ry)
    R = np.matmul(R, Rx)
    #Transform all the vertecies
    for poly in mesh.m:
        for vertex in poly.vertecies:
            vertex.coord = np.dot(R, vertex.coord)

def scale(mesh):
    for poly in mesh.m:
        poly.vertecies[0].coord[1] *= WIDTH
        poly.vertecies[1].coord[1] *= WIDTH
        poly.vertecies[2].coord[1] *= WIDTH

        poly.vertecies[0].coord[0] *= HEIGHT
        poly.vertecies[1].coord[0] *= HEIGHT
        poly.vertecies[2].coord[0] *= HEIGHT


def draw(mesh, screen, pg):
    for poly in mesh.m:
        #print('POLYS\n\n')
        #print('x: {0}, {1}, {2}\n'.format(poly.vertecies[0].x, poly.vertecies[1].x, poly.vertecies[2].x))
        #print('y: {0}, {1}, {2}\n'.format(poly.vertecies[0].y, poly.vertecies[1].y, poly.vertecies[2].y))
        #print('z: {0}, {1}, {2}\n'.format(poly.vertecies[0].z, poly.vertecies[1].z, poly.vertecies[2].z))

        pg.draw.line(screen, (1, 1, 1), (poly.vertecies[0].coord[0], poly.vertecies[0].coord[1]), (poly.vertecies[1].coord[0], poly.vertecies[1].coord[1]), 2)
        pg.draw.line(screen, (1, 1, 1), (poly.vertecies[1].coord[0], poly.vertecies[1].coord[1]), (poly.vertecies[2].coord[0], poly.vertecies[2].coord[1]), 2)
        pg.draw.line(screen, (1, 1, 1), (poly.vertecies[2].coord[0], poly.vertecies[2].coord[1]), (poly.vertecies[0].coord[0], poly.vertecies[0].coord[1]), 2)

def rotate_cube(cube, theta):
    #Do the rotations and translations
    mesh_transformed = copy.deepcopy(cube)
    transform(mesh_transformed, d_z=theta/10, theta_y=theta, theta_z=theta*0.7)
    transform(mesh_transformed, d_x=5, d_y=3, d_z=3)
    #Scale the mesh
    scale(mesh_transformed)
    proj_mesh(mesh_transformed)
    return mesh_transformed

if __name__ == '__main__':
    screen, pg = init()
    run = True
    cube_object = Object("None")
    cube_object.load_mesh(create_cube())
    c = 0.1
    while(run):
        for event in pg.event.get():
            if event.type == pg.QUIT:
                run = False 
        mesh = rotate_cube(cube_object.mesh, c)
        screen.fill((255, 255, 255))
        draw(mesh, screen, pg)
        pg.display.flip()
        c += 0.5
        time.sleep(0.01)
