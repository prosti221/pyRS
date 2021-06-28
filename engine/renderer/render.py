import time
import random
import copy
import numpy as np
import pygame as pg

#window size
WIDTH = 900 
HEIGHT = 800

#Colors
BLACK = (1, 1, 1)
WHITE = (255, 255, 255)
GREEN = (1, 255, 30)

#Perspective projection parameters
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
        #Contains an extra dimension for the matrix multiplication
        self.coord = np.array([ x, y, z, 1]) 

class Polygon:
    def __init__(self, vertecies):
        #Contains three Vertex objects describing a triangle
        self.vertecies = vertecies 

    #Find the normal of the polygon plane
    def getNormal(self):
        A = self.vertecies[1].coord[:3] - self.vertecies[0].coord[:3]
        B = self.vertecies[2].coord[:3] - self.vertecies[1].coord[:3]
        normal = np.cross(A, B)
        return normal/np.linalg.norm(normal) #returns only [x, y, z]
    
    #Check if the polygon should be visible to the camera
    def isVisible(self, camera_pos):
        normal = self.getNormal()
        similarity = np.dot(normal, self.vertecies[0].coord[:3] - camera_pos)
        if similarity < 0:
            return True
        return False

    def shader(self, color, light):
        normal = self.getNormal()
        dp = np.dot(normal, light)
        return tuple([abs(value * dp) for value in color])

#Meshes will store a collection of polygons
class Mesh:
    def __init__(self, m):
        self.m = m

#This represents scene objects
class Object:
    def __init__(self, file):
        self.file = file
        #True 3D representation of the object
        self.mesh = None 
    
    def load_mesh(self, mesh):
        self.mesh = mesh

class Camera:
    def __init__(self, x=0, y=0, z=0):
        self.pos = np.array([x, y, z])

class Light:
    def __init__(self, x=0, y=0, z=0):
        self.direction = np.array([x, y, z])/np.linalg.norm(np.array([x, y, z]))

def init():
    pg.init()
    screen = pg.display.set_mode((WIDTH, HEIGHT))
    screen.fill(BLACK)
    pg.display.flip()    
    return (screen, pg)

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
        #Project from 3D space to 2D space
        if poly.isVisible(camera.pos):
            shader = poly.shader(GREEN, light.direction)
            for vertex in poly.vertecies:
                vertex.coord = np.dot(vertex.coord, matProj)
                w = vertex.coord[-1]
                if w != 0.0:
                    vertex.coord /= w
            
            #Draw the polygon
            pg.draw.line(screen, WHITE, (poly.vertecies[0].coord[0], poly.vertecies[0].coord[1]), (poly.vertecies[1].coord[0], poly.vertecies[1].coord[1]), 2)
            pg.draw.line(screen, WHITE, (poly.vertecies[1].coord[0], poly.vertecies[1].coord[1]), (poly.vertecies[2].coord[0], poly.vertecies[2].coord[1]), 2)
            pg.draw.line(screen, WHITE, (poly.vertecies[2].coord[0], poly.vertecies[2].coord[1]), (poly.vertecies[0].coord[0], poly.vertecies[0].coord[1]), 2)
            pg.draw.polygon(surface=screen, color=shader, points=[(poly.vertecies[0].coord[0], poly.vertecies[0].coord[1]), (poly.vertecies[1].coord[0], poly.vertecies[1].coord[1]), (poly.vertecies[2].coord[0], poly.vertecies[2].coord[1])])

def rotate_cube(cube, theta):
    #Do the rotations and translations
    mesh_transformed = copy.deepcopy(cube)
    transform(mesh_transformed, d_z=0, theta_y=theta*0.2, theta_z=theta*0.6)
    transform(mesh_transformed, d_x=3, d_y=1, d_z=4)
    #Scale the mesh
    scale(mesh_transformed)
    draw(mesh_transformed, screen, pg)

if __name__ == '__main__':
    #initializing the screen
    screen, pg = init()

    #creating a cube for testing
    cube_object = Object("None")
    cube_object.load_mesh(create_cube())
    
    #setting a temporary camera and lighting direction
    camera = Camera(0, 0, 0)
    light = Light(0.23, 0.45, 0.9)
    
    c = 0.1
    run = True
    while(run):
        screen.fill(BLACK)
        for event in pg.event.get():
            if event.type == pg.QUIT:
                run = False
        rotate_cube(cube_object.mesh, c)
        pg.display.flip()
        c += 0.1
