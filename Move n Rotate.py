import numpy as np
import matplotlib.pyplot as plt
import sys
sys.path.append('.')  # or wherever you have placed Homework07.py
from Homework07 import HouseBallAnimation


def project(d):
    """
    returns the projection matrix corresponding 
    to having the viewpoint at (0,0,d)
    and the viewing plane at z=0 (the xy plane).
    """
    P = np.array([[1, 0, 0, 0],
                  [0, 1, 0, 0],
                  [0, 0, 0, 0],
                  [0, 0, -1/d, 1]])
    return P

def moveTo(start, end):
    """
    returns the matrix corresponding to moving an obj from position 
    'start' to position 'end.'
    positions are given in 3D homogeneous coordinates.
    """
    distance1 = end[0] - start[0]
    distance2 = end[1] - start[1]
    distance3 = end[2] - start[2]
    P = np.array([[1, 0, 0, distance1],
                  [0, 1, 0, distance2],
                  [0, 0, 1, distance3],
                  [0, 0, 0, 1]])
    return P

def rotate(x, y, z):
    """
    returns the matrix corresponding to first rotating a value 'x' 
    around the x-axis, 
    then rotating 'y' around the y-axis, 
    and then 'z' around the z-axis.   
    All angles are in radians. 
    The center of rotation is at point given by 'loc' 
    (3D homogeneous coord).
    These matrices obey the right-hand rule: 
    a positive rotation is counter-clockwise
    when looking along the axis of rotation 
    from the positive direction
    toward the origin.  
    """
    x_axis = np.array([[1, 0, 0, 0],
                    [0, np.cos(x), -np.sin(x), 0],
                    [0, np.sin(x), np.cos(x), 0],
                    [0, 0, 0, 1]])
    
    y_axis = np.array([[np.cos(y), 0, np.sin(y), 0],
                         [0, 1, 0, 0],
                         [-np.sin(y), 0, np.cos(y), 0],
                         [0, 0, 0, 1]])
    
    z_axis = np.array([[np.cos(z), -np.sin(z), 0, 0],
                         [np.sin(z), np.cos(z), 0, 0],
                         [0, 0, 1, 0],
                         [0, 0, 0, 1]])
    
    
    return z_axis@y_axis@x_axis

def houseTransform4(i, loc):
    """
    returns the appropriate transformation matrix for the house.  
    The center of the house before transformation is given by 'loc'.  
    The appropriate transformation depends on the
    timestep which is given by 'i'.
    """
    P = project(100).dot(rotate(0, (i/150)*2*np.pi, 0))
                         
    return P

def ballTransform4(i, loc):
    """
    returns the appropriate transformation matrix for the ball.
    The center of the ball before transformation is given by 'loc'.  
    The appropriate transformation depends on the
    timestep which is given by 'i'.
    """
    original = moveTo(loc, np.array([0,0,0,1]))
    rotation = rotate(0,0,-(i/150)* 2 * np.pi)
    moveforward = moveTo(np.array([0, 0, 0, 1]), loc + (i/150*np.array([20, 0, 0, 1])))
    return project(100)@moveforward@rotation@original


obj = HouseBallAnimation(show_axes = True)
anim = obj.animate(ballTransform4, houseTransform4)
plt.show()
