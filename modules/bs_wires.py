"""
Library file for wire shapes for Biot-Savart solver.
"""

from numpy import sqrt, cos, sin, arccos, linspace, zeros, array,\
    concatenate, append, cross, matmul, dot, pi, deg2rad


class Wires:
    """
    Implements a collection of Wire objects.

    Wires is the object visible to `main.py`, and is effectively a list of all wires/coils which have been created.
    """
    # Create an empty list by default
    def __init__(self):
        self.wires = []

    def print_wires_with_properties(self):
        """
        Print all the Wire objects (and their properties) in Wires.
        """
        for wire in self.wires:
            properties = vars(wire)
            for property in properties:
                print(f"{property}: {properties[property]}")
            print()  # newline as separator

    def _parse_angular_quantity(self, angle_param, unit_param=None):
        """
        Parses angular quantity and returns angle in radians.
        Assumes units provided are given in multiples of pi radians unless specified as degrees.
        """
        match unit_param:
            case ("degrees" | "degree" | "deg"):
                angle = deg2rad(angle_param)
            case _:
                angle = pi * angle_param
        return angle

    def _gen_circular_params(self, wire_params):
        """
        Unpack the params for the circular loop and return.
        """
        # Parse angular quantities in `wire_params`. If angular unit not given,
        # catch the KeyError and assume the angle is given in radians.
        try:
            # Parse angular quantities in `wire_params`
            theta = self._parse_angular_quantity(
                angle_param=wire_params["orientation"]["theta"],
                unit_param=wire_params["orientation"]["angle unit"]
            )
        except KeyError:
            theta = self._parse_angular_quantity(angle_param=wire_params["orientation"]["theta"])

        try:
            # Parse angular quantities in `wire_params`
            phi = self._parse_angular_quantity(
                angle_param=wire_params["orientation"]["phi"],
                unit_param=wire_params["orientation"]["angle unit"]
            )
        except KeyError:
            phi = self._parse_angular_quantity(angle_param=wire_params["orientation"]["theta"])

        try:
            # Parse angular quantities in `wire_params`
            phase = self._parse_angular_quantity(
                angle_param=wire_params["current"]["phase"],
                unit_param=wire_params["current"]["angle unit"]
            )
        except KeyError:
            phase = self._parse_angular_quantity(angle_param=wire_params["current"]["phase"])

        params = {
            "name": wire_params["name"],
            "shape": wire_params["shape"],
            "centre": array([
                wire_params["centre"]["x"],
                wire_params["centre"]["y"],
                wire_params["centre"]["z"],
            ]),  # (x, y, z)
            "radius": wire_params["radius"],
            "np": wire_params["number of points"],
            "n": wire_params["number of loops"],
            "orientation": array([theta, phi]),
            "current": complex(wire_params["current"]["modulus"], phase)
        }
        return params

    def _gen_square_params(self, wire_params):
        """
        Unpack the params for the square loop and return.
        """
        # Parse angular quantities in `wire_params`. If angular unit not given,
        # catch the KeyError and assume the angle is given in radians.
        try:
            # Parse angular quantities in `wire_params`
            theta = self._parse_angular_quantity(
                angle_param=wire_params["orientation"]["theta"],
                unit_param=wire_params["orientation"]["angle unit"]
            )
        except KeyError:
            theta = self._parse_angular_quantity(angle_param=wire_params["orientation"]["theta"])

        try:
            # Parse angular quantities in `wire_params`
            phi = self._parse_angular_quantity(
                angle_param=wire_params["orientation"]["phi"],
                unit_param=wire_params["orientation"]["angle unit"]
            )
        except KeyError:
            phi = self._parse_angular_quantity(angle_param=wire_params["orientation"]["theta"])

        try:
            # Parse angular quantities in `wire_params`
            phase = self._parse_angular_quantity(
                angle_param=wire_params["current"]["phase"],
                unit_param=wire_params["current"]["angle unit"]
            )
        except KeyError:
            phase = self._parse_angular_quantity(angle_param=wire_params["current"]["phase"])

        params = {
            "name": wire_params["name"],
            "shape": wire_params["shape"],
            "centre": array([
                wire_params["centre"]["x"],
                wire_params["centre"]["y"],
                wire_params["centre"]["z"],
            ]),  # (x, y, z)
            "length": wire_params["side length"],
            "dl": wire_params["discretization length"],
            "n": wire_params["number of loops"],
            "orientation": array([theta, phi]),
            "current": complex(wire_params["current"]["modulus"], phase)
        }
        return params

    def new_wire(self, wire_params):
        """
        Create a new Wire object and add to self.wires
        """
        new_wire = Wire()

        # Parse the wire_params object to extract the relevant parameters

        # Pattern match against wire_params to check what shape of wire we're creating
        match wire_params["shape"]:
            case "circle":
                params = self._gen_circular_params(wire_params)
                new_wire.circular_loop(params)
            case "square":
                params = self._gen_square_params(wire_params)
                new_wire.square_loop(params)
            case _:
                shape = wire_params["shape"]
                raise Exception(f"ERROR: Code currently only supports circular and square current loops. You provided: \"{shape}\". Please specify either \"circle\" or \"square\".")  # noqa: E501

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

    def _gen_r_matrix(self, orientation):
        """
        Generates the rotation matrix for a given combination of theta and phi.
        """
        # Unpack orientation angles theta and phi
        theta, phi = orientation[0], orientation[1]

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

    def _reorient_loop(self, orientation):
        """
        Reorients the current loop based upon the angles (theta, phi)
        Works for both square and circular current loops.
        """

        # Unpack orientation angles theta and phi
        theta, phi = orientation[0], orientation[1]

        # Generate empty variable for rotation matrix(/matrices)
        r_matrix = []

        # Failsafe: generating a rotation matrix for phi = 0 will create NaNs because it takes the cross product of
        # two parallel vectors. Instead, if phi == 0 do two rotations.
        if phi != 0:
            # Do one rotation as expected
            r_matrix.append(self._gen_r_matrix(orientation))
        else:
            # Do two rotations, each of phi = pi so that the net change in phi is 0.
            r_matrix.append(self._gen_r_matrix(array([theta, pi])))
            r_matrix.append(self._gen_r_matrix(array([0, pi])))

        # Iterate through each point in `coordinates` (x, y, z)
        for i in range(len(self.coordinates[0])):
            # Get the point to be reoriented
            point = array([self.coordinates[0][i], self.coordinates[1][i], self.coordinates[2][i]])

            # Iterate through the r_matrix and reorient
            for r in r_matrix:
                point = matmul(r, point)

            # Save the new reoriented point
            self.coordinates[0][i] = point[0]
            self.coordinates[1][i] = point[1]
            self.coordinates[2][i] = point[2]

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

        # Generate a circular loop in the x-y plane: to be rotated later
        t = linspace(0, 2*pi, self.np)

        x = params["centre"][0] + params["radius"] * sin(t)
        y = params["centre"][1] + params["radius"] * cos(t)
        z = zeros(self.np)

        self.coordinates = [x, y, z]

        # Now reorient the wire according to `orientation`
        self._reorient_loop(params["orientation"])

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

        # Generate un-rotated origin
        origin = array([
            params["centre"][0] + params["length"]/2,
            params["centre"][1] - params["length"]/2,
            params["centre"][2]]
            )

        # Add the 4 wire elements for a square loop in the x-y plane
        self.add_wire_element(pi/2, pi/2, params["length"], origin)
        self.add_wire_element(pi, pi/2, params["length"])
        self.add_wire_element(3*pi/2, pi/2, params["length"])
        self.add_wire_element(0, pi/2, params["length"])

        # Reorient the loop according to orientation
        self._reorient_loop(params["orientation"])

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
