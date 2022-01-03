"""
Test script to plot 8 coils arranged in a circle around the origin.
"""
# Internal Imports
from matplotlib.pyplot import plot
from import_above import allow_above_imports


def main():
    from bs_wires import Wires
    from parse_json import parse_json

    # Hard-code the json_path for sake of ease in this case
    json_path = "./modules/tests/validation_tests/params/plot_8_coils.json"
    coils, actions = parse_json(json_path)

    # Create a new object Wires; a list of all wires and coils which have been created
    wires = Wires()
    for coil in coils:
        wires.new_wire(coil)

    # wires.plot_wires(zlim=[-1.2, 1.2])
    wires.plot_wires()

    # for wire in wires.wires:
    #     for att in dir(wire):
    #         print(att, getattr(wire, att))

    # # Check if `plot coils` is given as an action. If do, get the dict and plot the coils
    # do_plots = next((d for _, d in enumerate(actions) if "plot coils" in d), None)
    # if do_plots is not None:
    #     zlim = next((d for _, d in enumerate(do_plots["plot coils"]) if "zlim" in d), None)
    #     if zlim is not None:
    #         zlim = do_plots["plot coils"][zlim]
    #     wires.plot_wires(zlim=zlim)

    # # Check if `plot coils` is given as an action. If so, do it
    # if any("plot coils" in action for action in actions):
    #     wires.plot_wires(zlim=[-1.2, 1.2])


if __name__ == "__main__":
    allow_above_imports()
    main()
