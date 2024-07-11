#!/usr/bin/python3

"""
This script deletes out-of-date archives, using the function do_clean

It deletes them from both local and remote servers.
It keeps only a specified number of
the most recent archives and deletes the rest.

"""
import os
from fabric.api import *

# specifies the remote hosts on whic the commands will be run.
env.hosts = ["18.235.243.79", "34.207.57.119"]


def do_clean(number=0):
    """
    do_clean: deletes old archives,
    keeping only a specified number of the most recent ones.

    number=0 is default parameter value indicating
    how many recent archives to keep.

    If number is 0 or 1, keep only the most recent version of your archive.
    if number is 2, keep the most recent,
    and second most recent versions of your archive.
    etc.
    """

    # if number is 0, we default to 1, ie keep only the most recent version.
    # Else keep the value of the number parameter
    number = 1 if int(number) == 0 else int(number)

    # Lists and sorts the archives in the versions directory.
    arch_files = sorted(os.listdir("versions"))

    # Then we use list method, pop:
    # It removes the most recent number of archives from the list (those to be
    # kept)
    [arch_files.pop() for i in range(number)]

    # Then we use the lcd context manager to cd into versions
    # This handles local archives in versions
    with lcd("versions"):
        # Then use local to remove the remaining (old) archives in the versions
        # directory.
        [local("rm ./{}".format(file)) for file in arch_files]

    # Handle the remote host
    # Use cd context manager to execute commands on the remote host
    # Changes the remote directory to "/data/web_static/releases".
    with cd("/data/web_static/releases"):
        # Lists and sorts the files in the remote directory by
        # modification time and splits the output into a list.
        arch_files = run("ls -tr").split()

        # Filters the list to include only archives with "web_static_" in their
        # names.
        arch_files = [file for file in arch_files if "web_static_" in file]

        # Removes the most recent number of archives from the list (those to be
        # kept)
        [arch_files.pop() for i in range(number)]

        # Deletes the remaining (old) archives in the remote directory.
        [run("rm -rf ./{}".format(file)) for file in arch_files]
