import numpy as np
import time
import pygame as pg


WIDTH = 900 
HEIGHT = 600

near = 0.1
far = 1000.0
fov = 90.0
aspect = float(HEIGHT / WIDTH)
e = 1.0/np.tan(fov/2)


#Projection matrix
matProj = np.array([[aspect * e, 0, 0, 0],
                    [0, e, 0 ,0], 
                    [0, 0, far/(far - near), 1.0],
                    [0, 0, (-far * near)/(far -near), 0]])

class Vertex:
    def __init__(self, x, y, z):
        self.x = x
        self.y = y 
        self.z = z
        self.coord = np.array([ x,
                                y,
                                z,
                                1])

class Polygon:
    def __init__(self, vertecies):
        self.vertecies = vertecies #1x3 

class Mesh:
    def __init__(self, m):
        self.m = m

class Object:
    def __init__(self, mesh,):
        pass

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
                vertex.x = vertex.coord[0] / w
                vertex.y = vertex.coord[1] / w
                vertex.z = vertex.coord[2] / w
            vertex.coord /= w


def translate(mesh, x, y, z):
    for poly in mesh.m:
        for vertex in poly.vertecies:
            vertex.coord[0] += x; vertex.x += x;
            vertex.coord[1] += y; vertex.y += y;
            vertex.coord[2] += z; vertex.z += z;



def rotate(mesh, theta_x, theta_y, theta_z):
    Rx = np.array([[1, 0, 0, 0], 
                    [0, np.cos(np.deg2rad(theta_x)), -np.sin(np.deg2rad(theta_x)), 0], 
                    [0, np.sin(np.deg2rad(theta_x)), np.cos(np.deg2rad(theta_x)), 0],
                    [0, 0, 0, 1]])
    
    Ry = np.array([[np.cos(np.deg2rad(theta_y)), 0, np.sin(np.deg2rad(theta_y)), 0], 
                    [0, 1, 0, 0], 
                    [-np.sin(np.deg2rad(theta_y)), 0, np.cos(np.deg2rad(theta_y)), 0],
                    [0, 0, 0, 1]])


    Rz = np.array(  [[np.cos(np.deg2rad(theta_z)), -np.sin(np.deg2rad(theta_z)), 0, 0], 
                    [np.sin(np.deg2rad(theta_z)), np.cos(np.deg2rad(theta_z)), 0, 0], 
                    [0, 0, 1, theta_z/10],
                    [0, 0, 0, 1]])

    R = np.matmul(Rz, Ry)
    R = np.matmul(R, Rx)
    #R = Rx

    for poly in mesh.m:
        for vertex in poly.vertecies:
            (vertex.x, vertex.y, vertex.z) = np.dot(R[0:3, 0:3], np.array([vertex.x,vertex.y,vertex.z]))
            vertex.coord = np.dot(R, vertex.coord)

def scale(mesh):
    for poly in mesh.m:
        poly.vertecies[0].coord[0] *= 2*WIDTH
        poly.vertecies[1].coord[0] *= 2*WIDTH
        poly.vertecies[2].coord[0] *= 2*WIDTH

        poly.vertecies[0].coord[1] *= 2*HEIGHT
        poly.vertecies[1].coord[1] *= 2*HEIGHT
        poly.vertecies[2].coord[1] *= 2*HEIGHT


def draw(mesh, screen, pg):
    for poly in mesh.m:
        print('POLYS\n\n')
        print('x: {0}, {1}, {2}\n'.format(poly.vertecies[0].x, poly.vertecies[1].x, poly.vertecies[2].x))
        print('y: {0}, {1}, {2}\n'.format(poly.vertecies[0].y, poly.vertecies[1].y, poly.vertecies[2].y))
        print('z: {0}, {1}, {2}\n'.format(poly.vertecies[0].z, poly.vertecies[1].z, poly.vertecies[2].z))

        pg.draw.line(screen, (1, 1, 1), (poly.vertecies[0].coord[0], poly.vertecies[0].coord[1]), (poly.vertecies[1].coord[0], poly.vertecies[1].coord[1]), 2)
        pg.draw.line(screen, (1, 1, 1), (poly.vertecies[1].coord[0], poly.vertecies[1].coord[1]), (poly.vertecies[2].coord[0], poly.vertecies[2].coord[1]), 2)
        pg.draw.line(screen, (1, 1, 1), (poly.vertecies[2].coord[0], poly.vertecies[2].coord[1]), (poly.vertecies[0].coord[0], poly.vertecies[0].coord[1]), 2)

def rotate_cube(theta):
    #Create the cube mesh
    mesh = create_cube()
    #Do the rotations and translations
    rotate(mesh, 0, 0, theta)
    translate(mesh, 0, 0, 3)
    #Scale the mesh
    scale(mesh)
    translate(mesh, 5000, 1500, 0)
    proj_mesh(mesh)
    return mesh

if __name__ == '__main__':

    screen, pg = init()
    run = True
    c = 0.1
    while(run):
        for event in pg.event.get():
            if event.type == pg.QUIT:
                run = False 
        mesh = rotate_cube(c)
        screen.fill((255, 255, 255))
        draw(mesh, screen, pg)
        pg.display.flip()
        c += 0.5
        time.sleep(0.01)
