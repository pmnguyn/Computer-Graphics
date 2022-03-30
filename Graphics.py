import numpy as np
import matplotlib.pyplot as plt
import matplotlib.animation as animation

class HouseBallAnimation:

    def obj2flist(self, fp):
        """
        reads a standard .obj file as used in solid modeling.
        returns a list of 2-d numpy arrays, 
        in which columns are vertices of a face.
        """
        vertices = []
        faces = []
        for line in fp:
            tokens = line.split()
            # vertex lines
            if ((len(tokens) > 0) and (tokens[0] == 'v')):
                vertices.append([float(tokens[1]),
                                     float(tokens[2]),
                                     float(tokens[3])])
            # face lines
            elif ((len(tokens) > 0) and (tokens[0] == 'f')):
                # note that .obj arrays index from 1
                # each face is a set of indices into the vertex array,
                # with optional additional properties following slashes
                face = [int(t.split('/')[0])-1
                            for t in tokens[1:]] + [
                                    int(tokens[1].split('/')[0])-1]
                faces.append(face)
        coords = [np.array([vertices[i] for i in f]).T for f in faces]
        return coords

    def objCenter(self, flist):
        """
        computes an approximate object center to be used for translation, 
        rotation, etc.
        flist is a list of faces.
        """
        flat = np.concatenate(flist,axis=1)
        return (np.min(flat,axis=1) + np.max(flat,axis=1))/2.0

    def homogenize(self, flist):
        """
        convert every point in flist to homogeneous coordinates.
        flist is a list of faces.
        """
        return [np.concatenate((f,np.ones((1,np.shape(f)[1])))) for f in flist]

    def wrl2flist(self, fp):
        """
        reads a standard .wrl file as used in VRML
        returns a list of 2-d numpy arrays, 
        in which columns are vertices of a face.
        """
        vertices = []
        faces = []
        base = True
        C1 = False
        C2 = False
        F1 = False
        F2 = False
        debug = False
        for line in fp:
            tokens = line.split()
            if (len(tokens) == 0):
                continue
            elif (base and line.find("Coordinate3") != -1):
                C1 = True
                base = False
            elif (C1 and line.find("point") != -1):
                C2 = True
                C1 = False
            elif (C2 and line.find("]") == -1):
                tk = line.rstrip(',\n').split()
                vertices.append([float(tk[0]),float(tk[1]),float(tk[2])])
                if (debug): print("appending vertex {}".format(vertices[-1]))
            elif (C2 and line.find("]") != -1):
                C2 = False
                base = True
            elif (base and line.find("IndexedFaceSet") != -1):
                F1 = True
                base = False
            elif (F1 and line.find("coordIndex") != -1):
                F2 = True
                F1 = False
            elif (F2 and line.find("]") == -1):
                tk = line.split(',')
                if (tk[-2] != "-1"):
                    print("error in parsing faces; line doesnt end a face (-1)")
                faces.append([int(f) for f in tk[:-2]])
                if (debug): print("appending face {}".format(faces[-1]))
            elif (F2 and line.find("]") != -1):
                F2 = False
                base = True
        coords = [np.array([vertices[i] for i in f]).T for f in faces]
        return coords

    def scale(self, f):
        """
        returns a matrix that scales a point by f
        """
        return(np.array([[f, 0, 0, 0],
                         [0, f, 0, 0],
                         [0, 0, f, 0],
                         [0, 0, 0, 1]]).astype('float'))

    def __init__(self, show_axes = True, width = 40, close = False):
        #
        # load house wireframe
        with open('basicHouse.obj','r') as fp:
            self.house = self.obj2flist(fp)
        self.house = self.homogenize(self.house)
        houseScale = 3.0
        # place house centered at the origin
        d = np.array([0., 0, 0, 1]) - self.objCenter(self.house) 
        M = np.array([[1, 0, 0, d[0]], 
                      [0, 1, 0, d[1]], 
                      [0, 0, 1, d[2]], 
                      [0, 0, 0,   1]]).astype('float')
        self.house = [self.scale(houseScale) @ M @ f for f in self.house]
        #
        # load ball wireframe
        # ball has radius equal to ballScale feet
        with open('snub_icosidodecahedron.wrl','r') as fp:
            self.ball = self.wrl2flist(fp)
        self.ball = self.homogenize(self.ball)
        ballScale = 3.0
        # place ball centered at this position
        d = np.array([10.0, -3, 0., 1]) - self.objCenter(self.ball)
        M = np.array([[1, 0, 0, d[0]],
                      [0, 1, 0, d[1]],
                      [0, 0, 1, d[2]],
                      [0, 0, 0,   1]]).astype('float')
        self.ball = [self.scale(ballScale) @ M @ f for f in self.ball]
        #
        # set up plot
        self.fig = plt.figure(figsize = (8,8))
        self.ax = plt.axes(xlim=(-30, 70), ylim=(-width, width))
        plt.axis('off')
        # force the plot to be width wide and high
        plt.plot(-(width-10), -width/2, '')
        plt.plot(width+20, width/2, '')
        plt.axis('equal')
        if show_axes:
            plt.arrow(0, 0, 40,  0, width = 0.25, head_width = 1.5)
            plt.arrow(0, 0,  0, 40, width = 0.25, head_width = 1.5)
            plt.plot(0, 0, '.', color = 'gray', markersize = 15)
            plt.text(2, width-2, 'y')
            plt.text(width-2, 2, 'x')
            plt.text(-0.5, -0.5, 'z')
        if close:
            # close in jupyter notebook so doesnt create extra still figure
            plt.close()
        #
        # create drawables
        self.ballLines = []
        for b in self.ball:
            self.ballLines += self.ax.plot([],[])
        self.houseLines = []
        for h in self.house:
            self.houseLines += self.ax.plot([],[],'r')
        
    def draw_frame(self, i, ballTransform, houseTransform):
        # called once each for each animation frame
        M = ballTransform(i+1, self.objCenter(self.ball))
        for b, l in zip(self.ballLines, self.ball):
            n = M @ l
            b.set_data(n[0]/n[3], n[1]/n[3])
        M = houseTransform(i+1, self.objCenter(self.house))
        for b, l in zip(self.houseLines, self.house):
            n = M @ l
            b.set_data(n[0]/n[3], n[1]/n[3])
        
    # To run animation in jupyter notebook:
    #
    # %matplotlib inline
    # from IPython.display import HTML
    # HTML(obj.animate(ballTransform, houseTransform).to_jshtml())
    #
    # To run animation in python interpreter:
    #
    # import matplotlib.pyplot as plt
    # obj.animate(ballTransform, houseTransform)
    # plt.show()

    def animate(self, ballTransform, houseTransform, n_frames = 150):
        return animation.FuncAnimation(self.fig, 
                                       self.draw_frame,
                                       frames = n_frames, 
                                       fargs = (ballTransform,
                                                houseTransform),
                                       interval=1000/25, 
                                       repeat=False, 
                                       blit=False)


