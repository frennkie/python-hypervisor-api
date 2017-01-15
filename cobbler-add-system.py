#!/usr/bin/python
from __future__ import print_function

import sys
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

    # file to read
    if len(sys.argv) == 2:
        fname = sys.argv[1]
    else:
        print("Give an input file as argument...")
        sys.exit(99)

    # read contents of input file and put it in dict
    with open(fname, "r") as f:
        vm_list = {}
        for line in f:
            line = line.strip()
            # ignore comments
            if not line.startswith("#") and line:
                if line.startswith("[") and line.endswith("]"):
                    guest_name = line[1:-1]
                    vm_list[guest_name] = {}
                    # default values, adjust or remove to specify in the input-file
                    vm_list[guest_name]["guest_dc"] = "ha-datacenter"
                    vm_list[guest_name]["guest_ver"] = "vmx-09"
                    vm_list[guest_name]["guest_iso"] = ""
                    vm_list[guest_name]["guest_os"] = "rhel6Guest"
                    vm_list[guest_name]["guest_network"] = "vlan99"
                    vm_list[guest_name]["cobbler_add"] = ""
                else:
                    key, value = line.split(":")
                    vm_list[guest_name][key.strip()] = value.strip()

    print(vm_list)


    cobbler_url = "https://{0}/cobbler_api".format(config.COBBLER_HOST)
    server = xmlrpclib.Server(cobbler_url)
    token = server.login(config.COBBLER_USER, config.COBBLER_PASS)

    print("Profiles")
    list_profiles(server)
    print("Systems")
    list_systems(server)

    check_for_system(server, "otrs-t2")

    for vm in vm_list:
        vm_info = vm_list[vm]

        print("VM: {0}".format(vm))
        if vm_info["cobbler_add"].lower() in ["yes", "true"]:

            if not any(d['name'] == vm_info["cobbler_profile"] for d in server.get_profiles()):
                raise Exception("Profile does not exist: {0}".format(vm_info["cobbler_profile"]))

            if any(d['name'] == vm for d in server.get_systems()):
                print("Warn: System {0} already exists! Skipping.".format(vm))
                continue

            system_id = server.new_system(token)
            server.modify_system(system_id, "name", vm, token)
            server.modify_system(system_id, "hostname", vm_info["guest_hostname"], token)
            server.modify_system(system_id, 'modify_interface',
                                            {"macaddress-eth0"   : "01:02:03:04:05:07",
                                                "dnsname-eth0"      :  vm_info["guest_hostname"]}, token)
            server.modify_system(system_id, "profile", vm_info["cobbler_profile"], token)

            server.save_system(system_id, token)
            server.sync(token)

        else:
            print("not adding {0} to cobbler (add is not set)".format(vm))

if __name__ == '__main__':
        main()
