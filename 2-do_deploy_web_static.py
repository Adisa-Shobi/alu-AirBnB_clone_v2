#!/usr/bin/python3
'''Fabric file to deploy web static

do_pack: Creates an archive of the web_static directory
do_deploy: Moves an archive to the web servers
'''
from fabric.api import *
from datetime import datetime
import os


env.hosts = [
    '54.210.227.60',
    '54.82.115.223'
]
env.user = 'ubuntu'
env.key_filename = '~/.ssh/id_rsa'


def do_pack():
    ''' Creates an archive of the web_static directory
    Using format:
        versions/web_static_<year><month><day><hour><minute><second>.tgz
    '''
    local("mkdir -p versions")
    archive_path = "versions/web_static_{}.tgz".format(
        datetime.now().strftime('%Y%m%d%H%M%S'))
    result = local("tar -cvzf {} web_static".format(archive_path))

    if result.succeeded:
        return archive_path
    return None


def do_deploy(archive_path):
    """Archives to web-servers"""
    if exists(archive_path) is False:
        return False
    try:
        file_n = archive_path.split("/")[-1]
        no_ext = file_n.split(".")[0]
        path = "/data/web_static/releases/"
        put(archive_path, '/tmp/')
        run('mkdir -p {}{}/'.format(path, no_ext))
        run('tar -xzf /tmp/{} -C {}{}/'.format(file_n, path, no_ext))
        run('rm /tmp/{}'.format(file_n))
        run('mv {0}{1}/web_static/* {0}{1}/'.format(path, no_ext))
        run('rm -rf {}{}/web_static'.format(path, no_ext))
        run('rm -rf /data/web_static/current')
        run('ln -s {}{}/ /data/web_static/current'.format(path, no_ext))
        return True
    except:
        return False
