import copy
import numpy as np
import pygame as pg

#window size
WIDTH = 900 
HEIGHT = 600

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

def init():
    pg.init()
    screen = pg.display.set_mode((WIDTH, HEIGHT))
    screen.fill((0, 0, 0))
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

def proj_mesh(mesh):
    for poly in mesh.m:
        if poly.isVisible(camera.pos): 
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

        pg.draw.line(screen, (255, 255, 255), (poly.vertecies[0].coord[0], poly.vertecies[0].coord[1]), (poly.vertecies[1].coord[0], poly.vertecies[1].coord[1]), 2)
        pg.draw.line(screen, (255, 255, 255), (poly.vertecies[1].coord[0], poly.vertecies[1].coord[1]), (poly.vertecies[2].coord[0], poly.vertecies[2].coord[1]), 2)
        pg.draw.line(screen, (255, 255, 255), (poly.vertecies[2].coord[0], poly.vertecies[2].coord[1]), (poly.vertecies[0].coord[0], poly.vertecies[0].coord[1]), 2)

def rotate_cube(cube, theta):
    #Do the rotations and translations
    mesh_transformed = copy.deepcopy(cube)
    transform(mesh_transformed, d_z=0, theta_y=theta, theta_z=theta)
    transform(mesh_transformed, d_x=2, d_y=2, d_z=5)
    #Scale the mesh
    scale(mesh_transformed)
    proj_mesh(mesh_transformed)
    return mesh_transformed

if __name__ == '__main__':
    screen, pg = init()
    run = True
    cube_object = Object("None")
    cube_object.load_mesh(create_cube())
    camera = Camera(0, 0, 0)
    c = 0.1
    while(run):
        for event in pg.event.get():
            if event.type == pg.QUIT:
                run = False 
        mesh = rotate_cube(cube_object.mesh, c)
        screen.fill((1, 1, 1))
        draw(mesh, screen, pg)
        pg.display.flip()
        c += 0.05
