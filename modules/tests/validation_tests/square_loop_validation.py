"""
Test script to compare the magnetic fields calculated by the Biot-Savart solver vs. an analytical solution.

Circular loop
"""
# Internal Imports
from import_above import allow_above_imports
# External imports
from numpy import array, linspace, sqrt, pi, floor, log10
from scipy.constants import mu_0 as mu
import matplotlib.pyplot as plt
from timeit import timeit  # noqa: F401


def round_sig(x, sig=2):
    return round(x, sig-int(floor(log10(abs(x))))-1)


def main(timing=False):
    """
    square_loop_validation.py

    Parse `square_loop_validation.json` for simulation properties

    Define a square loop with properties:
        - centre (x, y, z) = (0, 0, 0)
        - side length = 2
        - discretization length = 0.1
        - number of loops = 1
        - orientation (theta, phi) = (0, 0)
        - current (magnitude, phase) = (1A, 0)

    Calculate magnetic field for (x, y) = (0, 0) with z from 0.1m to 10m
    """
    # Internal imports
    from bs_wires import Wires
    from bs_solver import solve, b_abs
    from load_json import parse_json

    # Hard-code the json_path for sake of ease in this case
    json_path = "./modules/tests/validation_tests/params/square_loop_validation.json"
    coils, actions = parse_json(json_path)

    # Create a new object Wires; a list of all wires and coils which have been created
    wires = Wires()
    for coil in coils:
        wires.new_wire(coil)

    # Hard coded to assume it needs to calculate magnetic field along a line.
    job = actions["calculate magnetic field"]
    xs = linspace(job["start point"]["x"], job["end point"]["x"], job["number of points"])
    ys = linspace(job["start point"]["y"], job["end point"]["y"], job["number of points"])
    zs = linspace(job["start point"]["z"], job["end point"]["z"], job["number of points"])
    points = array([xs, ys, zs])

    # Calculate resultant magnetic field via bs_solver
    b = solve(wires, points)
    b_mag = b_abs(b)

    # Do plots and comparison if not timing execution
    if timing is False:
        # Extract wire properties for ease of analytical solution calculation
        test_loop = wires.wires[0]
        current = test_loop.current
        length = test_loop.length

        # Calculate analytical solution of magnetic field due to current loop
        # Calculate analytical solution of magnetic field due to current loop
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
        ax.set_title(f"Square Loop Validation, Discretization Length = {test_loop.dl}")

        # Calculate root mean square error, RMSE
        rmse = sqrt(sum((b_analytical-b_mag)**2.0)/len(b_mag))
        print(f"Root Mean Square Error = {rmse}")

        # Add RMSE to plot
        ax.text(0.8, 0.8, f"RMSE = {round_sig(rmse, sig = 3)} T", horizontalalignment='center',
                verticalalignment='center', transform=ax.transAxes, fontsize=16)

        plt.show()


if __name__ == "__main__":
    allow_above_imports()

    # # Time how long it takes to execute the whole simulation. Turn this off later.
    # repeats = 100
    # execution_time = timeit(lambda: main(True), number=repeats)
    # avg_time = execution_time/repeats
    # print("Square Loop:")
    # print(f"total runtime over {repeats} repeats = {execution_time:.3f} seconds")
    # print(f"average runtime = {avg_time:.3f} seconds\n")

    # Comment this out if I want to time how long the code takes to execute
    main()
