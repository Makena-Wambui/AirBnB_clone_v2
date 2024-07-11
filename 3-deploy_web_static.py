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
import os
from fabric.contrib import files

# Environment configuration:
# Remote hosts where we are distributing our archive
env.hosts = ['18.235.243.79', ' 34.207.57.119']

# Define the username to use for SSH connections
env.user = 'ubuntu'

# Define the path to the private key file for SSH authentication
env.key_filename = '~/.ssh/id_rsa'


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
        return None


"""
This script distributes an archive to your web servers,
using the function do_deploy.

Returns False if the file at the path archive_path doesn’t exist.

We import the functions, run, put, env from fabric's api module.
We use them for ssh operations.

SUMMARY:
    This script automates the deployment process by
    uploading an archive, extracting its contents,
    moving them to a designated directory,
    creating a symbolic link for easy access,
    and handling errors gracefully
"""


def do_deploy(archive_path):
    """
    Function: do_deploy

    This function takes archive_path as an argument:
    ie the path to the archive file that will be deployed.
    """

    # Check if the archive_path exists locally using os.path.exists().
    # If not, returns False
    if not os.path.exists(archive_path):
        return False

    # Base directory where deployed files will be stored.
    base_dir = '/data/web_static/releases/'

    # Extracts and prepares paths and names frm archive_path argument
    tmp = archive_path.split('.')[0]
    f_name = tmp.split('/')[1]

    destination_path = base_dir + f_name

    try:
        # put() function to upload the archive file to the /tmp directory on
        # the remote server
        put(archive_path, '/tmp')

        # Create the directory structure using run().
        run('mkdir -p {}'.format(destination_path))

        # Extracts the uploaded archive (tar -xzf /tmp/{}.tgz -C {}).
        run('tar -xzf /tmp/{}.tgz -C {}'.format(f_name, destination_path))

        # Clean Up: delete the uploaded archive after extracting
        run('rm -f /tmp/{}.tgz'.format(f_name))

        # Move the contents of the extracted web_static dir
        run('mv {}/web_static/* {}/'
            .format(destination_path, destination_path))

        # Delete  Old web_static Directory
        run('rm -rf {}/web_static'.format(destination_path))

        # Update Symbolic Link:
        # Remove any existing /data/web_static/current symbolic link.
        # create a new one pointing to destination_path
        run('rm -rf /data/web_static/current')

        run('ln -s {} /data/web_static/current'.format(destination_path))

        # Success
        return True

    # except block to catch any errors/exceptions
    except Exception:
        return False


def deploy():
    """
    Function: deploy

    This function does the work of both do_pack() and do_deploy()

    This function orchestrates the entire deployment process
    by calling do_pack to create the archive and then calling
    do_deploy to deploy the archive to the web servers.
    """

    # Returns the created archive
    archive = do_pack()

    print(archive)

    # Check if the archive was created successfully.
    if archive is None:
        return False

    # then we call do_deploy providing archive as arg and return its result
    return do_deploy(archive)
