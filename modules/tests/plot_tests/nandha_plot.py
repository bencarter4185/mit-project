"""
Test script to plot 8 coils arranged in a circle around the origin.
"""
# Internal Imports
from import_above import allow_above_imports


def main():
    from bs_wires import Wires
    from bs_actions import do_action
    from parse_json import parse_json

    # Hard-code the json_path for sake of ease in this case
    json_path = "./modules/tests/plot_tests/params/nandha_plot2.json"
    coils, actions = parse_json(json_path)

    # Create a new object Wires; a list of all wires and coils which have been created
    wires = Wires()
    for coil in coils:
        wires.new_wire(coil)

    # Iterate through all actions and perform them
    for action in actions:
        if action["execute"] is not False:
            do_action(action, wires)


if __name__ == "__main__":
    allow_above_imports()
    main()
