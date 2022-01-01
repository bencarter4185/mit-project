import os
import sys


def allow_above_imports():
    """
    This hacky code is necessary to import module files from the directory above.
    Python can be pretty awful at relative/absolute imports and it gives me a headache.
    """
    filepath = os.getcwd().replace('\\', '\\\\')
    filepath = f"{filepath}\\\\modules"
    sys.path.append(filepath)
