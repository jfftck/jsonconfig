import os


def system_path(path):
    """
    Converts paths with system variables and returns the absolute normalized path.

    :param path: string
    """
    return os.path.normpath(os.path.abspath(os.path.expanduser(os.path.expandvars(path))))
