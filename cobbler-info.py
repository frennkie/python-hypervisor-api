#!/usr/bin/python
from __future__ import print_function

import config
import xmlrpclib

def check_for_system(server, name=None):
    if not name:
        raise Exception("please specfiy name")

    print("Test whether \"{0}\" is in list of systems..".format(name))

    res = any(d['name'] == 'otrs-t2' for d in server.get_systems())

    if res:
        print("found")
    else:
        print("not found")
    return res


def list_distros(server):
    distro_names = [x["name"] for x in server.get_distros()]
    if distro_names:
        print(distro_names)
    else:
        print("No Distros")
    return distro_names

def list_profiles(server):
    profile_names = [x["name"] for x in server.get_profiles()]
    if profile_names:
        print(profile_names)
    else:
        print("No Profiles")
    return profile_names

def list_systems(server):
    system_names = [x["name"] for x in server.get_systems()]
    if system_names:
        print(system_names)
    else:
        print("No Systems")
    return system_names

def main():

    cobbler_url = "https://{0}/cobbler_api".format(config.COBBLER_HOST)
    server = xmlrpclib.Server(cobbler_url)
    token = server.login(config.COBBLER_USER, config.COBBLER_PASS)

    print("Profiles")
    list_profiles(server)
    print("Systems")
    list_systems(server)

    check_for_system(server, "otrs-t2")

if __name__ == '__main__':
        main()
