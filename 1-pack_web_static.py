#!/usr/bin/python3

"""
This script is designed to create a .tgz (tar gzip) archive of
the contents of the web_static folder from AirBnB Clone repository.
The archive file is named based on the current
date and time to ensure uniqueness.

Imports python's datetime module, which we use to work with date & time.

Imports all functions and classes(*) from Fabric's API.
This is a library used for automating tasks.

The do_pack function will create the archive.
"""
import datetime
from fabric.api import *


def do_pack():
    """
    do_pack function creates the archive;
    it performs the compression.
    """

    # datetime module to get the current date and time.
    # now() function returns a datetime object
    # representing the current date and time.
    now = datetime.datetime.now()

    # create a directory versions, where our archive will be located.
    # If the directory already exists, no error is raised("-p")
    # Use Fabric local function to execute shell commands on local machine.
    local("mkdir -p versions")

    # construct a string for the archive filename using current date and time.
    # ensures each archive has a unique name based on the time it was created

    archive_file = "versions/web_static_{}{}{}{}{}{}.tgz".format(now.year,
                                                                 now.month,
                                                                 now.day,
                                                                 now.hour,
                                                                 now.minute,
                                                                 now.second)

    # Next we create the archive
    # We use the local function to run a local shell command.
    # tar -> an archiving utility.
    result = local("tar -czvf {} web_static".format(archive_file))

    # We check if tar command was successful
    if result.succeeded:
        return archive_file  # return the created archive file
    else:
        print("Compression failed.")
        return None
