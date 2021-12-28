from numpy import cos, pi, array, sqrt, arctan2, arccos, sin, hypot
import matplotlib.pyplot as plt


# def cart2sph(x, y, z):
#     hxy = hypot(x, y)
#     r = hypot(hxy, z)
#     el = arctan2(z, hxy)
#     az = arctan2(y, x)
#     return az, el, r

# def cartesian_to_spherical(point):
#     """
#     Convert point in cartesian coordinates to spherical polar.
#     Requires: point of coordinates (x, y, z)
#     """
#     # Unpack cartesian coordinates
#     x, y, z = point[0], point[1], point[2]
    
#     hxy = hypot(x, y)
#     r = hypot(hxy, z)
#     phi = arctan2(y, x)
#     theta = arctan2(z, hxy)

#     return array([r, theta, phi])

# def spherical_to_cartesian(point):
#     """
#     Convert point in spherical polar coordinates to cartesian.
#     Requires: point of coordinates (r, theta, phi)
#     """
#     # Unpack spherical polar coordinates
#     r, theta, phi = point[0], point[1], point[2]

#     x = r * cos(theta) * sin(phi)
#     y = r * sin(theta) * sin(phi)
#     z = r * cos(phi)

#     return array([x, y, z])

def cart2sph(point):
    x, y, z = point[0], point[1], point[2]
    
    hxy = hypot(x, y)
    r = hypot(hxy, z)
    el = arctan2(z, hxy)
    az = arctan2(y, x)
    return array([az, el, r])

def sph2cart(point):
    az, el, r = point[0], point[1], point[2]

    rcos_theta = r * cos(el)
    x = rcos_theta * cos(az)
    y = rcos_theta * sin(az)
    z = r * sin(el)
    return array([x, y, z])


def do_point(point, theta, phi):
    point_sp = cart2sph(point)

    print(point_sp)

    # Rotate by theta and phi
    point_sp[0] += theta
    point_sp[1] += phi

    print(point_sp)

    point = sph2cart(point_sp)
    print(point)

    print()

    return point

theta, phi = 0, pi/4

fig = plt.figure()
ax = fig.add_subplot(projection='3d')

point1 = array([0.5, -0.5, 0])
point2 = array([0.5, 0.5, 0])
point3 = array([-0.5, 0.5, 0])
point4 = array([-0.5, -0.5, 0])

# point = do_point(point, theta, phi)

ax.scatter(point1[0], point1[1], point1[2], c = "red")
ax.scatter(point2[0], point2[1], point2[2], c = "red")
ax.scatter(point3[0], point3[1], point3[2], c = "red")
ax.scatter(point4[0], point4[1], point4[2], c = "red")

point1_r = do_point(point1, theta, phi)
point2_r = do_point(point2, theta, phi)
point3_r = do_point(point3, theta, phi)
point4_r = do_point(point4, theta, phi)

ax.scatter(point1_r[0], point1_r[1], point1_r[2], c = "blue")
ax.scatter(point2_r[0], point2_r[1], point2_r[2], c = "blue")
ax.scatter(point3_r[0], point3_r[1], point3_r[2], c = "blue")
ax.scatter(point4_r[0], point4_r[1], point4_r[2], c = "blue")

ax.axes.set_xlim3d(left=-0.8, right=0.8) 
ax.axes.set_ylim3d(bottom=-0.8, top=0.8) 
ax.axes.set_zlim3d(bottom=-0.8, top=0.8)

print(point1, point2, point3, point4)
print(point1_r, point2_r, point3_r, point4_r)

plt.show()

# from numpy import array, append

# some_list = []

# new_wire = array([array([0, 1]), array([0, 1]), array([0, 1])])

# x = append(some_list[0], new_wire[0][1])

# def torcoil(self, r_i, r_o, n, step):
#         """
#         Create a toroidal coil of:
#             inner radius r_i
#             outer radius r_oD
#             number of turns n
#             step length step
#         Generates `coordinates` and returns
#         """
#         a = r_i
#         b = r_o
#         c = n

#         # Generate diffrent possible angles within this coil
#         t = arange(0, 2*pi, step)

#         x = (a + b * sin(c * t)) * cos(t)
#         y = (a + b * sin(c * t)) * sin(t)
#         z = b * cos(c * t)

#         self.coordinates = [x, y, z]