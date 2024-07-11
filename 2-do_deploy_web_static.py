#!/usr/bin/python3

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


import os
from fabric.contrib import files
from fabric.api import env, put, run

# Environment configuration:
# Remote hosts where we are distributing our archive
env.hosts = ['18.235.243.79', '	34.207.57.119']

# Define the username to use for SSH connections
env.user = 'ubuntu'

# Define the path to the private key file for SSH authentication
env.key_filename = '~/.ssh/id_rsa'


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
    except Exception as err:
        print(err)
        # Failure
        return False
