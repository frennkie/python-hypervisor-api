#!/usr/bin/python
from __future__ import print_function
import sys
import api_vmware_include
import config

def main():
    # change these to match your installation
    host = config.ESXI_HOST
    user = config.ESXI_USER
    pw = config.ESXI_PASS

    if len(sys.argv) == 2:
        vm = sys.argv[1]
    else:
        print("Give a VM name as input...")
        sys.exit(99)

    #connect to the host
    host_con = api_vmware_include.connectToHost(host, user, pw)

    mac = api_vmware_include.getMac(host_con, vm)
    print(" - MAC Address: {0}".format(mac))

    # disconnect from the host
    host_con.disconnect()

if __name__ == '__main__':
    main()
