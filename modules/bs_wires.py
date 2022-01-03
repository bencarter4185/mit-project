"""
Library file for wire shapes for Biot-Savart solver.
"""

import matplotlib.pyplot as plt
import mpl_toolkits.mplot3d.axes3d as p3
from numpy import sqrt, cos, sin, arccos, linspace, zeros, array,\
    concatenate, append, cross, matmul, dot, pi, arccos, arctan2, ptp


class Wires:
    """
    Implements a collection of Wire objects.

    Wires is the object visible to `main.py`, and is effectively a list of all wires/coils which have been created.
    """
    # Create an empty list by default
    def __init__(self):
        self.wires = []

    def plot_wires(self, xlim=None, ylim=None, zlim=None, axes_equal=False):
        """
        Plots all wire objects on the same axis.
        """
        fig = plt.figure(None)
        ax = p3.Axes3D(fig)

        for wire in self.wires:
            ax = wire.plotme(ax, axes_equal=axes_equal)

        if xlim is not None:
            ax.axes.set_xlim3d(left=xlim[0], right=xlim[1])

        if ylim is not None:
            ax.axes.set_ylim3d(bottom=ylim[0], top=ylim[1])

        if zlim is not None:
            ax.axes.set_zlim3d(bottom=zlim[0], top=zlim[1])

        if axes_equal == True:
            ax.set_box_aspect((1, 1, 1))  # aspect ratio is 1:1:1 in data space

        plt.show()

    def print_wires_with_properties(self):
        """
        Print all the Wire objects (and their properties) in Wires.
        """
        for wire in self.wires:
            properties = vars(wire)
            for property in properties:
                print(f"{property}: {properties[property]}")
            print()  # newline as separator

    def new_wire(self, params):
        """
        Create a new Wire object and add to self.wires
        """
        new_wire = Wire()

        # Pattern match against wire_params to check what shape of wire we're creating
        match params["shape"]:
            case "circle":
                new_wire.circular_loop(params)
            case "square":
                new_wire.square_loop(params)

        # Now the wire is created, append it to our Wires object
        self.wires.append(new_wire)


class Wire:
    """
    Implements a Wire of arbitrary shape and dimensions.

    By default, the Wire has no coordinates, a current of 1A with 0 phase,
    and number of turns `n` = 1.

    Creating a loop of wire, for example, can then be done by calling the
    circular_loop() method.
    """
    # Create a `null wire` by default,
    def __init__(self):
        self.name = "Default Wire Element"
        self.shape = None
        self.current = complex(1, 0)
        self.coordinates = []
        self.n = 1
        self.np = None
        self.dl = None
        self.radius = None
        self.length = None

    def set_name(self, name):
        """
        Set name of wire
        """
        self.name = name

    def set_current(self, current):
        """
        Set current of wire to be modulus amperes and with a phase theta
        """
        self.current = current

    def set_loops(self, n):
        """
        Set number of loops in wire (coil) to be integer value n
        """
        self.n = int(n)

    def _gen_r_matrix(self, phi):
        """
        Generates the rotation matrix for a given combination of theta and phi.
        """
        # Set theta to 0
        theta = 0

        # Unit vector of an x-y plane
        v = array([0, 0, 1])

        # Create a unit vector of magnitude 1 to rotate towards
        r = 1
        v_p = array([r*cos(theta)*sin(phi), r*sin(theta)*sin(phi), r*cos(phi)])

        # Generate unit vector of axis of rotation, u
        n = cross(v, v_p)
        u = n/self._magnitude(n)

        # Calculate angle between the two vectors, alpha, and pre-calculate
        # cos(alpha) and sin(alpha)
        alpha = arccos(dot(v, v_p)/(self._magnitude(v) * self._magnitude(v_p)))
        a_cos = cos(alpha)
        a_sin = sin(alpha)

        # Extract components of u
        u_x = u[0]
        u_y = u[1]
        u_z = u[2]

        # Generate rotation matrix, r, in cartesian coordinates
        r = array([
            [a_cos+u_x**2*(1-a_cos), u_x*u_y*(1-a_cos)-u_z*a_sin, u_x*u_z*(1-a_cos)+u_y*a_sin],
            [u_y*u_x*(1-a_cos)+u_z*a_sin, a_cos+u_y**2*(1-a_cos), u_y*u_z*(1-a_cos)-u_x*a_sin],
            [u_z*u_x*(1-a_cos)-u_y*a_sin, u_z*u_y*(1-a_cos)+u_x*a_sin, a_cos+u_z**2*(1-a_cos)]
            ])

        return r

    def _magnitude(self, vec):
        """
        Returns the magnitude of a vector
        """
        return sqrt(vec.dot(vec))


    def _spherical_to_cartesian(self, point):
        """
        Return the spherical point in cartesian coordinates, assuming a right-handed coordinate system.
        """
        # Unpack point
        r = point[0]
        theta = point[1]
        phi = point[2]

        x = r * cos(theta) * sin(phi)
        y = r * sin(theta) * sin(phi)
        z = r * cos(phi)

        return array([x, y, z])


    def _cartesian_to_spherical(self, point):
        """
        Return the cartesian point in spherical coordinates, asssuming a right-handed coordinate system.
        """
        # Unpack point
        x = point[0]
        y = point[1]
        z = point[2]

        r = sqrt(x**2 + y**2 + z**2)
        theta = arctan2(y, x)
        phi = arccos(z/r)

        return array([r, theta, phi])


    def _reorient_theta_translate(self, theta, centre):
        """
        Reorients the current loop in theta and translates to new centre.
        """
        # Iterate through each point in `coordinates` (x, y, z)
        for i in range(len(self.coordinates[0])):
            # Get the point to be reoriented
            point = array([self.coordinates[0][i], self.coordinates[1][i], self.coordinates[2][i]])

            # Convert the point to spherical coordinates
            point_spherical = self._cartesian_to_spherical(point)

            # Add theta
            point_spherical[1] += theta

            # Convert back to cartesian coordinates
            point = self._spherical_to_cartesian(point_spherical)

            # Save the new reoriented point
            self.coordinates[0][i] = point[0] + centre[0]  # x
            self.coordinates[1][i] = point[1] + centre[1]  # y
            self.coordinates[2][i] = point[2] + centre[2]  # z


    def _reorient_phi(self, phi):
        """
        Reorients the current loop in phi.
        """
        # Failsafe: Code will get confused if we attempt to reorient by phi = 0. If we attempt to, return
        if phi == 0:
            return

        # Generate rotation matrix
        r = self._gen_r_matrix(phi)
        
        # Iterate through each point in `coordinates` (x, y, z)
        for i in range(len(self.coordinates[0])):
            # Get the point to be reoriented
            point = array([self.coordinates[0][i], self.coordinates[1][i], self.coordinates[2][i]])

            # Iterate through the r_matrix and reorient
            point = matmul(r, point)

            # Save the new reoriented point
            self.coordinates[0][i] = point[0]  # x
            self.coordinates[1][i] = point[1]  # y
            self.coordinates[2][i] = point[2]  # z



    def _reorient_loop(self, orientation, centre):
        """
        Reorients the current loop based upon the angles (theta, phi)
        Works for both square and circular current loops.

        Order of operation:
            - generate r_matrix
            - reorient in phi, generating rotation matrix
            - convert to spherical coordinates, reorient in theta, and translate to new centre
            - translate to new centre
        """
        # Unpack orientation angles theta and phi
        theta, phi = orientation[0], orientation[1]

        # Reorient in phi
        self._reorient_phi(phi)

        # Reorient in theta
        self._reorient_theta_translate(theta, centre)

    def circular_loop(self, params):
        """
        Create a circular loop of wire with:
            centre of loop `centre` (x, y, z)
            radius of loop `radius`
            number of points `np`
            number of turns `n`
            orientation of loop `orientation` (theta, phi)

        The `orientation` of the loop is the direction of the unit vector normal to the loop
        surface in spherical coordinates. For example, a loop sitting in an x-y plane would
        be of orientation (theta, phi) = (0, 0), i.e. (0, 0, 1) in Cartesian coordinates.
        A loop in an x-z plane would have orientation (theta, phi) = (0, pi/2).
        """

        # Set name of loop
        self.name = params["name"]

        # Set shape of loop
        self.shape = params["shape"]

        # Set radius of loop
        self.radius = params["radius"]

        # Set complex current in loop
        self.current = params["current"]

        # Set number of turns of current loop
        self.n = params["n"]

        # Set number of points current loop is defined by
        self.np = params["np"]

        # Generate a circular loop in the x-y plane centred on (0, 0, 0): to be rotated and translated later
        t = linspace(0, 2*pi, self.np)

        x = params["radius"] * sin(t)
        y = params["radius"] * cos(t)
        z = zeros(self.np)

        self.coordinates = [x, y, z]

        # Now reorient the wire according to `orientation`
        self._reorient_loop(params["orientation"], params["centre"])

    def square_loop(self, params):
        """
        Create a square loop of wire with:
            centre of square loop `centre` (x, y, z)
            side length of square loop `length`
            number of turns `n`
            orientation of loop `orientation` (theta, phi

        The `orientation` of the loop is the direction of the unit vector normal to the loop
        surface in spherical coordinates. For example, a loop sitting in an x-y plane would
        be of orientation (theta, phi) = (0, 0), i.e. (0, 0, 1) in Cartesian coordinates.
        A loop in an x-z plane would have orientation (theta, phi) = (0, pi/2).
        """

        # Set name of loop
        self.name = params["name"]

        # Set shape of loop
        self.shape = params["shape"]

        # Set side length of loop
        self.length = params["length"]

        # Set complex current in loop
        self.current = params["current"]

        # Set number of turns of current loop
        self.n = params["n"]

        # Set the discretization length
        self.dl = params["dl"]

        # Generate un-rotated origin based on a centre of (0, 0, 0)
        origin = array([params["length"]/2, -params["length"]/2, 0])

        # Add the 4 wire elements for a square loop in the x-y plane
        self.add_wire_element(pi/2, pi/2, params["length"], origin)
        self.add_wire_element(pi, pi/2, params["length"])
        self.add_wire_element(3*pi/2, pi/2, params["length"])
        self.add_wire_element(0, pi/2, params["length"])

        # Reorient the loop according to orientation
        self._reorient_loop(params["orientation"], params["centre"])

    def add_wire_element(self, theta, phi, length, origin=None):
        """
        Add a straight wire element from origin, of length length
            and azimuth theta and inclination phi
        """

        # If no origin supplied, either get the most recent vertex or start from (0, 0, 0)
        # If origin supplied, add the origin to self.coordinates
        match origin:
            case None if len(self.coordinates) == 0:
                origin = array([0, 0, 0])
                add_origin = False
            case None if len(self.coordinates) != 0:
                origin = array(self.coordinates)[:, -1]
                add_origin = False
            case _:
                add_origin = True

        # Create new wire element from the origin
        new_wire = self._create_wire(origin, theta, phi, length, add_origin)

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

    def _create_wire(self, origin, theta, phi, length, add_origin):
        '''
        Create_Wire(self,origin,theta,phi,length)
        creates a single wire length long, starting from point
        origin, with inclination theta and Azimuth phi and
        returns its coordinates in the form [x,y,z]
        '''

        # Computes the unit vector
        ux = cos(theta) * sin(phi)
        uy = sin(theta) * sin(phi)
        uz = cos(phi)

        u = array([ux, uy, uz])

        # Computes the second vertex
        vertex = origin + length * u

        # Manually add the origin if it has been explicitly specified
        match add_origin:
            case True:
                x = array([origin[0], vertex[0]])
                y = array([origin[1], vertex[1]])
                z = array([origin[2], vertex[2]])
            case False:
                x = array([vertex[0]])
                y = array([vertex[1]])
                z = array([vertex[2]])

        return [x, y, z]

    def plotme(self, ax=None, axes_equal=False):
        '''Plots itself. Optional axis argument, otherwise new axes are created
        inactive until ShowPlots is called'''

        X = self.coordinates[0]
        Y = self.coordinates[1]
        Z = self.coordinates[2]

        ax.plot(X, Y, Z)
        ax.set_xlabel('X')
        ax.set_ylabel('Y')
        ax.set_zlabel('Z')

        plt.draw()

        return ax
