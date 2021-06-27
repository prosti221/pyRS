import numpy as np
import time
import pygame as pg
from dataclasses import dataclass

WIDTH = 1920 
HEIGHT = 1280

near = 0.1
far = 10.0
fov = 90.0
aspect = float(HEIGHT / WIDTH)
e = 1.0/np.tan(fov/2)

top = near * np.tan(fov / 2)
bottom = -top
right = aspect * top
left = -right

#Projection matrix
matProj = np.array([[e/aspect, 0, 0, 0],
                    [0, e, 0 ,0], 
                    [0, 0, (far + near)/(near - far), (2*far*near)/(near-far)],
                    [0, 0, -1, 0]])

class Vertex:
    def __init__(self, x, y, z):
        self.x = x
        self.y = y 
        self.z = z
        self.coord = np.array([ x,
                                y,
                                z,
                                1])

@dataclass
class Polygon:
    vertecies: list[Vertex] #1x3 

@dataclass
class Mesh:
    m: list[Polygon]

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

def project(polygon):
    cpy = polygon
    for vertex in cpy.vertecies:
        vertex.coord = np.dot(vertex.coord, matProj)
        w = vertex.coord[-1]
        if w != 0.0:
            vertex.x = -vertex.coord[0] / w
            vertex.y = -vertex.coord[1] / w
            vertex.z = vertex.coord[2] / w
    return cpy

def transform(mesh):
    mesh_proj = []
    for poly in mesh.m:
        poly_proj = project(poly)
        mesh_proj.append(poly_proj)
    return Mesh(mesh_proj)

def translate(mesh, x, y, z):
    mesh_trans = []
    for poly in mesh.m:
        cpy = poly
        for vertex in cpy.vertecies:
            vertex.coord[0] += x; vertex.x += x;
            vertex.coord[1] += y; vertex.y += y;
            vertex.coord[2] += z; vertex.z += z;
        mesh_trans.append(cpy)
    return Mesh(mesh_trans)

def rotateXZ(mesh, theta):
    Rx = np.array([[1, 0, 0], 
                    [0, np.cos(np.pi * np.deg2rad(theta)), -np.sin(np.pi * np.deg2rad(theta))], 
                    [0, np.sin(np.pi* np.deg2rad(theta)), np.cos(np.pi * np.deg2rad(theta))]])
    
    Rz = np.array(  [[np.cos(1.2*np.pi * np.deg2rad(theta)), -np.sin(1.2*np.pi * np.deg2rad(theta)), 0], 
                    [np.sin(1.2*np.pi * np.deg2rad(theta)), np.cos(1.2*np.pi * np.deg2rad(theta)), 0], 
                    [0, 0, 1]])
    R = np.matmul(Rx, Rz)
    mesh_rot = []
    for poly in mesh.m:
        cpy = poly
        for vertex in cpy.vertecies:
            (vertex.x, vertex.y, vertex.z) = np.dot(np.array([vertex.x,vertex.y,vertex.z]), R)
        mesh_rot.append(cpy)
    return Mesh(mesh_rot)

def scale(mesh):
    for poly in mesh.m:
        poly.vertecies[0].coord[0] *= 0.25 * WIDTH
        poly.vertecies[1].coord[0] *= 0.25 * WIDTH
        poly.vertecies[2].coord[0] *= 0.25 * WIDTH

        poly.vertecies[0].coord[1] *= 0.25 * HEIGHT
        poly.vertecies[1].coord[1] *= 0.25 * HEIGHT
        poly.vertecies[2].coord[1] *= 0.25 * HEIGHT
    return mesh

def draw(mesh, screen, pg):
    for poly in mesh.m:
        print('POLYS\n\n')
        print('x: {0}, {1}, {2}\n'.format(poly.vertecies[0].x, poly.vertecies[1].x, poly.vertecies[2].x))
        print('y: {0}, {1}, {2}\n'.format(poly.vertecies[0].y, poly.vertecies[1].y, poly.vertecies[2].y))
        print('z: {0}, {1}, {2}\n'.format(poly.vertecies[0].z, poly.vertecies[1].z, poly.vertecies[2].z))

        pg.draw.line(screen, (1, 1, 1), (poly.vertecies[0].x, poly.vertecies[0].y), (poly.vertecies[1].x, poly.vertecies[1].y), 2)
        pg.draw.line(screen, (1, 1, 1), (poly.vertecies[1].x, poly.vertecies[1].y), (poly.vertecies[2].x, poly.vertecies[2].y), 2)
        pg.draw.line(screen, (1, 1, 1), (poly.vertecies[2].x, poly.vertecies[2].y), (poly.vertecies[0].x, poly.vertecies[0].y), 2)



if __name__ == '__main__':
    mesh = create_cube()
    mesh = translate(mesh, 1, 1, 6)
    mesh = scale(mesh)
    mesh = translate(mesh, 600, 600, 0) 
    mesh = transform(mesh)
    screen, pg = init()
    run = True
    c = 0.0
    while(run):
        for event in pg.event.get():
            if event.type == pg.QUIT:
                run = False 
        mesh = rotateXZ(mesh, c)
        #mesh = translate(mesh, c, c, c)
        screen.fill((255, 255, 255))
        draw(mesh, screen, pg)
        pg.display.flip()
        time.sleep(0.01)
 
