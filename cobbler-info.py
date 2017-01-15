#!/usr/bin/python
from __future__ import print_function

import config
import xmlrpclib


def list_distros(server):
    distro_names = [x["name"] for x in server.get_distros()]
    if distro_names:
        return distro_names
    else:
        return "No Distros"


def list_profiles(server):
    profile_names = [x["name"] for x in server.get_profiles()]
    if profile_names:
        return profile_names
    else:
        return "No Profiles"


def list_systems(server):
    system_names = [x["name"] for x in server.get_systems()]
    if system_names:
        return system_names
    else:
        return "No Systems"


def main():
    cobbler_url = "https://{0}/cobbler_api".format(config.COBBLER_HOST)
    server = xmlrpclib.Server(cobbler_url)

    print("Profiles: {0}".format(list_profiles(server)))
    print("Systems: {0}".format(list_systems(server)))


if __name__ == '__main__':
        main()
