"""
Writing a biot-savart solver from scratch
"""
import ast
import sys
from modules.parse_json import parse_json
from modules.bs_wires import Wires


def parse_args(args):
    """
    Parse args and kwargs passed into main and return.

    Credit to: <https://stackoverflow.com/questions/49723047/parsing-a-string-as-a-python-argument-list>
    """
    args = 'f({})'.format(args)
    tree = ast.parse(args)
    funccall = tree.body[0].value

    args = [ast.literal_eval(arg) for arg in funccall.args]
    kwargs = {arg.arg: ast.literal_eval(arg.value) for arg in funccall.keywords}
    return args, kwargs


def main():
    """
    Testing how we extract `what to do` from the JSON file.
    """
    # Parse args and kwargs and store args[1] as the filepath for the `params.json` file.
    args, _ = parse_args(sys.argv)
    json_path = args[0][1]

    coils, actions = parse_json(json_path)

    # Create a new object Wires; a list of all wires and coils which have been created
    wires = Wires()
    for coil in coils:
        wires.new_wire(coil)
    wires.print_wires_with_properties()

    # Check if `plot coils` is given as an action. If so, do it
    if any("plot coils" in action for action in actions):
        wires.plot_wires()


if __name__ == '__main__':
    main()
