#!/usr/bin/python3
"""
Fabric script that distributes an archive to your web servers, using the
function do_deploy.
"""
from fabric.api import env, put, run
from os.path import exists

env.hosts = ['<IP web-01>', '<IP web-02>']
env.user = 'ubuntu'
env.key_filename = ['my_ssh_private_key']


def do_deploy(archive_path):
    """
    Distributes an archive to your web servers
    """
    if not exists(archive_path):
        return False

    try:
        # Upload archive to /tmp/ directory of web servers
        put(archive_path, "/tmp/")

        # Extract archive to /data/web_static/releases/<archive filename without extension>/
        filename = archive_path.split("/")[-1]
        foldername = filename.split(".")[0]
        run("mkdir -p /data/web_static/releases/{}/".format(foldername))
        run("tar -xzf /tmp/{} -C /data/web_static/releases/{}/"
            .format(filename, foldername))

        # Delete archive from web servers
        run("rm /tmp/{}".format(filename))

        # Move files out of web_static folder
        run("mv /data/web_static/releases/{}/web_static/* \
            /data/web_static/releases/{}/"
            .format(foldername, foldername))

        # Remove empty web_static folder
        run("rm -rf /data/web_static/releases/{}/web_static"
            .format(foldername))

        # Delete old symbolic link
        run("rm -rf /data/web_static/current")

        # Create new symbolic link
        run("ln -s /data/web_static/releases/{}/ /data/web_static/current"
            .format(foldername))

        print("New version deployed!")
        return True

    except Exception as e:
        print(e)
        return False
