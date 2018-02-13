import numpy as np
import math

ICE=True
n_ice = 1.78
c_light = 0.29929 #m/s

if ICE:
    c_light = c_light / n_ice

nantenna=7 #8
antenna_spacing_closest = 1 #m
antenna_depth = 200. #m   

def euclideanDistance2D(r1, r2):
    distance = math.sqrt(pow((r2[0]-r1[0]) ,2) + pow((r2[1]-r1[1]) ,2))
    return distance

def timeDifference(distance):
    return distance / c_light

def getTheta(delay, spacing=None):
    if spacing == None:
        theta= np.arcsin( delay * c_light / (antenna_spacing_closest) )
    else:
        theta= np.arcsin( delay * c_light / spacing )

    return theta

#-- right now, only setup for linear array (see ANITA geometry package for extension; throwing planewaves at 3D receiver):
antenna_location= [0,1,2,3,4,6,8]

#radial position, meters
#r_ant=np.zeros(nantenna, dtype=float)

#phi_ant=np.zeros(nantenna, dtype=float)

z_ant = -1. * np.array(antenna_location)
x_ant = np.zeros(len(antenna_location))

#A5 cal pulser location, relative to z_ant, x_ant
z_cal_pulser = -2.0
x_cal_pulser = 49.0

#vertical position, meters
#z_ant=np.arange(-1.*antenna_depth, -1*antenna_depth+nantenna*antenna_spacing)[::-1]
#x_ant = r_ant * np.cos(np.radians(phi_ant)) # Antenna x positions (m)
#y_ant = r_ant * np.sin(np.radians(phi_ant)) # Antenna y positions (m)

def drawArray():
    from ..tools import myplot
    import matplotlib.pyplot as plt
    from mpl_toolkits.mplot3d import Axes3D

    fig = plt.figure()
    ax = fig.add_subplot(111, projection='3d')
    ax.scatter(x_ant, y_ant, z_ant, marker='s', color='gray', alpha=.9, s=10)

    plt.figure(figsize=(6,8))
    plt.plot(r_ant, z_ant, 's', color='blue', ms=10, alpha=.7)
    plt.xlabel('ANITA x [m]')
    plt.ylabel('ANITA z [m]')
    #plt.ylim([-8, 0])
    plt.tight_layout()
    plt.show()

if __name__=='__main__':
    drawArray()
