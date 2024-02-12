#!/usr/bin/python3
'''
Fabric file to deploy web static

This script uses  fabric to make deployments
of a static app to a remote server
'''
from fabric.api import *
from datetime import datetime


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
