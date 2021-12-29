"""
Library file for wire shapes for Biot-Savart solver.
"""

import sympy as sp
from numpy import sqrt, cos, sin, arccos, arctan2, arange, linspace, zeros, array, concatenate, append, around, cross, matmul, dot, pi

# Credit to <https://stackoverflow.com/questions/18646477/why-is-sin180-not-zero-when-using-python-and-numpy>
def scos(x): return sp.N(sp.cos(x))
def ssin(x): return sp.N(sp.sin(x))

def arctan2_r(y, x): return around(arctan2(y, x), decimals=5)
def arccos_r(x): return around(arccos(x), decimals=5)

class Wire:
    """
    Implements a Wire of arbitrary shape and dimensions.

    By default, the Wire has no coordinates and a current of 1A with 0 phase.
    """
    # Create a `null wire` by default, 
    def __init__(self):
        self.current = complex(1, 0)
        self.coordinates = []

    def set_current(self, modulus, theta):
        """
        Set current of wire to be modulus amperes and with a phase theta
        """
        self.current = complex(modulus, theta)
    
    def loop(self, centre, radius, n_p, orientation="xy"):
        """
        Create a loop of wire with:
            centre of loop centre (i.e. centre = (x,y) if orientation == `xy`)
            radius of loop radius
            number of points n_p
            orientation of loop orientation
        """
        t = linspace(0, 2*pi, n_p)

        match orientation:
            case "xy":
                x = centre[0] + radius * sin(t)
                y = centre[1] + radius * cos(t)
                z = zeros(n_p)
            case "xz":
                x = centre[0] + radius * sin(t)
                z = centre[1] + radius * cos(t)
                y = zeros(n_p)
            case "yz":
                y = centre[0] + radius * sin(t)
                z = centre[1] + radius * cos(t)
                x = zeros(n_p)

        self.coordinates = [x, y, z]

    def square_loop(self, centre, length, orientation = array([0, 0])):
        """
        Add a square current loop. 

        Loop is first generated in cartesian coordinates in an "xy" orientation,
            before being rotated in spherical polar coordinates according to
            orientation (theta, phi)
        """

        # Unpack orientation theta and phi
        theta, phi = orientation[0], orientation[1]

        # Generate un-rotated origin
        origin_x = centre[0] + length/2
        origin_y = centre[1] - length/2
        origin_z = centre[2]

        origin = array([origin_x, origin_y, origin_z])

        self.add_wire_element(pi/2, pi/2, length, origin)
        self.add_wire_element(pi, pi/2, length)
        self.add_wire_element(3*pi/2, pi/2, length)
        self.add_wire_element(0, pi/2, length)

        # Rotate generated square according to orientation
        for i in range(len(self.coordinates[0])):
            point = array([self.coordinates[0][i], self.coordinates[1][i], self.coordinates[2][i]])
            new_point = self.__rotate_square(point, orientation)
            self.coordinates[0][i] = new_point[0]; self.coordinates[1][i] = new_point[1]; self.coordinates[2][i] = new_point[2]

    def __magnitude(self, vec):
        """
        Returns the magnitude of a vector
        """
        return sqrt(vec.dot(vec))

    def __rotate_square(self, point, orientation):
        """
        Rotate generated square according to orientation (theta, phi)
        """

        # Unpack orientation
        theta, phi = orientation[0], orientation[1]

        # Override: if phi is set to 0, rotation will error out, so set phi to pi and do two rotations
        if phi == 0: 
            phi = pi
            reflip = True
        else:
            reflip = False

        # Unit vector of an x-y plane
        v = array([0,0,1])

        # Create a unit vector of magnitude 1 to rotate towards
        r = 1
        op = array([r*cos(theta)*sin(phi), r*sin(theta)*sin(phi), r*cos(phi)])

        # Generate unit vector of axis of rotation, u
        n = cross(v, op)
        u = n/self.__magnitude(n)

        # Calculate angle between the two vectors, alpha, and pre-calculate cos(alpha) and sin(alpha)
        alpha = arccos(dot(v, op)/(self.__magnitude(v) * self.__magnitude(op)))
        a_cos = cos(alpha); a_sin = sin(alpha)

        # Extract components of u
        u_x = u[0]; u_y = u[1]; u_z = u[2]

        # Generate rotation matrix in cartesian coordinates, r
        r = array([
            [a_cos+u_x**2*(1-a_cos), u_x*u_y*(1-a_cos)-u_z*a_sin, u_x*u_z*(1-a_cos)+u_y*a_sin],
            [u_y*u_x*(1-a_cos)+u_z*a_sin, a_cos+u_y**2*(1-a_cos), u_y*u_z*(1-a_cos)-u_x*a_sin],
            [u_z*u_x*(1-a_cos)-u_y*a_sin, u_z*u_y*(1-a_cos)+u_x*a_sin, a_cos+u_z**2*(1-a_cos)]])

        new_point = matmul(r, point)

        # If phi was overriden, perform another rotation to flip the point back again
        if reflip == True:
            return self.__rotate_square(new_point, array([0, pi]))

        return new_point





    def add_wire_element(self, theta, phi, length, origin = None):
        """
        Add a straight wire element from origin, of length length
            and azimuth theta and inclination phi
        """

        # If no origin supplied, either get the most recent vertex or start from (0, 0, 0)
        match origin:
            case None if len(self.coordinates) == 0:
                origin = array([0, 0, 0])
            case None if len(self.coordinates) != 0:
                origin = array(self.coordinates)[:, -1]

        # Create new wire element from the origin
        new_wire = self.__create_wire(origin, theta, phi, length)

        if len(self.coordinates) == 0:
            self.coordinates = new_wire
            return

        match origin: 
            case None:
                x = append(self.coordinates[0], new_wire[0][1])
                y = append(self.coordinates[1], new_wire[1][1])
                z = append(self.coordinates[2], new_wire[2][1])
            case _:
                x = concatenate((self.coordinates[0], new_wire[0]), axis=0)
                y = concatenate((self.coordinates[1], new_wire[1]), axis=0)
                z = concatenate((self.coordinates[2], new_wire[2]), axis=0)

        self.coordinates = [x, y, z]


    def __create_wire(self, origin, theta, phi, length):
        '''
        Create_Wire(self,origin,theta,phi,length)
        creates a single wire length long, starting from point
        origin, with inclination theta and Azimuth phi and
        returns its coordinates in the form [x,y,z]
        '''

        # Computes the unit vector
        ux = scos(theta) * ssin(phi)
        uy = ssin(theta) * ssin(phi)
        uz = scos(phi)

        u = array([ux, uy, uz])

        # Computes the second vertex
        vertex = origin + length * u

        x = array([origin[0], vertex[0]])
        y = array([origin[1], vertex[1]])
        z = array([origin[2], vertex[2]])

        return [x, y, z]

    def __cartesian_to_polar(self, point):
        """
        Convert point in cartesian coordinates to spherical polar.
        Requires: point of coordinates (x, y, z)
        """
        # Unpack cartesian coordinates
        x, y, z = point[0], point[1], point[2]

        r = sqrt(x**2 + y**2 + z**2)
        theta = arctan2_r(y, x)
        phi = arccos_r(z/r)

        return array([r, theta, phi])

    def __polar_to_cartesian(self, point):
        """
        Convert point in spherical polar coordinates to cartesian.
        Requires: point of coordinates (r, theta, phi)
        """
        # Unpack spherical polar coordinates
        r, theta, phi = point[0], point[1], point[2]

        x = r * scos(theta) * ssin(phi)
        y = r * ssin(theta) * ssin(phi)
        z = r * scos(phi)

        return array([x, y, z])

    def plotme(self, ax=None):
        '''Plots itself. Optional axis argument, otherwise new axes are created
        inactive until ShowPlots is called'''
        import pylab as p
        import mpl_toolkits.mplot3d.axes3d as p3

        X = self.coordinates[0]
        Y = self.coordinates[1]
        Z = self.coordinates[2]

        if ax is None:
            fig = p.figure(None)
            ax1 = p3.Axes3D(fig)
        else:
            ax1 = ax

        ax1.plot(X, Y, Z)
        ax1.set_xlabel('X')
        ax1.set_ylabel('Y')
        ax1.set_zlabel('Z')

        p.draw()

        return ax1





