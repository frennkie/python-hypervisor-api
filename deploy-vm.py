#!/usr/bin/python
from __future__ import print_function

# Created by Jens Depuydt
# http://www.jensd.be
# http://github.com/jensdepuydt

import sys
import api_vmware_include
import xmlrpclib
import time
import config

def main():
    # file to read
    if len(sys.argv) == 2:
        fname = sys.argv[1]
    else:
        print("Give an input file as argument...")
        sys.exit(99)

    cobbler_url = "https://{0}/cobbler_api".format(config.COBBLER_HOST)
    server = xmlrpclib.Server(cobbler_url)
    token = server.login(config.COBBLER_USER, config.COBBLER_PASS)


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
                    vm_list[guest_name]["esx_host"] = config.ESXI_CLUSTER_HOST
                    vm_list[guest_name]["esx_dc"] = config.ESXI_DATACENTER
                    vm_list[guest_name]["guest_ver"] = config.ESXI_VM_VERSION
                    vm_list[guest_name]["guest_iso"] = ""
                    vm_list[guest_name]["guest_os"] = "rhel6Guest"
                    vm_list[guest_name]["guest_datastore"] = config.ESXI_VM_DATASTORE
                    vm_list[guest_name]["guest_network"] = config.ESXI_VM_NETWORK
                    vm_list[guest_name]["cobbler_add"] = ""
                else:
                    key, value = line.split(":")
                    vm_list[guest_name][key.strip()] = value.strip()

    print("- Connect to hypervisor ({0})".format(config.ESXI_HOST))
    host_pw = config.ESXI_PASS

    host_con = api_vmware_include.connectToHost(config.ESXI_HOST, config.ESXI_USER , host_pw)

    for vm in vm_list:
        vm_info = vm_list[vm]

        if vm_info["purpose"]:
            guest_name_purpose = "{0} ({1})".format(vm, vm_info["purpose"])
        else:
            guest_name_purpose = "{0}".format(vm)
        print("  VM: {0}".format(guest_name_purpose))
        print("  * Settings:".format())
        print("    - datacenter: {0}".format(vm_info["esx_dc"]))
        print("    - target host: {0}".format(vm_info["esx_host"]))
        print("    - datastore: {0}".format(vm_info["guest_datastore"]))
        print("    - memory: {0} {1}".format(vm_info["guest_mem"], "MB"))
        print("    - #cpu: {0}".format(vm_info["guest_cpu"]))
        print("    - space: {0} {1}".format(vm_info["guest_space"], "GB"))

        print("  * Create VM..".format())

        res = api_vmware_include.createGuest(host_con,
                                            vm_info["esx_dc"],
                                            vm_info["esx_host"],
                                            guest_name_purpose,
                                            vm_info["guest_ver"],
                                            int(vm_info["guest_mem"]),
                                            int(vm_info["guest_cpu"]),
                                            vm_info["guest_iso"],
                                            vm_info["guest_os"],
                                            int(vm_info["guest_space"]),
                                            vm_info["guest_datastore"],
                                            vm_info["guest_network"])

        print("   -", res)
        if res != "Succesfully created guest: {0}".format(guest_name_purpose):
            print("Finished unsuccesfully, aborting")
            host_con.disconnect()
            sys.exit(99)

        print("  * Start VM..".format())
        api_vmware_include.powerOnGuest(host_con, guest_name_purpose)

        time.sleep(1)
        mac = api_vmware_include.getMac(host_con, guest_name_purpose)
        print("   - MAC Address: {0}".format(mac))


        if vm_info["cobbler_add"].lower() in ["yes", "true"]:

            if not any(d['name'] == vm_info["cobbler_profile"] for d in server.get_profiles()):
                raise Exception("Profile does not exist: {0}".format(vm_info["cobbler_profile"]))

            if any(d['name'] == vm for d in server.get_systems()):
                print("Warn: System {0} already exists! Skipping.".format(vm))
                continue

            print("    - adding to cobbler".format())

            system_id = server.new_system(token)
            server.modify_system(system_id, "name", vm, token)
            server.modify_system(system_id, "hostname", vm_info["guest_hostname"], token)
            server.modify_system(system_id, 'modify_interface',
                                            {"macaddress-eth0": mac,
                                             "dnsname-eth0": vm_info["guest_hostname"]}, token)
            server.modify_system(system_id, "profile", vm_info["cobbler_profile"], token)

            server.save_system(system_id, token)
            server.sync(token)

        else:
            print("    - not adding to cobbler (add is not set)".format())


        print("---".format())
    print("* Disconnect from hypervisor")
    host_con.disconnect()

if __name__ == '__main__':
        main()
