# Internal Imports
from import_above import allow_above_imports
import matplotlib.pyplot as plt
from numpy import array, linspace, zeros, unique, meshgrid, pi
from itertools import product
allow_above_imports()
from bs_wires import Wires
from parse_json import parse_json
import bs_solver


def normalise_angle(angle):
    return (angle + 2*pi) % (2*pi)


# Hard-code the json_path for sake of ease in this case
json_path = "./modules/tests/plot_tests/params/nandha_plot2.json"
coils, _ = parse_json(json_path)

# Create a new object Wires; a list of all wires and coils which have been created
wires = Wires()
for coil in coils:
    wires.new_wire(coil)

wires.plot_wires()
# plt.show()

"""
Plots a heatmap of an xy slice of data.
"""
# Plot graph of results
plt.style.use("seaborn")

np = 10
xmin = -2
xmax = 2
ymin = -2
ymax = 2

# Set up the points (xs, ys, zs) at which the magnetic field will be calculated
xs = linspace(xmin, xmax, np)
ys = linspace(ymin, ymax, np)

points = zeros([3, int(np**2)])
b = zeros([3, int(np**2)])
b_mag = zeros(int(np**2))

# i = 0
# for (x, y) in product(xs, ys):
#     points[0][i] = x
#     points[1][i] = y
#     points[2][i] = 0

#     mag = bs_solver.solve(wires, array([x, y, 0]))

    # b[0][i] = mag[0][0]
    # b[1][i] = mag[0][1]
    # b[2][i] = mag[0][2]
    # b_mag[i] = bs_solver.b_abs(mag)

#     i += 1

i = 0
for (x, y) in product(xs, ys):
    points[0][i] = x
    points[1][i] = y
    points[2][i] = 0
    i += 1

# Code to perform a time average
phase_max = 2*pi
timesteps = 4
phase_to_add = phase_max / timesteps

phases = linspace(0, phase_max, timesteps)
modulus = 1

iteration = 0
for phase in range(timesteps):
    # Set the phase of the wire currents
    for wire in wires.wires:
        current_phase = wire.current.imag
        new_phase = normalise_angle(current_phase + phase_to_add)
        wire.set_current(complex(modulus, new_phase))
    print(f"Iteration {iteration} of {timesteps}")

    i = 0
    for (x, y) in product(xs, ys):
        mag = bs_solver.solve(wires, array([x, y, 0]))

        b[0][i] += mag[0][0]
        b[1][i] += mag[0][1]
        b[2][i] += mag[0][2]
        b_mag[i] += bs_solver.b_abs(mag)

        i += 1
    
    iteration += 1

b /= timesteps
b_mag /= timesteps

x_map = unique(points[0])
y_map = unique(points[1])
xx, yy = meshgrid(x_map, y_map)

bx = b[0].reshape(len(y_map), len(x_map))
by = b[1].reshape(len(y_map), len(x_map))
bb = b_mag.reshape(len(y_map), len(x_map))

# Perform a quiver plot
fig, ax = plt.subplots(ncols=1, nrows=1)
ax.quiver(xx, yy, bx, by)
ax.axis("equal")

# Perform a heatmap plot
fig, ax = plt.subplots(ncols=1, nrows=1)
cmap = plt.colormaps['inferno']
im = plt.pcolormesh(xx, yy, bb, cmap=cmap, shading="gouraud")
fig.colorbar(im, ax=ax)

plt.show()





# # b = bs_solver.solve(wires, points)

# x_map = unique(points[0])
# y_map = unique(points[1])
# xx, yy = meshgrid(x_map, y_map)

# bx = b[0].reshape(len(y_map), len(x_map))
# by = b[1].reshape(len(y_map), len(x_map))
# bb = b_mag.reshape(len(y_map), len(x_map))

# # Perform a quiver plot
# fig, ax = plt.subplots(ncols=1, nrows=1)
# ax.quiver(xx, yy, bx, by)
# ax.axis("equal")


# # Perform a heatmap plot
# fig, ax = plt.subplots(ncols=1, nrows=1)
# cmap = plt.colormaps['inferno']
# im = plt.pcolormesh(xx, yy, bb, cmap=cmap, shading="gouraud")
# fig.colorbar(im, ax=ax)


# plt.show()