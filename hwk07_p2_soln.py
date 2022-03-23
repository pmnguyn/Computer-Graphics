import numpy as np

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
    from the positive direction toward the origin.  
    """
    all_zeros = np.array([1, 0, 0, 0])
    
    x_axis = np.array([[1, 0, 0, 0],
                    [0, np.cos(x), -np.sin(x), 0],
                    [0, np.sin(x), np.cos(x), 0],
                    [0, 0, 0, 1]])
    
    y_axis = np.array([[np.cos(y), 0, np.sin(y), 0],
                         [0, 1, 0, 0],
                         [-np.sin(y), 0, np.cos(y), 0],
                         [0, 0, 0, 1]])
    
    z_axis = np.array([[np.cos(z), -np.sin(z), 0, 0],
                         [np.sin(z), np.cos(z), 0, 1],
                         [0, 0, 1, 0],
                         [0, 0, 0, 1]])
    
    loc = x_axis * y_axis * z_axis * all_zeros
    return loc
    
    
def houseTransform2(i, loc):
    """
    returns the appropriate transformation matrix for the house.  
    The center of the house before transformation is given by 'loc'.  
    The appropriate transformation depends on the
    timestep which is given by 'i'.
    """
    y = 2.0 * np.pi * (i/150)
    P = np.array([[1, 0, 0, 0],
                  [0, 1, 0, 0],
                  [0, 0, 0, 0],
                  [0, 0, -1/100, 1]]).dot(np.array([[np.cos(y), 0, np.sin(y), 0],
                                                    [0, 1, 0, 0],
                                                    [-np.sin(y), 0, np.cos(y), 0],
                                                    [0, 0, 0, 1]]))
    return P
    

def ballTransform2(i, loc):
    """
    returns the appropriate transformation matrix for the ball.
    The center of the ball before transformation is given by 'loc'.  
    The appropriate transformation depends on the
    timestep which is given by 'i'.
    """
    P = project(100)
    return P
