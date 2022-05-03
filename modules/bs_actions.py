"""
Library file to perform `actions` as requested.
"""
from numpy import asarray, broadcast_arrays, linspace, array, meshgrid, sqrt, pi, floor, log10, zeros_like, zeros, unique
from bs_solver import solve, b_abs
from scipy.constants import mu_0 as mu
import matplotlib.pyplot as plt
from itertools import product
from scipy.interpolate import interp2d


def _round_sig(x, sig=2):
    return round(x, sig-int(floor(log10(abs(x))))-1)


def _validate_magnetic_field(action, wires):
    """
    Validate magnetic field for given parameters.
    """
    # Set up the points (xs, ys, zs) at which the magnetic field will be calculated
    xs = linspace(action["start_point"][0], action["end_point"][0], action["np"])
    ys = linspace(action["start_point"][1], action["end_point"][1], action["np"])
    zs = linspace(action["start_point"][2], action["end_point"][2], action["np"])
    points = array([xs, ys, zs])

    # Calculate resultant magnetic field via bs_solver
    b = solve(wires, points)
    b_mag = b_abs(b)

    # Validation assumes we're only working with one current loop. Compare to analytical solution:
    wire = wires.wires[0]
    current = wire.current
    match action["shape"]:
        case "circle":
            radius = wire.radius
            np = wire.np
            b_analytical = abs(mu*current*radius**2/(2*(zs**2+radius**2)**(3.0/2.0)))
        case "square":
            length = wire.length
            dl = wire.dl
            r = sqrt(zs**2 + (length/2)**2)
            b_analytical = abs((mu*current)/(2*pi*r**2) * (length**2)/(sqrt(zs**2 + (length**2)/2)))

    # Plot graph of results
    plt.style.use("seaborn")
    _, ax = plt.subplots(ncols=1, nrows=1)

    ax.plot(zs, b_mag, label="Numerical solution")
    ax.scatter(zs, b_analytical, label="Analytical Solution")

    ax.legend()
    ax.set_xlabel(r"$z$ (m)")
    ax.set_ylabel(r"$B$ (T)")

    match action["shape"]:
        case "circle":
            ax.set_title(f"Circular Loop Validation, Number of Points = {np}")
        case "square":
            ax.set_title(f"Square Loop Validation, Discretization Length = {dl}")

    # Calculate root mean square error, RMSE
    rmse = sqrt(sum((b_analytical-b_mag)**2.0)/len(b_mag))
    print(f"Root Mean Square Error = {rmse}")

    # Add RMSE to plot
    ax.text(0.8, 0.8, f"RMSE = {_round_sig(rmse, sig = 3)} T", horizontalalignment='center',
            verticalalignment='center', transform=ax.transAxes, fontsize=16)

    plt.show()

    # Set plot style back to default
    plt.style.use("default")


def _plot_wires(action, wires):
    """
    Plot the wires given.
    """
    wires.plot_wires(
        xlim=action["xlim"],
        ylim=action["ylim"],
        zlim=action["zlim"],
        axes_equal=action["axes_equal"]
    )


def _ndmesh(*args):
    args = map(asarray, args)
    return broadcast_arrays(*[x[(slice(None),)+(None,)*i] for i, x in enumerate(args)])


def _plot_slice_xy(action, wires):
    """
    Plots a heatmap of an xy slice of data.
    """
    # Plot graph of results
    plt.style.use("seaborn")
    fig, ax = plt.subplots(ncols=1, nrows=1)

    # Set up the points (xs, ys, zs) at which the magnetic field will be calculated
    xs = linspace(action["xlim"][0], action["xlim"][1], action["np"])
    ys = linspace(action["ylim"][0], action["ylim"][1], action["np"])

    points = zeros([3, int(action["np"]**2)])

    i = 0
    for (x, y) in product(xs, ys):
        points[0][i] = x
        points[1][i] = y
        points[2][i] = 0
        i += 1

    b = solve(wires, points)
    b_mag = b_abs(b)

    cmap = plt.colormaps['inferno']

    x_map = unique(points[0])
    y_map = unique(points[1])

    xx, yy = meshgrid(x_map, y_map)
    bb = b_mag.reshape(len(y_map), len(x_map))
    im = plt.pcolormesh(xx, yy, bb, cmap=cmap, shading="gouraud")
    fig.colorbar(im, ax=ax)

    # # Create a meshgrid for our data
    # xx, yy, zz = _ndmesh(points[0], points[1], b_mag)
    # print(xx)

    # c = ax.pcolormesh(xx, yy, zz, cmap='RdBu', vmin=min(zz), vmax=max(zz))
    # ax.set_title('pcolormesh')
    # # set the limits of the plot to the limits of the data
    # ax.axis([xx.min(), xx.max(), yy.min(), yy.max()])
    # fig.colorbar(c, ax=ax)

    # plt.scatter(points[0], points[1], c=b_mag, cmap='jet', vmin=min(b_mag), vmax=max(b_mag))
    # plt.colorbar()

    if action["axes_equal"]:
        ax.axis("equal")

    plt.show()

    # print(wires)
    # print(points.shape)

    # b = solve(wires, points)
    # b_mag = b_abs(b)
    # print(b)

    # print(len(points))

    # b = solve(wires, points)
    # b_mag = b_abs(b)
    # print(len(b))
    # print(len(b_mag))

    # print(b)
    # print(b_mag)
    # print()

    # i = 0
    # for (x, y) in product(xs, ys):
    #     print(b_mag[i])
    #     ax.scatter(x, y, c=b_mag[i], cmap='jet', vmin=min(b_mag), vmax=max(b_mag))
    #     i += 1

    # ax.colorbar()
    # plt.show()

    # # Calculate resultant magnetic field via bs_solver
    # b = solve(wires, points)
    # b_mag = b_abs(b)

    # xx, yy, zz = meshgrid(xs, ys, zs)
    # b = solve(wires, [xx, yy, zz])

    # # Plot graph of results
    # plt.style.use("seaborn")
    # _, ax = plt.subplots(ncols=1, nrows=1)

    # ax.imshow(b_mag, cmap="hot", interpolation="nearest")


def do_action(action, wires):
    """
    Pattern match the action's name and perform a task accordingly.
    """
    match action["name"]:
        case "validate magnetic field":
            _validate_magnetic_field(action, wires)
        case "plot coils":
            _plot_wires(action, wires)
        case "plot slice xy":
            _plot_slice_xy(action, wires)