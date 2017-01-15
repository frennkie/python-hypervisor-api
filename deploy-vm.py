#!/usr/bin/python
from __future__ import print_function

# Created by Jens Depuydt
# http://www.jensd.be
# http://github.com/jensdepuydt

import sys
import api_vmware_include
import time
import config

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
                else:
                    key, value = line.split(":")
                    vm_list[guest_name][key.strip()] = value.strip()

    for vm in vm_list:
        print("*" * sum((12, len(vm))))
        print("***** {0} *****".format(vm))
        print("*" * sum((12, len(vm))))
        vm_info = vm_list[vm]

    print(" - Connect to hypervisor")
    host_pw = config.ESXI_PASS

    host_con = api_vmware_include.connectToHost(config.ESXI_HOST, config.ESXI_USER , host_pw)

    print(" - Create VM on host")

    if vm_info["purpose"]:
        guest_name_purpose = "{0} ({1})".format(vm, vm_info["purpose"])
    else:
        guest_name_purpose = "{0}".format(vm)
    print(" - name: {0}".format(guest_name_purpose))
    print(" - memory: {0}".format(vm_info["guest_mem"], "MB"))
    print(" - #cpu: {0}".format(vm_info["guest_cpu"]))
    print(" - space: {0}".format(vm_info["guest_space"], "GB"))
    print(" - datastore: {0}".format(vm_info["datastore"]))
    print(" - target host: {0}".format(vm_info["esx_host"]))
    print(" - hypervisor: {0}".format(vm_info["host"]))

    res = api_vmware_include.createGuest(host_con, vm_info["guest_dc"], vm_info["esx_host"], guest_name_purpose, vm_info["guest_ver"], int(vm_info["guest_mem"]), int(vm_info["guest_cpu"]), vm_info["guest_iso"], vm_info["guest_os"], int(vm_info["guest_space"]), vm_info["datastore"], vm_info["guest_network"])

    print(" -", res)
    if res != "Succesfully created guest: {0}".format(guest_name_purpose):
        print("Finished unsuccesfully, aborting")
        host_con.disconnect()
        sys.exit(99)

    print(" - Start the VM")
    api_vmware_include.powerOnGuest(host_con, guest_name_purpose)

    time.sleep(1)
    mac = api_vmware_include.getMac(host_con, guest_name_purpose)
    print(" - MAC Address: {0}".format(mac))

    print(" - Disconnect from hypervisor")
    host_con.disconnect()

if __name__ == '__main__':
        main()
