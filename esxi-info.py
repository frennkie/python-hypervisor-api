#!/usr/bin/python
from __future__ import print_function
import api_vmware_include
import config

def main():
    # change these to match your installation
    host = config.ESXI_HOST
    user = config.ESXI_USER
    pw = config.ESXI_PASS

    #connect to the host
    host_con = api_vmware_include.connectToHost(host, user, pw)

    # list server type
    print("Type: {}".format(host_con.get_server_type()))

    print("Datacenters: {}".format(host_con.get_datacenters().items()))
    print("Hosts: {}".format(host_con.get_hosts().items()))
    print("Datastores: {}".format(host_con.get_datastores().items()))

    # disconnect from the host
    host_con.disconnect()

if __name__ == '__main__':
    main()
